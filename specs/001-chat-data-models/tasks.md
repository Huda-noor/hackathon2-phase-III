# Tasks: AI Chat Backend & Data Models

**Input**: Design documents from `/specs/001-chat-data-models/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per spec success criteria SC-004 and SC-006 (automated integration tests)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- Paths shown below use web app structure per plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Python project with pyproject.toml in backend/ directory
- [x] T002 Create directory structure: backend/src/{models,schemas,api,core}, backend/tests/{unit,integration}, backend/alembic/versions
- [x] T003 [P] Configure pyproject.toml with dependencies: fastapi>=0.104, sqlmodel>=0.0.14, alembic>=1.13, asyncpg>=0.29, pydantic>=2.5, pytest>=7.4, pytest-asyncio>=0.21
- [x] T004 [P] Create .env.example file with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, DEBUG, LOG_LEVEL placeholders
- [x] T005 [P] Configure linting tools (Ruff/Black) in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create backend/src/core/config.py with Settings class (Pydantic BaseSettings) for DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, DEBUG, LOG_LEVEL
- [x] T007 Create backend/src/core/database.py with async SQLModel engine setup, connection pooling config (pool_size=10, max_overflow=20)
- [x] T008 [P] Create backend/src/core/auth.py with JWT validation dependency function (get_current_user) using FastAPI HTTPBearer
- [x] T009 Initialize Alembic with `alembic init alembic` command in backend/ directory
- [x] T010 [P] Configure backend/alembic/env.py to use SQLModel metadata and async engine
- [x] T011 [P] Create backend/alembic.ini with database URL configuration
- [x] T012 [P] Create enum definitions in backend/src/models/__init__.py: TaskStatus (pending/in_progress/completed), TaskPriority (low/medium/high), MessageRole (user/assistant)
- [x] T013 Create backend/src/api/deps.py with database session dependency (get_db) using async context manager
- [x] T014 Create backend/src/main.py with FastAPI app initialization, CORS configuration, and router registration placeholders
- [x] T015 [P] Create backend/tests/conftest.py with pytest fixtures: in-memory SQLite engine, test database session, mock JWT tokens for authentication

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Data Persistence (Priority: P1) 🎯 MVP

**Goal**: Implement persistent task storage with full CRUD operations, user isolation, and timestamp tracking

**Independent Test**: Authenticate user, create/read/update/delete tasks via API, verify database storage, confirm cross-user access denied

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T016 [P] [US1] Integration test for task creation in backend/tests/integration/test_tasks.py (POST /api/tasks with auth, verify 201 response, check database)
- [x] T017 [P] [US1] Integration test for task list retrieval in backend/tests/integration/test_tasks.py (GET /api/tasks with auth, verify user isolation)
- [x] T018 [P] [US1] Integration test for task update in backend/tests/integration/test_tasks.py (PUT /api/tasks/{id}, verify updated_at timestamp changes)
- [x] T019 [P] [US1] Integration test for task deletion in backend/tests/integration/test_tasks.py (DELETE /api/tasks/{id}, verify 204 response)
- [x] T020 [P] [US1] Integration test for cross-user access denial in backend/tests/integration/test_tasks.py (User A attempts to access User B's task, verify 403 response)
- [x] T021 [P] [US1] Unit test for Task model validation in backend/tests/unit/test_task_model.py (test enum constraints, required fields, timestamp defaults)

### Implementation for User Story 1

- [x] T022 [US1] Create Task SQLModel in backend/src/models/task.py with all fields (id, title, description, status, priority, user_id, created_at, updated_at), enums, indexes, and timestamp defaults
- [x] T023 [US1] Create Alembic migration 001_create_task_table.py with task table, indexes (user_id, status, created_at), constraints, and updated_at trigger
- [x] T024 [US1] Run `alembic upgrade head` to apply task table migration
- [x] T025 [P] [US1] Create TaskCreate Pydantic schema in backend/src/schemas/task.py (title, description, status, priority with defaults)
- [x] T026 [P] [US1] Create TaskUpdate Pydantic schema in backend/src/schemas/task.py (optional title, description, status, priority)
- [x] T027 [P] [US1] Create TaskResponse Pydantic schema in backend/src/schemas/task.py (all fields including id, user_id, timestamps)
- [x] T028 [US1] Implement POST /api/tasks endpoint in backend/src/api/tasks.py (create task with authenticated user_id, return 201)
- [x] T029 [US1] Implement GET /api/tasks endpoint in backend/src/api/tasks.py (list tasks filtered by user_id, support skip/limit pagination, status filter)
- [x] T030 [US1] Implement GET /api/tasks/{task_id} endpoint in backend/src/api/tasks.py (fetch single task, verify user ownership, return 403 if unauthorized, 404 if not found)
- [x] T031 [US1] Implement PUT /api/tasks/{task_id} endpoint in backend/src/api/tasks.py (update task, verify ownership, return 403 if unauthorized, update updated_at timestamp)
- [x] T032 [US1] Implement DELETE /api/tasks/{task_id} endpoint in backend/src/api/tasks.py (delete task, verify ownership, return 403 if unauthorized, return 204 on success)
- [x] T033 [US1] Register task router in backend/src/main.py with prefix="/api/tasks" and authentication dependency
- [x] T034 [US1] Run pytest backend/tests/integration/test_tasks.py to verify all task integration tests pass

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversation History Storage (Priority: P2)

**Goal**: Implement conversation session management with cascade delete and proper ownership enforcement

**Independent Test**: Authenticate user, create/read/update/delete conversations via API, verify cascade delete removes messages

### Tests for User Story 2

- [ ] T035 [P] [US2] Integration test for conversation creation in backend/tests/integration/test_conversations.py (POST /api/conversations with auth, verify 201 response)
- [ ] T036 [P] [US2] Integration test for conversation list retrieval in backend/tests/integration/test_conversations.py (GET /api/conversations, verify reverse chronological order, user isolation)
- [ ] T037 [P] [US2] Integration test for conversation update in backend/tests/integration/test_conversations.py (PUT /api/conversations/{id}, verify title update and updated_at change)
- [ ] T038 [P] [US2] Integration test for conversation deletion in backend/tests/integration/test_conversations.py (DELETE /api/conversations/{id}, verify 204 and cascade delete of messages)
- [ ] T039 [P] [US2] Integration test for cross-user access denial in backend/tests/integration/test_conversations.py (User A attempts to access User B's conversation, verify 403)
- [ ] T040 [P] [US2] Unit test for Conversation model in backend/tests/unit/test_conversation_model.py (test required fields, timestamp defaults, relationships)

### Implementation for User Story 2

- [ ] T041 [US2] Create Conversation SQLModel in backend/src/models/conversation.py with fields (id, title, user_id, created_at, updated_at), indexes, timestamp defaults, and relationship to messages
- [ ] T042 [US2] Create Alembic migration 002_create_conversation_table.py with conversation table, indexes (user_id, created_at), and updated_at trigger
- [ ] T043 [US2] Run `alembic upgrade head` to apply conversation table migration
- [ ] T044 [P] [US2] Create ConversationCreate Pydantic schema in backend/src/schemas/conversation.py (title required)
- [ ] T045 [P] [US2] Create ConversationUpdate Pydantic schema in backend/src/schemas/conversation.py (optional title)
- [ ] T046 [P] [US2] Create ConversationResponse Pydantic schema in backend/src/schemas/conversation.py (all fields including id, user_id, timestamps)
- [ ] T047 [US2] Implement POST /api/conversations endpoint in backend/src/api/conversations.py (create conversation with authenticated user_id, return 201)
- [ ] T048 [US2] Implement GET /api/conversations endpoint in backend/src/api/conversations.py (list conversations filtered by user_id, reverse chronological order, pagination)
- [ ] T049 [US2] Implement GET /api/conversations/{conversation_id} endpoint in backend/src/api/conversations.py (fetch single conversation, verify ownership, return 403/404)
- [ ] T050 [US2] Implement PUT /api/conversations/{conversation_id} endpoint in backend/src/api/conversations.py (update conversation title, verify ownership, update updated_at)
- [ ] T051 [US2] Implement DELETE /api/conversations/{conversation_id} endpoint in backend/src/api/conversations.py (delete conversation with cascade to messages, verify ownership, return 204)
- [ ] T052 [US2] Register conversation router in backend/src/main.py with prefix="/api/conversations" and authentication dependency
- [ ] T053 [US2] Run pytest backend/tests/integration/test_conversations.py to verify all conversation integration tests pass

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Message History Persistence (Priority: P3)

**Goal**: Implement message storage with role tracking (user/assistant) and chronological ordering within conversations

**Independent Test**: Create conversation, add user and assistant messages, retrieve message history in correct order, verify immutability

### Tests for User Story 3

- [ ] T054 [P] [US3] Integration test for message creation in backend/tests/integration/test_messages.py (POST /api/messages with conversation_id and role, verify 201)
- [ ] T055 [P] [US3] Integration test for message list retrieval in backend/tests/integration/test_messages.py (GET /api/conversations/{id}/messages, verify chronological order)
- [ ] T056 [P] [US3] Integration test for message authorization in backend/tests/integration/test_messages.py (User A attempts to add message to User B's conversation, verify 403)
- [ ] T057 [P] [US3] Integration test for cascade delete in backend/tests/integration/test_messages.py (delete conversation, verify messages also deleted)
- [ ] T058 [P] [US3] Unit test for Message model in backend/tests/unit/test_message_model.py (test role enum, required fields, conversation relationship, no updated_at field)

### Implementation for User Story 3

- [ ] T059 [US3] Create Message SQLModel in backend/src/models/message.py with fields (id, conversation_id, role, content, created_at), foreign key with ON DELETE CASCADE, indexes, and relationship to conversation
- [ ] T060 [US3] Create Alembic migration 003_create_message_table.py with message table, foreign key constraint (ON DELETE CASCADE), indexes (conversation_id, created_at)
- [ ] T061 [US3] Run `alembic upgrade head` to apply message table migration
- [ ] T062 [P] [US3] Create MessageCreate Pydantic schema in backend/src/schemas/message.py (conversation_id, role, content all required)
- [ ] T063 [P] [US3] Create MessageResponse Pydantic schema in backend/src/schemas/message.py (all fields including id, created_at, no updated_at)
- [ ] T064 [US3] Implement POST /api/messages endpoint in backend/src/api/messages.py (create message, verify conversation ownership, return 201)
- [ ] T065 [US3] Implement GET /api/conversations/{conversation_id}/messages endpoint in backend/src/api/messages.py (list messages filtered by conversation_id, chronological order, verify conversation ownership, pagination)
- [ ] T066 [US3] Register message router in backend/src/main.py with prefix="/api/messages" and authentication dependency
- [ ] T067 [US3] Run pytest backend/tests/integration/test_messages.py to verify all message integration tests pass

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T068 [P] Add structured logging (python-json-logger) to backend/src/core/config.py with JSON format configuration
- [ ] T069 [P] Add logging to all API endpoints in backend/src/api/ (log request start, completion, errors with user_id context)
- [ ] T070 [P] Create health check endpoint GET /health in backend/src/main.py (returns 200 OK with database connection status)
- [ ] T071 [P] Configure CORS middleware in backend/src/main.py with allowed origins from environment config
- [ ] T072 [P] Add API documentation metadata to backend/src/main.py (title, description, version, contact info for OpenAPI)
- [ ] T073 Run full test suite with `pytest backend/tests/ -v --cov=backend/src` to verify 100% test pass rate and coverage
- [ ] T074 [P] Create backend/README.md with quickstart instructions (setup, migrations, running server, running tests)
- [ ] T075 [P] Add input validation edge case handling (empty strings, max length, invalid enums) across all endpoints
- [ ] T076 Run quickstart.md validation: follow all setup steps from scratch to ensure documentation accuracy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent from US1)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires US2 conceptually (messages belong to conversations) but technically independent if conversation creation tested separately

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before migrations
- Migrations before endpoints
- Pydantic schemas can be parallel with models
- Endpoints after models and migrations
- Integration tests after endpoint implementation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T008, T010, T011, T012, T015)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Pydantic schemas within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Integration test for task creation in backend/tests/integration/test_tasks.py"
Task: "Integration test for task list retrieval in backend/tests/integration/test_tasks.py"
Task: "Integration test for task update in backend/tests/integration/test_tasks.py"
Task: "Integration test for task deletion in backend/tests/integration/test_tasks.py"
Task: "Integration test for cross-user access denial in backend/tests/integration/test_tasks.py"
Task: "Unit test for Task model validation in backend/tests/unit/test_task_model.py"

# Launch all Pydantic schemas for User Story 1 together:
Task: "Create TaskCreate Pydantic schema in backend/src/schemas/task.py"
Task: "Create TaskUpdate Pydantic schema in backend/src/schemas/task.py"
Task: "Create TaskResponse Pydantic schema in backend/src/schemas/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Task Data Persistence)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Tasks)
   - Developer B: User Story 2 (Conversations)
   - Developer C: User Story 3 (Messages)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests written BEFORE implementation (TDD approach per spec requirements)
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks include exact file paths for clarity
- Total tasks: 76 (Setup: 5, Foundational: 10, US1: 19, US2: 19, US3: 15, Polish: 8)
