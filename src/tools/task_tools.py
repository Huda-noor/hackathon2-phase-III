"""
Task tools for the MCP Agent.
These functions correspond to the API tools defined in the OpenAPI contract.
"""
from typing import List, Optional
from ..services.task_models import Task, TaskCreate, TaskUpdate
from ..services import task_service


def add_task(title: str, description: Optional[str] = None) -> Task:
    """
    Add a new task.
    
    Args:
        title: The title of the task
        description: Optional description of the task
        
    Returns:
        The created task
    """
    task_data = TaskCreate(title=title, description=description)
    return task_service.create_task(task_data)


def list_tasks(status: Optional[str] = None) -> List[Task]:
    """
    List tasks, optionally filtered by status.
    
    Args:
        status: Optional status filter ('open', 'completed')
        
    Returns:
        List of tasks matching the criteria
    """
    return task_service.get_tasks(status)


def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
    """
    Update an existing task.
    
    Args:
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        
    Returns:
        Updated task or None if not found
    """
    from ..services.task_service import update_task as service_update_task
    task_data = TaskUpdate(title=title, description=description)
    return service_update_task(task_id, task_data)


def complete_task(task_id: int) -> Optional[Task]:
    """
    Mark a task as completed.
    
    Args:
        task_id: ID of the task to complete
        
    Returns:
        Completed task or None if not found
    """
    return task_service.complete_task(task_id)


def delete_task(task_id: int) -> bool:
    """
    Delete a task.
    
    Args:
        task_id: ID of the task to delete
        
    Returns:
        True if deleted, False if not found
    """
    return task_service.delete_task(task_id)