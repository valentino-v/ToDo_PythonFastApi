# Ensure tests can import top-level modules like `app` and `todo_service`,
# regardless of the working directory in CI runners.
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from fastapi.testclient import TestClient
from app import app
from todo_service import TodoService

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)

@pytest.fixture
def clean_service():
    """Create a fresh TodoService instance for each test"""
    return TodoService()

@pytest.fixture(autouse=True)
def reset_global_service():
    """Reset the global todo_service before each test"""
    from todo_service import todo_service
    todo_service._todos.clear()
    todo_service._next_id = 1