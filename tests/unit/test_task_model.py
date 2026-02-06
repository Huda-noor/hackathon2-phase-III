"""
Unit test for Task Pydantic model validation.
"""
import pytest
from src.services.task_models import Task, TaskCreate


def test_task_creation():
    """Test creating a valid Task object."""
    task = Task(id=1, title="Test Task", description="Test Description", status="open")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "open"


def test_task_with_defaults():
    """Test creating a Task with default status."""
    task = Task(id=1, title="Test Task", description="Test Description")
    
    assert task.status == "open"


def test_task_create_model():
    """Test creating a TaskCreate object."""
    task_create = TaskCreate(title="New Task", description="New Description")
    
    assert task_create.title == "New Task"
    assert task_create.description == "New Description"


def test_task_validation():
    """Test that Task model validates correctly."""
    # Test that required fields are validated
    with pytest.raises(ValueError):
        Task(id=1, title="", description="Test", status="open")  # Empty title should fail validation