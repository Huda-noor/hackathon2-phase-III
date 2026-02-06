"""
Agent main module for MCP Agent Tools.
Handles the core agent logic and integrates with the task tools.
"""
from typing import Dict, Any
from src.tools import task_tools


class MCPTaskAgent:
    """
    MCP Task Agent that handles natural language commands and maps them to task tools.
    """
    
    def __init__(self):
        """Initialize the agent with available tools."""
        self.tools = {
            'add_task': task_tools.add_task,
            'list_tasks': task_tools.list_tasks,
            'update_task': task_tools.update_task,
            'complete_task': task_tools.complete_task,
            'delete_task': task_tools.delete_task
        }
    
    def process_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a natural language command and map it to the appropriate tool.
        
        Args:
            command: The command to execute (e.g., 'add_task', 'list_tasks')
            params: Parameters for the command
            
        Returns:
            Result of the command execution
        """
        if command not in self.tools:
            return {
                "error": f"Unknown command: {command}",
                "available_commands": list(self.tools.keys())
            }
        
        try:
            # Get the tool function
            tool_func = self.tools[command]
            
            # Execute the tool with provided parameters
            result = tool_func(**params)
            
            return {
                "success": True,
                "result": result,
                "command": command
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def add_task(self, title: str, description: str = None) -> Dict[str, Any]:
        """Add a new task."""
        return self.process_command('add_task', {'title': title, 'description': description})
    
    def list_tasks(self, status: str = None) -> Dict[str, Any]:
        """List tasks with optional status filter."""
        return self.process_command('list_tasks', {'status': status})
    
    def update_task(self, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update an existing task."""
        return self.process_command('update_task', {
            'task_id': task_id,
            'title': title,
            'description': description
        })
    
    def complete_task(self, task_id: int) -> Dict[str, Any]:
        """Complete a task."""
        return self.process_command('complete_task', {'task_id': task_id})
    
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        return self.process_command('delete_task', {'task_id': task_id})


# Global agent instance for simple access
agent = MCPTaskAgent()


def handle_user_input(user_input: str) -> Dict[str, Any]:
    """
    Simple function to handle user input and determine the appropriate action.
    This is a simplified version - in a real implementation, this would use
    NLP to parse the user's intent.
    
    Args:
        user_input: Natural language input from the user
        
    Returns:
        Result of processing the user's request
    """
    # This is a simplified parser - in reality, you'd use more sophisticated NLP
    user_input_lower = user_input.lower().strip()
    
    if user_input_lower.startswith("add task:") or user_input_lower.startswith("create task:"):
        # Extract title and description
        parts = user_input.split(":", 1)
        if len(parts) > 1:
            task_details = parts[1].strip()
            title_desc = task_details.split(" - ", 1)
            title = title_desc[0].strip()
            description = title_desc[1].strip() if len(title_desc) > 1 else None
            return agent.add_task(title, description)
        else:
            return {"error": "Invalid format. Use 'add task: title - description'"}
    
    elif user_input_lower.startswith("list tasks"):
        # Check if there's a status filter
        if "open" in user_input_lower:
            return agent.list_tasks(status="open")
        elif "completed" in user_input_lower:
            return agent.list_tasks(status="completed")
        else:
            return agent.list_tasks()
    
    elif user_input_lower.startswith("complete task"):
        # Extract task ID
        try:
            task_id_str = user_input.split(" ")[2]  # "complete task 123"
            task_id = int(task_id_str)
            return agent.complete_task(task_id)
        except (ValueError, IndexError):
            return {"error": "Invalid format. Use 'complete task 123'"}
    
    elif user_input_lower.startswith("delete task"):
        # Extract task ID
        try:
            task_id_str = user_input.split(" ")[2]  # "delete task 123"
            task_id = int(task_id_str)
            return agent.delete_task(task_id)
        except (ValueError, IndexError):
            return {"error": "Invalid format. Use 'delete task 123'"}
    
    else:
        return {"error": f"Unknown command: {user_input}. Available commands: add task, list tasks, complete task, delete task"}