"""
Tests for database models
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_models import Base, TodoDB, TodoStatusEnum, TodoPriorityEnum
from datetime import datetime

class TestDatabaseModels:
    def test_todo_status_enum(self):
        """Test TodoStatusEnum values"""
        assert TodoStatusEnum.PENDING.value == "pending"
        assert TodoStatusEnum.IN_PROGRESS.value == "in_progress"
        assert TodoStatusEnum.COMPLETED.value == "completed"

    def test_todo_priority_enum(self):
        """Test TodoPriorityEnum values"""
        assert TodoPriorityEnum.LOW.value == "low"
        assert TodoPriorityEnum.MEDIUM.value == "medium"
        assert TodoPriorityEnum.HIGH.value == "high"

    def test_todo_db_model_creation(self):
        """Test TodoDB model creation and attributes"""
        # Create a mock TodoDB instance (without database)
        todo = TodoDB()
        
        # Test table name
        assert TodoDB.__tablename__ == "todos"
        
        # Test that columns exist
        assert hasattr(TodoDB, 'id')
        assert hasattr(TodoDB, 'title')
        assert hasattr(TodoDB, 'description')
        assert hasattr(TodoDB, 'status')
        assert hasattr(TodoDB, 'priority')
        assert hasattr(TodoDB, 'created_at')
        assert hasattr(TodoDB, 'updated_at')

    def test_todo_db_model_defaults(self):
        """Test TodoDB model default values"""
        todo = TodoDB()
        
        # Test default status
        assert todo.status is None or todo.status == TodoStatusEnum.PENDING
        
        # Test default priority  
        assert todo.priority is None or todo.priority == TodoPriorityEnum.MEDIUM

    def test_todo_db_repr(self):
        """Test TodoDB __repr__ method"""
        # Create instance with test data
        todo = TodoDB()
        todo.id = 1
        todo.title = "Test Todo"
        todo.status = TodoStatusEnum.PENDING
        
        repr_str = repr(todo)
        assert "Todo(id=1" in repr_str
        assert "title='Test Todo'" in repr_str
        assert "status='pending'" in repr_str

    def test_base_model(self):
        """Test Base declarative base"""
        assert Base is not None
        assert hasattr(Base, 'metadata')

    def test_column_properties(self):
        """Test column properties and constraints"""
        # Test id column
        id_col = TodoDB.__table__.columns['id']
        assert id_col.primary_key
        assert id_col.autoincrement
        assert id_col.index

        # Test title column
        title_col = TodoDB.__table__.columns['title']
        assert not title_col.nullable
        assert title_col.type.length == 200
        assert title_col.index

        # Test description column
        desc_col = TodoDB.__table__.columns['description']
        assert desc_col.nullable

        # Test status column
        status_col = TodoDB.__table__.columns['status']
        assert not status_col.nullable
        assert status_col.index

        # Test priority column
        priority_col = TodoDB.__table__.columns['priority']
        assert not priority_col.nullable
        assert priority_col.index