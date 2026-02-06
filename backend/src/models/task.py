"""Task SQLModel definition."""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, DateTime, Index
from sqlalchemy.sql import func
from src.models import TaskStatus, TaskPriority


class Task(SQLModel, table=True):
    """Task model for todo items."""

    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING, nullable=False)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, nullable=False)
    user_id: str = Field(max_length=255, nullable=False, index=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    __table_args__ = (
        Index("idx_task_user_id", "user_id"),
        Index("idx_task_status", "status"),
        Index("idx_task_created_at", "created_at"),
    )