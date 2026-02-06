# Quickstart: MCP Task Tools

This guide provides a brief overview of how to interact with the MCP Task Tools API.

## Base URL

All API endpoints are relative to a base URL, which will be provided upon deployment. For local testing, this is likely `http://127.0.0.1:8000`.

## Tools as API Endpoints

### 1. Create a Task (`add_task`)

Create a new task by sending a POST request to `/tasks`.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/tasks" 
-H "Content-Type: application/json" 
-d '{
  "title": "Buy milk",
  "description": "Get 2% milk from the store"
}'
```

### 2. List Tasks (`list_tasks`)

Retrieve a list of your tasks. By default, it returns 'open' tasks.

**Example (Open Tasks):**
```bash
curl -X GET "http://127.0.0.1:8000/tasks"
```

**Example (Completed Tasks):**
```bash
curl -X GET "http://127.0.0.1:8000/tasks?status=completed"
```

### 3. Update a Task (`update_task`)

Modify the title or description of a task. You need the `task_id` (e.g., 1).

**Example:**
```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1" 
-H "Content-Type: application/json" 
-d '{
  "title": "Buy almond milk"
}'
```

### 4. Complete a Task (`complete_task`)

Mark a task as complete.

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/tasks/1/complete"
```

### 5. Delete a Task (`delete_task`)

Permanently remove a task.

**Example:**
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```
