from typing import List, Optional, Dict
from models import Task, TaskCreate, TaskUpdate, TaskStatus

class TaskService:
    """Business logic for Task operations with in-memory storage"""
    
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
    
    def create_task(self, task_data: TaskCreate) -> Task:
        """Create a new task"""
        task = Task(
            id=self._next_id,
            title=task_data.title,
            description=task_data.description,
            status="pending"
        )
        
        self._tasks[self._next_id] = task
        self._next_id += 1
        
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID"""
        return self._tasks.get(task_id)
    
    def list_tasks(self) -> List[Task]:
        """List all tasks"""
        return list(self._tasks.values())
    
    def update_task(self, task_id: int, updates: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        # Update fields if provided
        update_data = updates.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(task, field, value)
        
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# Global service instance
task_service = TaskService()