"""Integration tests for task CRUD operations."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_task(client: TestClient, auth_headers):
    """Test creating a task with authentication."""
    response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "Test task description",
            "status": "pending",
            "priority": "high"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test task description"
    assert data["status"] == "pending"
    assert data["priority"] == "high"
    assert data["user_id"] == "test-user-123"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_tasks_user_isolation(client: TestClient, auth_headers, auth_headers_user2):
    """Test listing tasks returns only authenticated user's tasks."""
    # User 1 creates a task
    response1 = client.post(
        "/api/tasks",
        json={"title": "User 1 Task", "description": "Task by user 1"},
        headers=auth_headers
    )
    assert response1.status_code == 201

    # User 2 creates a task
    response2 = client.post(
        "/api/tasks",
        json={"title": "User 2 Task", "description": "Task by user 2"},
        headers=auth_headers_user2
    )
    assert response2.status_code == 201

    # User 1 lists tasks - should only see their own
    response = client.get("/api/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "User 1 Task"
    assert data[0]["user_id"] == "test-user-123"


def test_update_task(client: TestClient, auth_headers):
    """Test updating a task and verifying updated_at timestamp changes."""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original Title", "description": "Original description"},
        headers=auth_headers
    )
    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    original_updated_at = task["updated_at"]

    # Update task
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Title", "status": "in_progress"},
        headers=auth_headers
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Title"
    assert updated_task["status"] == "in_progress"
    assert updated_task["updated_at"] != original_updated_at


def test_delete_task(client: TestClient, auth_headers):
    """Test deleting a task."""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Task to delete", "description": "Will be deleted"},
        headers=auth_headers
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Delete task
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    # Verify task is gone
    get_response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_cross_user_access_denial(client: TestClient, auth_headers, auth_headers_user2):
    """Test User A cannot access User B's task."""
    # User 2 creates a task
    create_response = client.post(
        "/api/tasks",
        json={"title": "User 2 Private Task", "description": "Should not be accessible"},
        headers=auth_headers_user2
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User 1 attempts to access User 2's task
    get_response = client.get(f"/api/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 403

    # User 1 attempts to update User 2's task
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Hacked"},
        headers=auth_headers
    )
    assert update_response.status_code == 403

    # User 1 attempts to delete User 2's task
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=auth_headers)
    assert delete_response.status_code == 403
