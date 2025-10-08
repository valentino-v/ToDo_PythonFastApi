from datetime import datetime
from typing import List, Optional, Dict, Any
from models import Todo, TodoCreate, TodoUpdate, TodoStatus, TodoPriority

class TodoService:
    """Business logic for Todo operations with in-memory storage"""
    
    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1
    
    def create_todo(self, todo_data: TodoCreate) -> Todo:
        """Create a new todo"""
        now = datetime.now()
        
        todo = Todo(
            id=self._next_id,
            title=todo_data.title,
            description=todo_data.description,
            status="pending",
            priority=todo_data.priority,
            created_at=now,
            updated_at=now
        )
        
        self._todos[self._next_id] = todo
        self._next_id += 1
        
        return todo
    
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Get a todo by ID"""
        return self._todos.get(todo_id)
    
    def list_todos(
        self, 
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        search: Optional[str] = None
    ) -> List[Todo]:
        """List todos with optional filters"""
        todos = list(self._todos.values())
        
        # Filter by status
        if status:
            todos = [todo for todo in todos if todo.status == status]
        
        # Filter by priority
        if priority:
            todos = [todo for todo in todos if todo.priority == priority]
        
        # Search in title and description
        if search:
            search_lower = search.lower()
            todos = [
                todo for todo in todos 
                if search_lower in todo.title.lower() 
                or (todo.description and search_lower in todo.description.lower())
            ]
        
        # Sort by created_at (newest first)
        todos.sort(key=lambda x: x.created_at, reverse=True)
        
        return todos
    
    def update_todo(self, todo_id: int, updates: TodoUpdate) -> Optional[Todo]:
        """Update an existing todo"""
        todo = self._todos.get(todo_id)
        if not todo:
            return None
        
        # Update fields if provided
        update_data = updates.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(todo, field, value)
        
        # Always update the timestamp
        todo.updated_at = datetime.now()
        
        return todo
    
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo by ID"""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get todo statistics"""
        todos = list(self._todos.values())
        total = len(todos)
        
        if total == 0:
            return {
                "total": 0,
                "by_status": {"pending": 0, "in_progress": 0, "completed": 0},
                "by_priority": {"low": 0, "medium": 0, "high": 0}
            }
        
        # Count by status
        status_counts = {"pending": 0, "in_progress": 0, "completed": 0}
        for todo in todos:
            status_counts[todo.status] += 1
        
        # Count by priority
        priority_counts = {"low": 0, "medium": 0, "high": 0}
        for todo in todos:
            priority_counts[todo.priority] += 1
        
        return {
            "total": total,
            "by_status": status_counts,
            "by_priority": priority_counts
        }
    
    def mark_completed(self, todo_id: int) -> Optional[Todo]:
        """Mark a todo as completed"""
        todo = self._todos.get(todo_id)
        if not todo:
            return None
        
        todo.status = "completed"
        todo.updated_at = datetime.now()
        
        return todo
    
    def clear_completed(self) -> int:
        """Delete all completed todos and return count of deleted items"""
        completed_ids = [
            todo_id for todo_id, todo in self._todos.items() 
            if todo.status == "completed"
        ]
        
        for todo_id in completed_ids:
            del self._todos[todo_id]
        
        return len(completed_ids)

# Global service instance
todo_service = TodoService()