from typing import Any, Dict
from ..core.mcp_tools import execute_mcp_tool


class ToolExecutionService:
    """
    Service responsible for executing MCP tools as directed by the AI agent.
    """
    
    @staticmethod
    async def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool with the provided arguments.
        """
        try:
            # Execute the tool using the MCP tools interface
            result = await execute_mcp_tool(tool_name, arguments)
            return {
                "success": True,
                "result": result,
                "tool_name": tool_name,
                "arguments": arguments
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name,
                "arguments": arguments
            }
    
    @staticmethod
    async def validate_tool_call(tool_name: str, arguments: Dict[str, Any]) -> bool:
        """
        Validate that a tool call is properly formed before execution.
        """
        # Check if the tool name is valid
        if not isinstance(tool_name, str) or not tool_name.strip():
            return False
        
        # Check if arguments is a dictionary
        if not isinstance(arguments, dict):
            return False
        
        # Additional validation could be performed here based on known tools
        # For now, we'll just return True
        return True
    
    @staticmethod
    async def execute_multiple_tools(tool_calls: list) -> list:
        """
        Execute multiple tools in sequence.
        """
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.get("tool_name")
            arguments = tool_call.get("arguments", {})
            
            # Validate the tool call
            is_valid = await ToolExecutionService.validate_tool_call(tool_name, arguments)
            if not is_valid:
                results.append({
                    "success": False,
                    "error": "Invalid tool call",
                    "tool_name": tool_name,
                    "arguments": arguments
                })
                continue
            
            # Execute the tool
            result = await ToolExecutionService.execute_tool(tool_name, arguments)
            results.append(result)
        
        return results