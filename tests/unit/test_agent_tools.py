"""
Unit test for agent's tool invocation logic.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.tools import task_tools


def test_add_task_tool_invocation():
    """Test the add_task tool invocation logic."""
    with patch('src.services.task_service.create_task') as mock_create:
        # Mock the return value
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.status = "open"
        mock_create.return_value = mock_task
        
        # Call the tool function
        result = task_tools.add_task("Test Task", "Test Description")
        
        # Verify the service was called correctly
        assert mock_create.called
        assert result.id == 1
        assert result.title == "Test Task"
        assert result.description == "Test Description"


def test_list_tasks_tool_invocation():
    """Test the list_tasks tool invocation logic."""
    with patch('src.services.task_service.get_tasks') as mock_get:
        # Mock the return value
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Test Task"
        mock_task.description = "Test Description"
        mock_task.status = "open"
        mock_get.return_value = [mock_task]
        
        # Call the tool function
        result = task_tools.list_tasks()
        
        # Verify the service was called correctly
        mock_get.assert_called_once_with(None)
        assert len(result) == 1
        assert result[0].id == 1


def test_list_tasks_with_status_filter():
    """Test the list_tasks tool with status filter."""
    with patch('src.services.task_service.get_tasks') as mock_get:
        # Mock the return value
        mock_get.return_value = []
        
        # Call the tool function with status filter
        result = task_tools.list_tasks(status="completed")
        
        # Verify the service was called correctly
        mock_get.assert_called_once_with("completed")


def test_update_task_tool_invocation():
    """Test the update_task tool invocation logic."""
    from src.services.task_models import TaskUpdate
    
    with patch('src.services.task_service.update_task') as mock_update:
        # Mock the return value
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.title = "Updated Task"
        mock_task.description = "Updated Description"
        mock_task.status = "open"
        mock_update.return_value = mock_task
        
        # Call the tool function
        result = task_tools.update_task(1, "Updated Task", "Updated Description")
        
        # Verify the service was called correctly with TaskUpdate object
        expected_task_update = TaskUpdate(title="Updated Task", description="Updated Description")
        mock_update.assert_called_once_with(1, expected_task_update)
        assert result.id == 1


def test_complete_task_tool_invocation():
    """Test the complete_task tool invocation logic."""
    with patch('src.services.task_service.complete_task') as mock_complete:
        # Mock the return value
        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.status = "completed"
        mock_complete.return_value = mock_task
        
        # Call the tool function
        result = task_tools.complete_task(1)
        
        # Verify the service was called correctly
        mock_complete.assert_called_once_with(1)
        assert result.status == "completed"


def test_delete_task_tool_invocation():
    """Test the delete_task tool invocation logic."""
    with patch('src.services.task_service.delete_task') as mock_delete:
        # Mock the return value
        mock_delete.return_value = True
        
        # Call the tool function
        result = task_tools.delete_task(1)
        
        # Verify the service was called correctly
        mock_delete.assert_called_once_with(1)
        assert result is True