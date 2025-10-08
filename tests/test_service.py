"""
Tests for the TaskService business logic
"""
import pytest
from todo_service import TaskService
from models import TaskCreate, TaskUpdate

class TestTaskService:
    
    def test_create_task(self, clean_service):
        """Test creating a new task"""
        service = clean_service
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description"
        )
        
        task = service.create_task(task_data)
        
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == "pending"
    
    def test_get_task_exists(self, clean_service):
        """Test getting an existing task"""
        service = clean_service
        task_data = TaskCreate(title="Test Task")
        created_task = service.create_task(task_data)
        
        retrieved_task = service.get_task(created_task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id
        assert retrieved_task.title == created_task.title
    
    def test_get_task_not_exists(self, clean_service):
        """Test getting a non-existent task"""
        service = clean_service
        
        task = service.get_task(999)
        
        assert task is None
    
    def test_list_tasks_empty(self, clean_service):
        """Test listing tasks when none exist"""
        service = clean_service
        
        tasks = service.list_tasks()
        
        assert tasks == []
    
    def test_list_tasks_with_data(self, clean_service):
        """Test listing tasks with data"""
        service = clean_service
        
        # Create multiple tasks
        task1 = service.create_task(TaskCreate(title="Task 1"))
        task2 = service.create_task(TaskCreate(title="Task 2"))
        
        tasks = service.list_tasks()
        
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks
    
    def test_update_task_exists(self, clean_service):
        """Test updating an existing task"""
        service = clean_service
        task = service.create_task(TaskCreate(title="Original Title"))
        
        updates = TaskUpdate(
            title="Updated Title",
            description="New description",
            status="in_progress"
        )
        
        updated_task = service.update_task(task.id, updates)
        
        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "New description"
        assert updated_task.status == "in_progress"
    
    def test_update_task_not_exists(self, clean_service):
        """Test updating a non-existent task"""
        service = clean_service
        updates = TaskUpdate(title="Updated Title")
        
        result = service.update_task(999, updates)
        
        assert result is None
    
    def test_delete_task_exists(self, clean_service):
        """Test deleting an existing task"""
        service = clean_service
        task = service.create_task(TaskCreate(title="To Delete"))
        
        success = service.delete_task(task.id)
        
        assert success is True
        assert service.get_task(task.id) is None
    
    def test_delete_task_not_exists(self, clean_service):
        """Test deleting a non-existent task"""
        service = clean_service
        
        success = service.delete_task(999)
        
        assert success is False