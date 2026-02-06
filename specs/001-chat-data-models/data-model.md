# Data Model: AI Chat Backend & Data Models

**Feature**: 001-chat-data-models
**Created**: 2026-02-06
**Phase**: 1 (Design)

## Overview

This document defines the database schema for three core entities: Task, Conversation, and Message. All entities enforce strict user isolation via foreign key constraints and include automatic timestamp tracking.

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │ (Managed by Better Auth, not defined here)
│             │
│ - id (PK)   │
└──────┬──────┘
       │
       │ 1:N
       │
       ├──────────────────────────┬───────────────────────────┐
       │                          │                           │
       ▼                          ▼                           ▼
┌─────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│      Task       │      │   Conversation    │      │                  │
│                 │      │                   │      │                  │
│ - id (PK)       │      │ - id (PK)         │◄─────┤     Message      │
│ - title         │      │ - title           │ 1:N  │                  │
│ - description   │      │ - user_id (FK)    │      │ - id (PK)        │
│ - status        │      │ - created_at      │      │ - conversation_id│
│ - priority      │      │ - updated_at      │      │   (FK)           │
│ - user_id (FK)  │      └───────────────────┘      │ - role           │
│ - created_at    │                                  │ - content        │
│ - updated_at    │                                  │ - created_at     │
└─────────────────┘                                  └──────────────────┘
```

## Entity Definitions

### 1. Task

**Purpose**: Represents a todo item owned by a user

**Table Name**: `task`

**Fields**:

| Field        | Type              | Constraints                  | Description                          |
|--------------|-------------------|------------------------------|--------------------------------------|
| id           | INTEGER           | PRIMARY KEY, AUTO INCREMENT  | Unique task identifier               |
| title        | VARCHAR(255)      | NOT NULL                     | Task title (max 255 characters)      |
| description  | TEXT              | NULL                         | Detailed task description            |
| status       | ENUM              | NOT NULL, DEFAULT 'pending'  | Task status (pending/in_progress/completed) |
| priority     | ENUM              | NOT NULL, DEFAULT 'medium'   | Task priority (low/medium/high)      |
| user_id      | VARCHAR(255)      | NOT NULL, FOREIGN KEY        | Owner user ID (from Better Auth)     |
| created_at   | TIMESTAMP(UTC)    | NOT NULL, DEFAULT NOW()      | Record creation timestamp            |
| updated_at   | TIMESTAMP(UTC)    | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | Last modification timestamp |

**Indexes**:
- `idx_task_user_id`: Index on `user_id` for fast user-specific queries
- `idx_task_status`: Index on `status` for filtering by status
- `idx_task_created_at`: Index on `created_at` for chronological sorting

**Constraints**:
- `user_id` references `user.id` (managed by Better Auth)
- `status` CHECK constraint: value IN ('pending', 'in_progress', 'completed')
- `priority` CHECK constraint: value IN ('low', 'medium', 'high')

**Validation Rules**:
- `title`: Required, max 255 characters, trimmed
- `description`: Optional, max 10,000 characters
- `status`: Must be valid enum value
- `priority`: Must be valid enum value
- `user_id`: Required, must match authenticated user

**State Transitions**:
- pending → in_progress
- in_progress → completed
- in_progress → pending (allowed for rollback)
- No direct pending → completed (must go through in_progress)

### 2. Conversation

**Purpose**: Represents a chat session between a user and AI assistant

**Table Name**: `conversation`

**Fields**:

| Field        | Type              | Constraints                  | Description                          |
|--------------|-------------------|------------------------------|--------------------------------------|
| id           | INTEGER           | PRIMARY KEY, AUTO INCREMENT  | Unique conversation identifier       |
| title        | VARCHAR(255)      | NOT NULL                     | Conversation title (for display)     |
| user_id      | VARCHAR(255)      | NOT NULL, FOREIGN KEY        | Owner user ID (from Better Auth)     |
| created_at   | TIMESTAMP(UTC)    | NOT NULL, DEFAULT NOW()      | Record creation timestamp            |
| updated_at   | TIMESTAMP(UTC)    | NOT NULL, DEFAULT NOW(), ON UPDATE NOW() | Last modification timestamp |

**Indexes**:
- `idx_conversation_user_id`: Index on `user_id` for fast user-specific queries
- `idx_conversation_created_at`: Index on `created_at` for reverse chronological ordering

**Constraints**:
- `user_id` references `user.id` (managed by Better Auth)
- CASCADE DELETE: Deleting conversation deletes all associated messages

**Validation Rules**:
- `title`: Required, max 255 characters, trimmed
- `user_id`: Required, must match authenticated user

**Relationships**:
- 1:N with Message (one conversation has many messages)
- N:1 with User (many conversations belong to one user)

### 3. Message

**Purpose**: Represents a single message within a conversation

**Table Name**: `message`

**Fields**:

| Field            | Type              | Constraints                  | Description                          |
|------------------|-------------------|------------------------------|--------------------------------------|
| id               | INTEGER           | PRIMARY KEY, AUTO INCREMENT  | Unique message identifier            |
| conversation_id  | INTEGER           | NOT NULL, FOREIGN KEY        | Parent conversation ID               |
| role             | ENUM              | NOT NULL                     | Message author (user/assistant)      |
| content          | TEXT              | NOT NULL                     | Message content (unlimited length)   |
| created_at       | TIMESTAMP(UTC)    | NOT NULL, DEFAULT NOW()      | Record creation timestamp            |

**Indexes**:
- `idx_message_conversation_id`: Index on `conversation_id` for fast conversation queries
- `idx_message_created_at`: Index on `created_at` for chronological ordering

**Constraints**:
- `conversation_id` references `conversation.id` with ON DELETE CASCADE
- `role` CHECK constraint: value IN ('user', 'assistant')
- Messages are IMMUTABLE after creation (no update_at field, no updates allowed)

**Validation Rules**:
- `conversation_id`: Required, must exist and belong to authenticated user
- `role`: Required, must be 'user' or 'assistant'
- `content`: Required, max 100,000 characters (arbitrary large limit)

**Relationships**:
- N:1 with Conversation (many messages belong to one conversation)

**Note**: Messages have no direct relationship to User - ownership enforced via Conversation

### 4. User (Reference Only)

**Purpose**: Represents an authenticated user (managed by Better Auth)

**Table Name**: Not defined in this feature (managed externally)

**Referenced Fields**:
- `id`: User identifier (type: VARCHAR or UUID, defined by Better Auth)

**Notes**:
- This entity is NOT created by this feature
- Better Auth manages user table and authentication
- Task and Conversation reference `user.id` via foreign keys
- User ID extracted from JWT token claims during API requests

## Database Migrations

### Initial Migration (001_initial_schema.py)

**Creates**:
1. Task table with indexes and constraints
2. Conversation table with indexes and constraints
3. Message table with indexes, constraints, and cascade delete
4. Enum types for status, priority, and role

**Upgrade Path**:
```sql
-- Create enums
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'completed');
CREATE TYPE task_priority AS ENUM ('low', 'medium', 'high');
CREATE TYPE message_role AS ENUM ('user', 'assistant');

-- Create task table
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status task_status NOT NULL DEFAULT 'pending',
    priority task_priority NOT NULL DEFAULT 'medium',
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_status ON task(status);
CREATE INDEX idx_task_created_at ON task(created_at);

-- Create conversation table
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversation_user_id ON conversation(user_id);
CREATE INDEX idx_conversation_created_at ON conversation(created_at);

-- Create message table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    role message_role NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_message_conversation_id ON message(conversation_id);
CREATE INDEX idx_message_created_at ON message(created_at);

-- Create trigger for updated_at on task
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_task_updated_at BEFORE UPDATE ON task
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversation_updated_at BEFORE UPDATE ON conversation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

**Downgrade Path**:
```sql
DROP TRIGGER IF EXISTS update_conversation_updated_at ON conversation;
DROP TRIGGER IF EXISTS update_task_updated_at ON task;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS message CASCADE;
DROP TABLE IF EXISTS conversation CASCADE;
DROP TABLE IF EXISTS task CASCADE;
DROP TYPE IF EXISTS message_role;
DROP TYPE IF EXISTS task_priority;
DROP TYPE IF EXISTS task_status;
```

## SQLModel Implementations

### Task Model

```python
from sqlmodel import SQLModel, Field
from sqlalchemy import func
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    user_id: str = Field(max_length=255, index=True)
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

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import func
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    user_id: str = Field(max_length=255, index=True)
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

    # Relationship
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import func
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: MessageRole
    content: str
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": func.now()}
    )

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")
```

## Query Examples

### User Isolation Queries

```python
# Get all tasks for authenticated user
tasks = await session.exec(
    select(Task).where(Task.user_id == current_user_id)
).all()

# Get conversations for authenticated user (reverse chronological)
conversations = await session.exec(
    select(Conversation)
    .where(Conversation.user_id == current_user_id)
    .order_by(Conversation.created_at.desc())
).all()

# Get messages for a conversation (with authorization check)
conversation = await session.get(Conversation, conversation_id)
if conversation.user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Not authorized")
messages = await session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.asc())
).all()
```

### Cascade Delete Example

```python
# Deleting conversation automatically deletes all messages
conversation = await session.get(Conversation, conversation_id)
if conversation.user_id != current_user_id:
    raise HTTPException(status_code=403, detail="Not authorized")
await session.delete(conversation)
await session.commit()
# All associated messages are automatically deleted via CASCADE
```

## Data Model Complete

All entities defined with complete field specifications, constraints, relationships, and SQLModel implementations. Proceed to API contract definition.
