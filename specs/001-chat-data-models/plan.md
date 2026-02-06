# Implementation Plan: AI Chat Backend & Data Models

**Branch**: `001-chat-data-models` | **Date**: 2026-02-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-chat-data-models/spec.md`

## Summary

Implement persistent data storage for AI chat backend with three core entities: Tasks (todo items), Conversations (chat sessions), and Messages (chat history). All data enforces strict user isolation at database and API levels using Better Auth JWT authentication. System uses SQLModel ORM with Neon Serverless PostgreSQL, implementing CRUD operations via FastAPI RESTful endpoints with automatic timestamp tracking and cascade deletes.

**Technical Approach**: Database-first design with PostgreSQL schema → SQLModel ORM models → FastAPI route handlers → Integration tests for data integrity and user isolation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14+, Alembic 1.13+, Pydantic 2.5+, asyncpg 0.29+
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, connection pooling enabled)
**Testing**: pytest 7.4+, pytest-asyncio 0.21+, FastAPI TestClient
**Target Platform**: Linux server (containerized deployment recommended)
**Project Type**: Web application (backend API only, no frontend)
**Performance Goals**: <500ms query response for 100-message conversations, support 100 concurrent users
**Constraints**: 1-week implementation timeline, SQLModel ORM only (no raw SQL), UTC timestamps mandatory
**Scale/Scope**: 3 database tables (Task, Conversation, Message), 9 API endpoints, authentication via Better Auth JWT

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Accuracy ✅
- ✅ Timestamps (created_at, updated_at) enforced via SQLModel defaults and on_update triggers
- ✅ Message history persisted with foreign key integrity to conversations
- ✅ Task state transitions tracked via updated_at field
- ✅ No silent data loss: database constraints prevent orphaned records

**Status**: PASS - All accuracy requirements met

### II. Security ✅
- ✅ User ownership enforced at database level: foreign key constraints on user_id (NOT NULL)
- ✅ User ownership enforced at API level: JWT validation middleware + query filters by user_id
- ✅ No cross-user access: authorization checks on all endpoints
- ✅ Better Auth JWT integration for authentication
- ✅ No secrets logged: structured logging excludes sensitive fields

**Status**: PASS - All security requirements met

### III. Reproducibility ✅
- ✅ Explicit SQLModel schemas for all entities
- ✅ Alembic migrations for versioned schema changes
- ✅ Pydantic response models for consistent JSON schemas
- ✅ Test fixtures with deterministic data
- ✅ UTC timestamps eliminate timezone ambiguity

**Status**: PASS - All reproducibility requirements met

### IV. Rigor ✅
- ✅ Pydantic models for request/response validation
- ✅ SQLModel with type hints for database models
- ✅ FastAPI HTTPException for error handling with status codes
- ✅ OpenAPI auto-generation enabled (FastAPI default)
- ✅ Dependency injection for database sessions (Depends pattern)
- ✅ Structured logging with JSON format (python-json-logger)

**Status**: PASS - All rigor requirements met

### V. Schema Integrity ✅
- ✅ Task model: id, title, description, status, priority, user_id, created_at, updated_at
- ✅ Conversation model: id, title, user_id, created_at, updated_at
- ✅ Message model: id, conversation_id, role, content, created_at
- ✅ Foreign keys enforced with ON DELETE CASCADE for conversations→messages
- ✅ NOT NULL constraints on user_id and conversation_id
- ✅ Alembic migrations for schema evolution

**Status**: PASS - All schema integrity requirements met

**Overall Constitution Status**: ✅ ALL GATES PASSED - No violations to justify

## Project Structure

### Documentation (this feature)

```text
specs/001-chat-data-models/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── tasks.openapi.yaml
│   ├── conversations.openapi.yaml
│   └── messages.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task SQLModel
│   │   ├── conversation.py  # Conversation SQLModel
│   │   └── message.py       # Message SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── task.py          # Task Pydantic request/response schemas
│   │   ├── conversation.py  # Conversation Pydantic schemas
│   │   └── message.py       # Message Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (DB session, auth)
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   ├── conversations.py # Conversation CRUD endpoints
│   │   └── messages.py      # Message create/read endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings (database URL, JWT secret)
│   │   ├── database.py      # SQLModel engine setup
│   │   └── auth.py          # JWT validation middleware
│   └── main.py              # FastAPI app initialization
├── alembic/
│   ├── versions/
│   │   └── 001_initial_schema.py  # Initial migration
│   └── env.py
├── tests/
│   ├── conftest.py          # Test fixtures (DB, auth mocks)
│   ├── integration/
│   │   ├── test_tasks.py
│   │   ├── test_conversations.py
│   │   └── test_messages.py
│   └── unit/
│       ├── test_task_model.py
│       ├── test_conversation_model.py
│       └── test_message_model.py
├── alembic.ini
├── pyproject.toml
└── .env.example
```

**Structure Decision**: Web application structure (Option 2) selected because:
- Feature explicitly targets backend API (no frontend in scope)
- Existing project has `backend/` directory (verified from README.md)
- Separation of concerns: models, schemas, API routes in dedicated directories
- Aligns with FastAPI best practices for medium-sized applications

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected - this section remains empty.*

## Phase 0: Research & Decisions

### Research Topics

All technical context resolved - no unknowns requiring research. See [research.md](research.md) for detailed decisions.

**Key Decisions Made**:
1. **Database Connection**: AsyncPG driver with SQLModel async engine for Neon PostgreSQL
2. **Migration Strategy**: Alembic for schema versioning (standard for SQLModel projects)
3. **Authentication Integration**: Dependency injection pattern for JWT validation (FastAPI standard)
4. **Timestamp Management**: SQLModel `default` and `sa_column_kwargs` for automatic timestamps
5. **Cascade Deletes**: PostgreSQL ON DELETE CASCADE for conversation→message relationship

## Phase 1: Design & Contracts

### Data Models

See [data-model.md](data-model.md) for comprehensive entity definitions with field types, constraints, and relationships.

**Entities Summary**:
- **Task**: Todo item with status/priority enums, user ownership
- **Conversation**: Chat session with user ownership, contains messages
- **Message**: Chat message with role enum (user/assistant), belongs to conversation
- **User**: Referenced entity (managed by Better Auth, not defined here)

### API Contracts

See [contracts/](contracts/) directory for OpenAPI specifications:
- `tasks.openapi.yaml`: Task CRUD endpoints (POST, GET, PUT, DELETE)
- `conversations.openapi.yaml`: Conversation CRUD endpoints
- `messages.openapi.yaml`: Message create/read endpoints (no update/delete)

**Endpoint Summary** (9 total):
- Tasks: 5 endpoints (create, list, get, update, delete)
- Conversations: 5 endpoints (create, list, get, update, delete)
- Messages: 2 endpoints (create, list by conversation)

### Quickstart

See [quickstart.md](quickstart.md) for:
- Environment setup (Python 3.11+, virtual environment)
- Dependency installation (`pip install -e .`)
- Database configuration (Neon connection string)
- Database migration (`alembic upgrade head`)
- Running development server (`uvicorn src.main:app --reload`)
- Running tests (`pytest`)

## Phase 2: Implementation Planning

**Not included in this document** - See `/sp.tasks` command output for:
- Task breakdown by user story
- Dependency ordering (schema → models → API → tests)
- Parallel task opportunities
- Acceptance criteria per task

## Next Steps

1. ✅ Phase 0 complete: All research decisions documented in research.md
2. ✅ Phase 1 complete: Data models, contracts, and quickstart documented
3. ⏳ Phase 2 pending: Run `/sp.tasks` to generate implementation task list
4. ⏳ Implementation: Follow tasks.md to build feature incrementally

## Architectural Decision Records

No significant architectural decisions requiring ADR documentation at this stage. Standard patterns used:
- FastAPI + SQLModel (industry standard for Python APIs)
- RESTful endpoints (standard HTTP API design)
- JWT authentication (standard for stateless auth)
- Alembic migrations (standard for SQLAlchemy/SQLModel)

If complex decisions emerge during implementation (e.g., caching strategy, query optimization), create ADRs using `/sp.adr` command.
