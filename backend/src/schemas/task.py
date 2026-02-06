"""Pydantic schemas for Task API."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from src.models import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(..., max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
