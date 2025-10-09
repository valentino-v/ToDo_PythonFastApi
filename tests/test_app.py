"""
Tests for the FastAPI application endpoints
"""
import pytest
from unittest.mock import patch, Mock
from httpx import AsyncClient
from app import app

class TestTaskAPI:
    @pytest.mark.asyncio
    async def test_create_task(self):
        """Test creating a new task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/tasks", json={
                "title": "Test Task",
                "description": "Test Description"
            })
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Task"
        assert data["description"] == "Test Description"
        assert data["status"] == "pending"
    
    @pytest.mark.asyncio
    async def test_create_task_minimal(self):
        """Test creating a task with minimal data"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/tasks", json={
                "title": "Minimal Task"
            })
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None
        assert data["status"] == "pending"
    
    @pytest.mark.asyncio
    async def test_create_task_invalid_status(self):
        """Test creating a task with invalid status"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/tasks", json={
                "title": "Test Task",
                "status": "invalid_status"
            })
        
        # The task is created with the invalid status value since we don't validate in TaskCreate
        # This test shows the behavior - in a real app you might want stricter validation
        assert response.status_code == 201
    
    @pytest.mark.asyncio
    async def test_list_tasks_empty(self, clean_app):
        """Test listing tasks when none exist"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/tasks")
        
        assert response.status_code == 200
        assert response.json() == []
    
    @pytest.mark.asyncio
    async def test_list_tasks_with_data(self, clean_app):
        """Test listing tasks with data"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Create tasks
            await client.post("/tasks", json={"title": "Task 1"})
            await client.post("/tasks", json={"title": "Task 2"})
            
            response = await client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    @pytest.mark.asyncio
    async def test_get_task_exists(self, clean_app):
        """Test getting an existing task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Create a task
            create_response = await client.post("/tasks", json={"title": "Test Task"})
            task_id = create_response.json()["id"]
            
            response = await client.get(f"/tasks/{task_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"
    
    @pytest.mark.asyncio
    async def test_get_task_not_exists(self, clean_app):
        """Test getting a non-existent task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/tasks/999")
        
        assert response.status_code == 404
        assert "Task with id 999 not found" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_update_task(self, clean_app):
        """Test updating an existing task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Create a task
            create_response = await client.post("/tasks", json={"title": "Original Title"})
            task_id = create_response.json()["id"]
            
            # Update the task
            response = await client.put(f"/tasks/{task_id}", json={
                "title": "Updated Title",
                "description": "New description",
                "status": "in_progress"
            })
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "New description"
        assert data["status"] == "in_progress"
    
    @pytest.mark.asyncio
    async def test_update_task_not_exists(self, clean_app):
        """Test updating a non-existent task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put("/tasks/999", json={"title": "Updated"})
        
        assert response.status_code == 404
        assert "Task with id 999 not found" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_delete_task(self, clean_app):
        """Test deleting an existing task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Create a task
            create_response = await client.post("/tasks", json={"title": "To Delete"})
            task_id = create_response.json()["id"]
            
            # Delete the task
            response = await client.delete(f"/tasks/{task_id}")
            assert response.status_code == 204
            
            # Verify it's deleted
            get_response = await client.get(f"/tasks/{task_id}")
            assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_delete_task_not_exists(self, clean_app):
        """Test deleting a non-existent task"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete("/tasks/999")
        
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test health check endpoint"""
        from httpx import ASGITransport
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "version" in data

    @pytest.mark.asyncio 
    async def test_create_task_exception_handling(self):
        """Test exception handling in create task"""
        from httpx import ASGITransport
        with patch('app.task_service.create_task') as mock_create:
            mock_create.side_effect = Exception("Database error")
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post("/tasks", json={
                    "title": "Test Task"
                })
            
            assert response.status_code == 500
            assert "Failed to create task" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_list_tasks_exception_handling(self):
        """Test exception handling in list tasks"""
        from httpx import ASGITransport
        with patch('app.task_service.list_tasks') as mock_list:
            mock_list.side_effect = Exception("Database error")
            
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/tasks")
            
            assert response.status_code == 500
            assert "Failed to retrieve tasks" in response.json()["detail"]