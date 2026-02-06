"""
Task Pydantic models for the MCP Agent Tools.
Based on the data-model.md specification and OpenAPI contract.
"""
from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    """Base class for Task with common fields."""
    title: str
    description: Optional[str] = None


class Task(TaskBase):
    """Task model with ID and status."""
    id: int
    status: str = "open"


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Model for updating an existing task."""
    title: Optional[str] = None
    description: Optional[str] = None