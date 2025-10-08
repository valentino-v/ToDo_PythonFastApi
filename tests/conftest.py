# Ensure tests can import top-level modules like `app` and `todo_service`,
# regardless of the working directory in CI runners.
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from todo_service import TaskService

@pytest.fixture
def clean_service():
    """Create a fresh TaskService instance for each test"""
    return TaskService()

@pytest.fixture(autouse=True)
def reset_global_service():
    """Reset the global task_service before each test"""
    from todo_service import task_service
    task_service._tasks.clear()
    task_service._next_id = 1

@pytest.fixture  
def clean_app():
    """Provide a clean app state for each test"""
    from todo_service import task_service
    task_service._tasks.clear()
    task_service._next_id = 1
    return task_service