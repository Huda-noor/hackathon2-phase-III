"""
Task service layer with in-memory storage for MCP Agent Tools.
Implements CRUD operations for Task objects.
"""
from typing import List, Optional, Dict
from .task_models import Task, TaskCreate, TaskUpdate


# In-memory storage for tasks
_tasks_db: Dict[int, Task] = {}
_next_id = 1


def reset_task_store():
    """Reset the in-memory task store. Useful for testing."""
    global _tasks_db, _next_id
    _tasks_db.clear()
    _next_id = 1


def create_task(task_data: TaskCreate) -> Task:
    """Create a new task with auto-generated ID."""
    global _next_id
    
    task = Task(
        id=_next_id,
        title=task_data.title,
        description=task_data.description,
        status="open"
    )
    
    _tasks_db[_next_id] = task
    _next_id += 1
    
    return task


def get_tasks(status: Optional[str] = None) -> List[Task]:
    """Get all tasks, optionally filtered by status."""
    tasks = list(_tasks_db.values())
    
    if status:
        tasks = [task for task in tasks if task.status == status]
    
    return tasks


def get_task(task_id: int) -> Optional[Task]:
    """Get a specific task by ID."""
    return _tasks_db.get(task_id)


def update_task(task_id: int, task_data: TaskUpdate) -> Optional[Task]:
    """Update an existing task."""
    task = _tasks_db.get(task_id)
    if not task:
        return None
    
    # Convert to dict to allow updates
    task_dict = task.model_dump()
    
    # Update with provided values
    if task_data.title is not None:
        task_dict['title'] = task_data.title
    if task_data.description is not None:
        task_dict['description'] = task_data.description
    
    # Create updated task
    updated_task = Task(**task_dict)
    _tasks_db[task_id] = updated_task
    
    return updated_task


def complete_task(task_id: int) -> Optional[Task]:
    """Mark a task as completed."""
    task = _tasks_db.get(task_id)
    if not task:
        return None
    
    # Update status to completed
    task_dict = task.model_dump()
    task_dict['status'] = 'completed'
    
    completed_task = Task(**task_dict)
    _tasks_db[task_id] = completed_task
    
    return completed_task


def delete_task(task_id: int) -> bool:
    """Delete a task by ID."""
    if task_id in _tasks_db:
        del _tasks_db[task_id]
        return True
    return False