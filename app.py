import os
import sys
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

# Ensure local imports work when running from different directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from config import settings
from models import (
    Todo, TodoCreate, TodoUpdate, TodoList, 
    HealthResponse, ErrorResponse, TodoStatus, TodoPriority
)
from todo_service import todo_service

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(),
        version=settings.app_version
    )

# Todo endpoints
@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED, tags=["Todos"])
def create_todo(todo_data: TodoCreate):
    """Create a new todo"""
    try:
        todo = todo_service.create_todo(todo_data)
        return todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create todo: {str(e)}"
        )

@app.get("/todos", response_model=TodoList, tags=["Todos"])
def list_todos(
    status_filter: Optional[TodoStatus] = Query(None, alias="status", description="Filter by status"),
    priority_filter: Optional[TodoPriority] = Query(None, alias="priority", description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title and description")
):
    """List all todos with optional filters"""
    try:
        todos = todo_service.list_todos(
            status=status_filter,
            priority=priority_filter,
            search=search
        )
        return TodoList(todos=todos, total=len(todos))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve todos: {str(e)}"
        )

@app.delete("/todos/completed", tags=["Todos"])
def clear_completed_todos():
    """Delete all completed todos"""
    deleted_count = todo_service.clear_completed()
    return {"message": f"Deleted {deleted_count} completed todos"}

@app.get("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    todo = todo_service.get_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

@app.put("/todos/{todo_id}", response_model=Todo, tags=["Todos"])
def update_todo(todo_id: int, updates: TodoUpdate):
    """Update an existing todo"""
    todo = todo_service.update_todo(todo_id, updates)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todos"])
def delete_todo(todo_id: int):
    """Delete a todo"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )

@app.patch("/todos/{todo_id}/complete", response_model=Todo, tags=["Todos"])
def mark_todo_completed(todo_id: int):
    """Mark a todo as completed"""
    todo = todo_service.mark_completed(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

@app.get("/stats", tags=["Stats"])
def get_todo_stats():
    """Get todo statistics"""
    return todo_service.get_stats()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )