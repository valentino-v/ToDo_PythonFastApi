"""
Tests for the TodoService business logic
"""
import pytest
from datetime import datetime
from todo_service import TodoService
from models import TodoCreate, TodoUpdate

class TestTodoService:
    
    def test_create_todo(self, clean_service):
        """Test creating a new todo"""
        service = clean_service
        todo_data = TodoCreate(
            title="Test Todo",
            description="Test Description",
            priority="high"
        )
        
        todo = service.create_todo(todo_data)
        
        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.status == "pending"
        assert todo.priority == "high"
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)
    
    def test_get_todo_exists(self, clean_service):
        """Test getting an existing todo"""
        service = clean_service
        todo_data = TodoCreate(title="Test Todo")
        created_todo = service.create_todo(todo_data)
        
        retrieved_todo = service.get_todo(created_todo.id)
        
        assert retrieved_todo is not None
        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == created_todo.title
    
    def test_get_todo_not_exists(self, clean_service):
        """Test getting a non-existent todo"""
        service = clean_service
        
        todo = service.get_todo(999)
        
        assert todo is None
    
    def test_list_todos_empty(self, clean_service):
        """Test listing todos when none exist"""
        service = clean_service
        
        todos = service.list_todos()
        
        assert todos == []
    
    def test_list_todos_with_data(self, clean_service):
        """Test listing todos with data"""
        service = clean_service
        
        # Create multiple todos
        todo1 = service.create_todo(TodoCreate(title="Todo 1", priority="high"))
        todo2 = service.create_todo(TodoCreate(title="Todo 2", priority="low"))
        
        todos = service.list_todos()
        
        assert len(todos) == 2
        # Should be sorted by created_at (newest first)
        assert todos[0].id == todo2.id  # todo2 was created last
        assert todos[1].id == todo1.id
    
    def test_list_todos_filter_by_status(self, clean_service):
        """Test filtering todos by status"""
        service = clean_service
        
        todo1 = service.create_todo(TodoCreate(title="Todo 1"))
        todo2 = service.create_todo(TodoCreate(title="Todo 2"))
        
        # Mark one as completed
        service.mark_completed(todo1.id)
        
        # Filter by pending
        pending_todos = service.list_todos(status="pending")
        assert len(pending_todos) == 1
        assert pending_todos[0].id == todo2.id
        
        # Filter by completed
        completed_todos = service.list_todos(status="completed")
        assert len(completed_todos) == 1
        assert completed_todos[0].id == todo1.id
    
    def test_list_todos_filter_by_priority(self, clean_service):
        """Test filtering todos by priority"""
        service = clean_service
        
        service.create_todo(TodoCreate(title="High Priority", priority="high"))
        service.create_todo(TodoCreate(title="Low Priority", priority="low"))
        
        high_todos = service.list_todos(priority="high")
        assert len(high_todos) == 1
        assert high_todos[0].title == "High Priority"
    
    def test_list_todos_search(self, clean_service):
        """Test searching todos"""
        service = clean_service
        
        service.create_todo(TodoCreate(title="Python Project", description="FastAPI development"))
        service.create_todo(TodoCreate(title="Java Project", description="Spring Boot app"))
        
        # Search in title
        python_todos = service.list_todos(search="Python")
        assert len(python_todos) == 1
        assert python_todos[0].title == "Python Project"
        
        # Search in description
        fastapi_todos = service.list_todos(search="FastAPI")
        assert len(fastapi_todos) == 1
        assert fastapi_todos[0].title == "Python Project"
    
    def test_update_todo_exists(self, clean_service):
        """Test updating an existing todo"""
        service = clean_service
        todo = service.create_todo(TodoCreate(title="Original Title"))
        original_updated_at = todo.updated_at
        
        updates = TodoUpdate(
            title="Updated Title",
            description="New description",
            status="in_progress"
        )
        
        updated_todo = service.update_todo(todo.id, updates)
        
        assert updated_todo is not None
        assert updated_todo.title == "Updated Title"
        assert updated_todo.description == "New description"
        assert updated_todo.status == "in_progress"
        assert updated_todo.updated_at > original_updated_at
    
    def test_update_todo_not_exists(self, clean_service):
        """Test updating a non-existent todo"""
        service = clean_service
        updates = TodoUpdate(title="Updated Title")
        
        result = service.update_todo(999, updates)
        
        assert result is None
    
    def test_delete_todo_exists(self, clean_service):
        """Test deleting an existing todo"""
        service = clean_service
        todo = service.create_todo(TodoCreate(title="To Delete"))
        
        success = service.delete_todo(todo.id)
        
        assert success is True
        assert service.get_todo(todo.id) is None
    
    def test_delete_todo_not_exists(self, clean_service):
        """Test deleting a non-existent todo"""
        service = clean_service
        
        success = service.delete_todo(999)
        
        assert success is False
    
    def test_mark_completed(self, clean_service):
        """Test marking a todo as completed"""
        service = clean_service
        todo = service.create_todo(TodoCreate(title="To Complete"))
        
        completed_todo = service.mark_completed(todo.id)
        
        assert completed_todo is not None
        assert completed_todo.status == "completed"
    
    def test_mark_completed_not_exists(self, clean_service):
        """Test marking a non-existent todo as completed"""
        service = clean_service
        
        result = service.mark_completed(999)
        
        assert result is None
    
    def test_clear_completed(self, clean_service):
        """Test clearing completed todos"""
        service = clean_service
        
        # Create todos
        todo1 = service.create_todo(TodoCreate(title="Todo 1"))
        todo2 = service.create_todo(TodoCreate(title="Todo 2"))
        todo3 = service.create_todo(TodoCreate(title="Todo 3"))
        
        # Mark some as completed
        service.mark_completed(todo1.id)
        service.mark_completed(todo3.id)
        
        # Clear completed
        deleted_count = service.clear_completed()
        
        assert deleted_count == 2
        assert service.get_todo(todo1.id) is None
        assert service.get_todo(todo2.id) is not None  # Should still exist
        assert service.get_todo(todo3.id) is None
    
    def test_get_stats_empty(self, clean_service):
        """Test getting stats with no todos"""
        service = clean_service
        
        stats = service.get_stats()
        
        expected = {
            "total": 0,
            "by_status": {"pending": 0, "in_progress": 0, "completed": 0},
            "by_priority": {"low": 0, "medium": 0, "high": 0}
        }
        assert stats == expected
    
    def test_get_stats_with_data(self, clean_service):
        """Test getting stats with todos"""
        service = clean_service
        
        # Create todos with different statuses and priorities
        service.create_todo(TodoCreate(title="Todo 1", priority="high"))
        service.create_todo(TodoCreate(title="Todo 2", priority="medium"))
        todo3 = service.create_todo(TodoCreate(title="Todo 3", priority="low"))
        
        # Change some statuses
        service.mark_completed(todo3.id)
        
        stats = service.get_stats()
        
        assert stats["total"] == 3
        assert stats["by_status"]["pending"] == 2
        assert stats["by_status"]["completed"] == 1
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["medium"] == 1
        assert stats["by_priority"]["low"] == 1