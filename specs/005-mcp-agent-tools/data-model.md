# Data Model: MCP Tools & Agent Intelligence

**Purpose**: Defines the core data entities for the task management feature.

## Entity: Task

Represents a single to-do item.

### Fields

| Field         | Type   | Description                                     | Constraints / Validation Rules           |
|---------------|--------|-------------------------------------------------|------------------------------------------|
| `id`          | `int`  | The unique identifier for the task.             | Required, Primary Key, Auto-incrementing |
| `title`       | `str`  | The main description of the task.               | Required, Non-empty string               |
| `description` | `str`  | A more detailed description of the task.        | Optional, Can be empty                   |
| `status`      | `str`  | The current state of the task.                  | Required, Must be one of: 'open', 'completed' |

### State Transitions

The `status` field can transition as follows:

- **Initial State**: `open`
- **Allowed Transitions**:
  - `open` -> `completed` (via the `complete_task` tool)

No other transitions are permitted. For example, a task cannot go from `completed` back to `open` within the scope of this feature.
