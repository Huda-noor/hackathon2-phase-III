"""Task CRUD API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session

from src.models.task import Task
from src.models import TaskStatus
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.api.deps import get_db
from src.core.auth import get_current_user


router = APIRouter()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Create a new task for the authenticated user."""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        user_id=user_id
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[TaskStatus] = None,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """List all tasks for the authenticated user with optional filtering."""
    query = select(Task).where(Task.user_id == user_id)

    if status_filter:
        query = query.where(Task.status == status_filter)

    query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())

    result = session.exec(query)
    tasks = result.all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Get a specific task by ID."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Update a task."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a task."""
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )

    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    session.delete(task)
    session.commit()
