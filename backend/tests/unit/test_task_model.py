"""Unit tests for Task model validation."""

import pytest
from datetime import datetime
from sqlmodel import Session
from src.models.task import Task
from src.models import TaskStatus, TaskPriority


def test_task_model_creation(session: Session):
    """Test Task model can be created with valid data."""
    task = Task(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.HIGH,
        user_id="test-user-123"
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.HIGH
    assert task.user_id == "test-user-123"
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_model_enum_constraints(session: Session):
    """Test Task model enforces enum constraints."""
    # Valid enum values should work
    task = Task(
        title="Test",
        status=TaskStatus.IN_PROGRESS,
        priority=TaskPriority.LOW,
        user_id="test-user"
    )
    session.add(task)
    session.commit()
    assert task.status == TaskStatus.IN_PROGRESS
    assert task.priority == TaskPriority.LOW


def test_task_model_required_fields(session: Session):
    """Test Task model enforces required fields at database level."""
    # Task with missing title should fail validation
    task_no_title = Task(
        user_id="test-user"
    )

    session.add(task_no_title)
    with pytest.raises(Exception):  # Will raise when committing to DB
        session.commit()

    session.rollback()

    # Task with missing user_id should fail validation
    task_no_user = Task(
        title="No user_id"
    )

    session.add(task_no_user)
    with pytest.raises(Exception):  # Will raise when committing to DB
        session.commit()


def test_task_model_default_values(session: Session):
    """Test Task model applies default values."""
    task = Task(
        title="Test Task",
        user_id="test-user"
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    # Check defaults
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
    assert task.description is None
    assert task.created_at is not None
    assert task.updated_at is not None
