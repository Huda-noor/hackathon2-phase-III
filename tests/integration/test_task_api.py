"""
Integration test for add_task API endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.services.task_service import reset_task_store


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the in-memory database before each test."""
    reset_task_store()
    yield
    reset_task_store()  # Clean up after test


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_add_task_success(client):
    """Test successfully adding a new task."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "open"
    assert "id" in data
    assert isinstance(data["id"], int)


def test_add_task_without_description(client):
    """Test adding a task without a description."""
    task_data = {
        "title": "Test Task Without Description"
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task Without Description"
    assert data["description"] is None
    assert data["status"] == "open"
    assert "id" in data


def test_list_tasks_initially_empty(client):
    """Test that the task list is initially empty."""
    response = client.get("/tasks")
    
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_list_tasks_with_status_filter(client):
    """Test filtering tasks by status."""
    # Add a task
    task_data = {
        "title": "Open Task",
        "description": "An open task"
    }
    client.post("/tasks", json=task_data)
    
    # Complete another task
    task_data_completed = {
        "title": "Completed Task",
        "description": "A completed task"
    }
    response = client.post("/tasks", json=task_data_completed)
    task_id = response.json()["id"]
    
    # Complete the task
    client.post(f"/tasks/{task_id}/complete")
    
    # Test filtering for open tasks
    response = client.get("/tasks?status=open")
    open_tasks = response.json()
    assert len(open_tasks) == 1
    assert open_tasks[0]["status"] == "open"
    
    # Test filtering for completed tasks
    response = client.get("/tasks?status=completed")
    completed_tasks = response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["status"] == "completed"