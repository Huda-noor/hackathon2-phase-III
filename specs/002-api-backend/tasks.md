# Tasks for Feature: 002-api-backend - Backend & API Development for Todo Web Application

**Feature Branch**: `002-api-backend`
**Date**: 2026-02-07

## Implementation Strategy

This feature will be implemented using an MVP-first approach, delivering independently testable increments.
The overall implementation will proceed in phases: Setup, Foundational, User Stories (in priority order), and a final Polish phase for cross-cutting concerns and testing.

Each task is designed to be specific and actionable, enabling parallel development where indicated.

## Phases

### Phase 1: Setup

*Goal*: Initialize the project environment and basic structure.

- [ ] T001 Set up Python virtual environment and install core dependencies (`fastapi`, `sqlmodel`, `uvicorn`, `python-jose[cryptography]`) in `backend/`.
- [ ] T002 Initialize FastAPI application in `backend/src/main.py`.
- [ ] T003 Configure Alembic for database migrations in `backend/alembic.ini` and `backend/alembic/env.py`.

### Phase 2: Foundational

*Goal*: Establish core infrastructure for database interaction and user identification.

- [ ] T004 Implement database connection and session management in `backend/src/db/database.py`.
- [ ] T005 Define base SQLModel `Base` and `engine` for models in `backend/src/models/base.py`.
- [ ] T006 [P] Create User model (for `OwnerID` reference) in `backend/src/models/user.py`.

### Phase 3: User Story 1 - Secure API Access (Priority: P1)

*Goal*: Implement JWT-based authentication to secure API endpoints.
*Independent Test Criteria*:
    - Unauthenticated requests to protected endpoints return 401 Unauthorized.
    - Requests with invalid/expired tokens return 401 Unauthorized.
    - Requests with valid tokens allow access and correctly identify the user.

- [ ] T007 [P] [US1] Implement JWT utility functions (encoding, decoding, validation) in `backend/src/core/security.py`.
- [ ] T008 [P] [US1] Define JWT settings and constants in `backend/src/core/config.py`.
- [ ] T009 [US1] Implement `get_current_user` dependency for protected routes in `backend/src/api/deps.py`.
- [ ] T010 [US1] Apply authentication dependency to a placeholder protected endpoint in `backend/src/main.py` (will be moved to `api/routes` later).

### Phase 4: User Story 2 - Task CRUD Operations (Priority: P1)

*Goal*: Enable users to Create, Read, Update, and Delete their tasks.
*Independent Test Criteria*:
    - POST `/tasks` creates a new task.
    - GET `/tasks/{id}` retrieves a specific task.
    - GET `/tasks` lists tasks for the authenticated user.
    - PATCH `/tasks/{id}` updates a task.
    - DELETE `/tasks/{id}` removes a task.

- [ ] T011 [P] [US2] Define `Task` SQLModel in `backend/src/models/task.py`.
- [ ] T012 [P] [US2] Create Pydantic schemas for `TaskCreate`, `TaskUpdate`, `TaskRead` in `backend/src/schemas/task.py`.
- [ ] T013 [US2] Implement service layer for Task operations (create, get, get_all, update, delete) in `backend/src/services/task_service.py`.
- [ ] T014 [US2] Create FastAPI router for `/tasks` endpoints (GET, POST, GET/{id}, PATCH/{id}, DELETE/{id}) in `backend/src/api/routes/tasks.py`.
- [ ] T015 [US2] Include `tasks` router in `backend/src/main.py`.

### Phase 5: User Story 3 - Data Isolation & Ownership (Priority: P2)

*Goal*: Ensure users can only access and modify their own tasks.
*Independent Test Criteria*:
    - User A cannot access User B's task IDs (returns 404).
    - User B's task list does not include User A's tasks.

- [ ] T016 [US3] Modify `backend/src/services/task_service.py` to filter tasks by `OwnerID` based on the authenticated user.
- [ ] T017 [US3] Implement authorization logic in `backend/src/services/task_service.py` to prevent users from modifying/deleting tasks they don't own.

### Final Phase: Polish & Cross-Cutting Concerns

*Goal*: Enhance robustness, testability, and maintainability.

- [ ] T018 Implement error handling middleware/exception handlers for common API errors (e.g., 404, 422, 500) in `backend/src/core/exceptions.py`.
- [ ] T019 Add basic logging configuration to `backend/src/core/logging.py` and integrate into `main.py`.
- [ ] T020 Write unit tests for `backend/src/core/security.py` (JWT utility functions) in `backend/tests/unit/test_security.py`.
- [ ] T021 Write integration tests for `backend/src/api/routes/tasks.py` covering CRUD operations with authentication and ownership in `backend/tests/integration/test_tasks_api.py`.
- [ ] T022 Update `backend/.env.example` with all necessary environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`).
- [ ] T023 Generate initial Alembic migration for `User` and `Task` models using `alembic revision --autogenerate -m "Create User and Task tables"`.

## Dependencies

User Story completion order:

1.  Secure API Access (US1)
2.  Task CRUD Operations (US2) - depends on US1 for authentication
3.  Data Isolation & Ownership (US3) - depends on US1 (for user context) and US2 (for tasks)

## Parallel Execution Examples

- **Example 1**: While T007 (JWT functions) and T008 (JWT config) are being implemented, T006 (User model) and T011 (Task model) can be developed in parallel as they have no direct code dependencies at this stage.
- **Example 2**: Once T009 (get_current_user) is ready, T012 (Task schemas) can be developed in parallel with T010 (applying auth to a placeholder endpoint).
- **Example 3**: After all core CRUD endpoints (T014) are implemented, T016 (filtering tasks by OwnerID) and T017 (authorization logic) can be worked on concurrently with T020 (unit tests for security) and T022 (.env.example update).

## Validation

All tasks are formulated to be independently testable. The "Independent Test Criteria" for each User Story ensures that the completion of tasks within that story can be verified in isolation or as part of a minimal functional increment.