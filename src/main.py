"""
Main FastAPI application for MCP Agent Tools.
"""
from fastapi import FastAPI, HTTPException
from typing import Optional

from src.services.task_models import Task, TaskCreate
from src.tools.task_tools import (
    add_task as add_task_tool,
    list_tasks as list_tasks_tool,
    update_task as update_task_tool,
    complete_task as complete_task_tool,
    delete_task as delete_task_tool
)


app = FastAPI(
    title="MCP Task Tools API",
    description="API endpoints that represent the tools available to the AI agent for task management.",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {"message": "Welcome to MCP Agent Tools API"}


@app.get("/tasks")
async def get_tasks(status: Optional[str] = None):
    """List tasks (list_tasks tool)"""
    return list_tasks_tool(status=status)


@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    """Create a task (add_task tool)"""
    return add_task_tool(title=task.title, description=task.description)


@app.patch("/tasks/{task_id}")
async def patch_task(task_id: int, task_update: dict):
    """Update a task (update_task tool)"""
    # Extract title and description from the request body
    title = task_update.get('title')
    description = task_update.get('description')
    
    updated_task = update_task_tool(task_id, title=title, description=description)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task_endpoint(task_id: int):
    """Delete a task (delete_task tool)"""
    success = delete_task_tool(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {}


@app.post("/tasks/{task_id}/complete")
async def complete_task_endpoint(task_id: int):
    """Complete a task (complete_task tool)"""
    completed_task = complete_task_tool(task_id)
    if not completed_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return completed_task


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)