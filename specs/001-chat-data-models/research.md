# Research & Technical Decisions: AI Chat Backend & Data Models

**Feature**: 001-chat-data-models
**Created**: 2026-02-06
**Phase**: 0 (Research)

## Overview

This document captures research findings and technical decisions for the AI Chat Backend & Data Models feature. All decisions are made to support the three core entities (Task, Conversation, Message) with strict user isolation and timestamp tracking.

## Decision 1: Database Connection Strategy

**Decision**: Use AsyncPG driver with SQLModel async engine

**Rationale**:
- Neon Serverless PostgreSQL recommends async connections for optimal performance
- AsyncPG is the fastest async PostgreSQL driver for Python
- SQLModel async engine provides connection pooling out of the box
- Reduces latency for concurrent requests (target: 100 concurrent users)

**Alternatives Considered**:
- **psycopg3**: Mature but synchronous (blocks I/O), not ideal for async FastAPI
- **SQLAlchemy 2.0 async**: Adds layer of abstraction, SQLModel already wraps this

**Implementation**:
```python
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    pool_size=10,  # Connection pool size
    max_overflow=20  # Extra connections when pool full
)
```

## Decision 2: Migration Strategy

**Decision**: Alembic for schema versioning

**Rationale**:
- Industry standard for SQLAlchemy/SQLModel migrations
- Supports both upgrade and downgrade paths
- Generates migrations from SQLModel changes (via `alembic revision --autogenerate`)
- Required for production deployments (cannot rely on SQLModel.metadata.create_all)

**Alternatives Considered**:
- **Manual SQL scripts**: Error-prone, no versioning, no rollback
- **SQLModel create_all()**: Only for development, doesn't track changes

**Implementation**:
- Initial migration (`001_initial_schema.py`) creates all three tables
- Subsequent migrations track schema changes incrementally
- Migrations run before app startup in deployment pipeline

## Decision 3: Authentication Integration

**Decision**: Dependency injection pattern for JWT validation

**Rationale**:
- FastAPI's Depends system enforces authentication at route level
- Centralizes JWT validation logic in single dependency function
- Automatically extracts user_id from JWT claims for query filtering
- Provides clear error responses (401 Unauthorized) when token invalid

**Alternatives Considered**:
- **Middleware**: Global but harder to skip for public endpoints (e.g., health checks)
- **Decorator pattern**: Not idiomatic for FastAPI, less type-safe

**Implementation**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)) -> str:
    """Validate JWT and extract user_id"""
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Usage in routes:
@app.get("/api/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id automatically filtered
    return await Task.get_by_user(user_id)
```

## Decision 4: Timestamp Management

**Decision**: SQLModel `default` and `sa_column_kwargs` for automatic timestamps

**Rationale**:
- Database-level defaults ensure timestamps even if ORM bypassed
- `func.now()` uses database clock (consistent for all records)
- `onupdate=func.now()` triggers automatic updated_at refresh
- UTC timezone enforced via database configuration

**Alternatives Considered**:
- **Python datetime.utcnow()**: Client-side, inconsistent across servers
- **Triggers**: More complex, harder to test, unnecessary with SQLModel

**Implementation**:
```python
from sqlmodel import Field, SQLModel
from sqlalchemy import func
from datetime import datetime

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now()}
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now()
        }
    )
```

## Decision 5: Cascade Delete Strategy

**Decision**: PostgreSQL ON DELETE CASCADE for conversation→message relationship

**Rationale**:
- Spec requirement: deleting conversation must delete all messages
- Database-level cascade is reliable (no orphaned messages if ORM skipped)
- Prevents data corruption from incomplete deletes
- Simpler than application-level cascade (no manual deletion loop)

**Alternatives Considered**:
- **Application-level cascade**: Manual loop to delete messages first, error-prone
- **Soft deletes**: Adds complexity (deleted flag), not required by spec

**Implementation**:
```python
from sqlmodel import Field, Relationship

class Conversation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Message(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversation.id",
        ondelete="CASCADE"  # Database-level cascade
    )
    conversation: Conversation = Relationship(back_populates="messages")
```

## Decision 6: Enum Handling

**Decision**: Python Enum with SQLModel enum type

**Rationale**:
- Type-safe at Python level (IDE autocomplete, type checking)
- Database-level constraint (invalid values rejected)
- Pydantic validation (API request validation)
- Clear documentation in OpenAPI schema

**Alternatives Considered**:
- **String literals**: No validation, error-prone
- **Check constraints**: Manual SQL, not type-safe in Python

**Implementation**:
```python
from enum import Enum
from sqlmodel import Field, SQLModel

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
```

## Decision 7: Pagination Strategy

**Decision**: Offset/limit pagination with query parameters

**Rationale**:
- Simple to implement with SQLModel `.offset()` and `.limit()`
- Standard for REST APIs (widely understood)
- Sufficient for expected scale (hundreds of tasks/conversations per user)
- OpenAPI auto-generates documentation for parameters

**Alternatives Considered**:
- **Cursor-based pagination**: More complex, overkill for this scale
- **Page number pagination**: Less flexible than offset/limit

**Implementation**:
```python
@app.get("/api/tasks")
async def list_tasks(
    user_id: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    query = select(Task).where(Task.user_id == user_id).offset(skip).limit(limit)
    tasks = await session.exec(query)
    return tasks.all()
```

## Decision 8: Error Handling Strategy

**Decision**: FastAPI HTTPException with detailed error messages

**Rationale**:
- Automatic JSON error responses with correct HTTP status codes
- Consistent error format across all endpoints
- OpenAPI documents possible error responses
- Structured error messages for client debugging

**Alternatives Considered**:
- **Custom exception classes**: Unnecessary complexity for this feature
- **Generic error messages**: Poor developer experience

**Implementation**:
```python
from fastapi import HTTPException, status

# 404 Not Found
if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )

# 403 Forbidden (authorization)
if task.user_id != current_user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this task"
    )

# 400 Bad Request (validation)
if not task.title:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task title is required"
    )
```

## Decision 9: Testing Strategy

**Decision**: pytest with TestClient and in-memory SQLite for tests

**Rationale**:
- pytest is Python standard for testing
- TestClient provides synchronous API for FastAPI testing
- In-memory SQLite for fast test execution (no external database)
- Fixtures for reusable test data and authentication mocks

**Alternatives Considered**:
- **Test against real PostgreSQL**: Slower, requires external service
- **unittest**: Less expressive than pytest, no fixtures

**Implementation**:
```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

@pytest.fixture
def client():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers():
    """Mock JWT token for testing"""
    token = create_test_jwt(user_id="test-user-123")
    return {"Authorization": f"Bearer {token}"}

# test_tasks.py
def test_create_task(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": "Test task", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```

## Summary of Key Technologies

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| Language | Python | 3.11+ | Type hints, async support, FastAPI requirement |
| API Framework | FastAPI | 0.104+ | Async support, auto-docs, Pydantic validation |
| ORM | SQLModel | 0.0.14+ | Type-safe, combines SQLAlchemy + Pydantic |
| Database | Neon PostgreSQL | - | Serverless, managed, spec requirement |
| Driver | asyncpg | 0.29+ | Fastest async PostgreSQL driver |
| Migrations | Alembic | 1.13+ | Standard for SQLAlchemy/SQLModel |
| Validation | Pydantic | 2.5+ | Request/response schemas, included with FastAPI |
| Testing | pytest | 7.4+ | Standard Python testing framework |
| Auth | Better Auth JWT | - | Spec requirement (integration only) |

## Research Complete

All technical decisions resolved. No unknowns remain. Proceed to Phase 1 (Design & Contracts).
