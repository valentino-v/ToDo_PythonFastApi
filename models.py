from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict

# Status and Priority enums
TodoStatus = Literal["pending", "in_progress", "completed"]
TodoPriority = Literal["low", "medium", "high"]

class TodoCreate(BaseModel):
    """Schema for creating a new todo"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API documentation",
                "priority": "high"
            }
        }
    )
    
    title: str = Field(..., min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    priority: TodoPriority = Field(default="medium", description="Todo priority level")

class TodoUpdate(BaseModel):
    """Schema for updating an existing todo"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated project documentation",
                "description": "Write comprehensive README, API documentation, and deployment guide",
                "status": "in_progress",
                "priority": "high"
            }
        }
    )
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Todo title")
    description: Optional[str] = Field(None, max_length=1000, description="Todo description")
    status: Optional[TodoStatus] = Field(None, description="Todo status")
    priority: Optional[TodoPriority] = Field(None, description="Todo priority level")

class Todo(BaseModel):
    """Complete Todo model"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API documentation",
                "status": "pending",
                "priority": "high",
                "created_at": "2025-10-07T10:00:00",
                "updated_at": "2025-10-07T10:00:00"
            }
        }
    )
    
    id: int = Field(..., description="Unique todo identifier")
    title: str = Field(..., description="Todo title")
    description: Optional[str] = Field(None, description="Todo description")
    status: TodoStatus = Field(default="pending", description="Todo status")
    priority: TodoPriority = Field(default="medium", description="Todo priority level")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class TodoList(BaseModel):
    """Response model for todo lists"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "todos": [
                    {
                        "id": 1,
                        "title": "Complete project documentation",
                        "description": "Write comprehensive README and API documentation",
                        "status": "pending",
                        "priority": "high",
                        "created_at": "2025-10-07T10:00:00",
                        "updated_at": "2025-10-07T10:00:00"
                    }
                ],
                "total": 1
            }
        }
    )
    
    todos: List[Todo]
    total: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "ok"
    timestamp: datetime
    version: str
    
class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime