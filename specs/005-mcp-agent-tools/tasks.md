# Tasks: MCP Tools & Agent Intelligence

**Input**: Design documents from `specs/005-mcp-agent-tools/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included following a TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. When creating tasks, ensure they align with the project constitution's principles of Intent Accuracy, Determinism, Transparency, and Safety.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
  - **Adapted for this project**: `src/agent/`, `src/tools/`, `src/services/`, `src/main.py`, `tests/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize the Python project and basic FastAPI application structure.

- [ ] T001 Create Python project structure with `pyproject.toml` and basic dependencies (FastAPI, uvicorn, pydantic, any HTTP client) in `./`
- [ ] T002 Configure a virtual environment for the project.
- [ ] T003 Create `src/main.py` with a minimal FastAPI application.
- [ ] T004 Create `src/tools/__init__.py` and `src/services/__init__.py` for module structure.
- [ ] T005 [P] Create initial `tests/unit/__init__.py` and `tests/integration/__init__.py`.

---

## Phase 2: Foundational (Core Tool Definitions)

**Purpose**: Implement the core `Task` data model and service functions for basic task management.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

### Tests for Foundational Phase

- [ ] T006 [P] Unit test for `Task` Pydantic model validation in `tests/unit/test_task_model.py`

### Implementation for Foundational Phase

- [ ] T007 Create `src/services/task_models.py` for Pydantic `Task`, `TaskCreate`, `TaskUpdate` models. (Based on `data-model.md` and `openapi.yml`)
- [ ] T008 Implement `src/services/task_service.py` with in-memory (or simple file-based) CRUD operations for `Task` objects, simulating persistence.
- [ ] T009 Create `src/tools/task_tools.py` to define the Python functions corresponding to the API tools (`add_task`, `list_tasks`, `update_task`, `complete_task`, `delete_task`). These will initially call the `task_service`.

---

## Phase 3: User Story 1 - Task Creation (P1) 🎯 MVP

**Goal**: Enable the AI agent to create new tasks based on natural language input.

**Independent Test**: The agent can successfully create a new task with a title and description, and the task is persisted (simulated by the `task_service`).

### Tests for User Story 1

- [ ] T010 [US1] Integration test for `add_task` API endpoint in `tests/integration/test_task_api.py` (should fail until API implemented)
- [ ] T011 [P] [US1] Unit test for agent's `add_task` tool invocation logic in `tests/unit/test_agent_tools.py` (mocking API call)

### Implementation for User Story 1

- [ ] T012 [US1] Implement `POST /tasks` API endpoint in `src/main.py` (or `src/api/tasks.py` if structure is further modularized) that calls `task_tools.add_task`.
- [ ] T013 [US1] Integrate `add_task` tool with agent's core in `src/agent/main.py` (mock agent interaction logic initially).

---

## Phase 4: User Story 2 - Task Listing & Filtering (P1)

**Goal**: Enable the AI agent to list and filter tasks based on natural language input.

**Independent Test**: The agent can list all tasks and filter them by status ('open', 'completed').

### Tests for User Story 2

- [ ] T014 [US2] Integration test for `GET /tasks` API endpoint (including `status` filter) in `tests/integration/test_task_api.py`
- [ ] T015 [P] [US2] Unit test for agent's `list_tasks` tool invocation logic in `tests/unit/test_agent_tools.py`

### Implementation for User Story 2

- [ ] T016 [US2] Implement `GET /tasks` API endpoint in `src/main.py` (or `src/api/tasks.py`) that calls `task_tools.list_tasks`.
- [ ] T017 [US2] Integrate `list_tasks` tool with agent's core in `src/agent/main.py`.

---

## Phase 5: User Story 3 - Task Modification and Completion (P2)

**Goal**: Enable the AI agent to update, complete, or delete tasks based on natural language input.

**Independent Test**: The agent can mark a task as complete, update its details, and delete it.

### Tests for User Story 3

- [ ] T018 [US3] Integration test for `PATCH /tasks/{task_id}` API endpoint in `tests/integration/test_task_api.py`
- [ ] T019 [US3] Integration test for `POST /tasks/{task_id}/complete` API endpoint in `tests/integration/test_task_api.py`
- [ ] T020 [US3] Integration test for `DELETE /tasks/{task_id}` API endpoint in `tests/integration/test_task_api.py`
- [ ] T021 [P] [US3] Unit test for agent's `update_task` tool invocation logic in `tests/unit/test_agent_tools.py`
- [ ] T022 [P] [US3] Unit test for agent's `complete_task` tool invocation logic in `tests/unit/test_agent_tools.py`
- [ ] T023 [P] [US3] Unit test for agent's `delete_task` tool invocation logic in `tests/unit/test_agent_tools.py`

### Implementation for User Story 3

- [ ] T024 [US3] Implement `PATCH /tasks/{task_id}` API endpoint in `src/main.py` (or `src/api/tasks.py`) that calls `task_tools.update_task`.
- [ ] T025 [US3] Implement `POST /tasks/{task_id}/complete` API endpoint in `src/main.py` (or `src/api/tasks.py`) that calls `task_tools.complete_task`.
- [ ] T026 [US3] Implement `DELETE /tasks/{task_id}` API endpoint in `src/main.py` (or `src/api/tasks.py`) that calls `task_tools.delete_task`.
- [ ] T027 [US3] Integrate `update_task` tool with agent's core in `src/agent/main.py`.
- [ ] T028 [US3] Integrate `complete_task` tool with agent's core in `src/agent/main.py`.
- [ ] T029 [US3] Integrate `delete_task` tool with agent's core in `src/agent/main.py`.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and general system hardening.

- [ ] T030 Implement FastAPI exception handlers for common errors (e.g., `TaskNotFound`).
- [ ] T031 Configure structured logging for the FastAPI application in `src/main.py`.
- [ ] T032 Update documentation (e.g., `README.md`, `quickstart.md`) with usage instructions for the new API.
- [ ] T033 Integrate with actual MCP SDK / OpenAI Agents SDK for real agent-tool interaction.
- [ ] T034 Review and refine agent confirmation logic in `src/agent/main.py` for clarity and user experience.
- [ ] T035 Overall code cleanup, refactoring, and linting.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion.
  - User Stories (Phase 3, 4, 5) can proceed sequentially in priority order (P1 -> P1 -> P2).
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation.
- `Task` models before `task_service`.
- `task_tools` before API endpoints.
- API endpoints before agent integration logic.

### Parallel Opportunities

- All Setup tasks (Phase 1) are marked `[P]` if independent.
- Unit tests within a user story phase are marked `[P]`.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready.
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3. Add User Story 2 → Test independently → Deploy/Demo.
4. Add User Story 3 → Test independently → Deploy/Demo.
5. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together.
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently.

---
