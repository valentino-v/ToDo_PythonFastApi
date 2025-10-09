"""
Tests for database module
"""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import database
from database_models import Base, TodoDB, TodoStatusEnum, TodoPriorityEnum

class TestDatabaseModule:
    def test_engine_creation(self):
        """Test that engine is created correctly"""
        assert database.engine is not None
        assert database.engine.url.drivername == "mysql+pymysql"

    def test_session_local_creation(self):
        """Test that SessionLocal is created correctly"""
        assert database.SessionLocal is not None
        
    @patch('database.Base.metadata.create_all')
    def test_create_tables(self, mock_create_all):
        """Test create_tables function"""
        database.create_tables()
        mock_create_all.assert_called_once_with(bind=database.engine)

    @patch('database.SessionLocal')
    def test_get_db_generator(self, mock_session_local):
        """Test get_db generator function"""
        # Mock session
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Get the generator
        db_gen = database.get_db()
        
        # Test that it yields the session
        db_session = next(db_gen)
        assert db_session == mock_session
        
        # Test that it closes on completion
        try:
            next(db_gen)
        except StopIteration:
            mock_session.close.assert_called_once()

    @patch('database.SessionLocal')
    def test_get_db_exception_handling(self, mock_session_local):
        """Test get_db exception handling"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Simulate an exception during session use
        db_gen = database.get_db()
        db_session = next(db_gen)
        
        # Force close by sending an exception
        try:
            db_gen.throw(Exception("Test exception"))
        except Exception:
            pass
        
        # Verify session was closed
        mock_session.close.assert_called_once()

    def test_engine_configuration(self):
        """Test engine configuration parameters"""
        # Test that engine has the expected configuration
        assert hasattr(database.engine, 'pool')
        # Note: We can't test exact pool settings without database connection
        # but we can verify the engine exists and is properly configured