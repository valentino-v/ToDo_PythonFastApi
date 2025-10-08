from typing import Optional, List, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# Status enum simplificado
TaskStatus = Literal["pending", "in_progress", "done"]

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API documentation"
            }
        }
    )
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated project documentation",
                "description": "Write comprehensive README, API documentation, and deployment guide",
                "status": "in_progress"
            }
        }
    )
    
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")

class Task(BaseModel):
    """Complete Task model"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write comprehensive README and API documentation",
                "status": "pending"
            }
        }
    )
    
    id: int = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(default="pending", description="Task status")

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