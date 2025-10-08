"""
Tests for the FastAPI application endpoints
"""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

class TestHealthEndpoint:
    
    def test_health_check(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert "version" in data

class TestTodoEndpoints:
    
    def test_create_todo_success(self, client):
        """Test creating a todo successfully"""
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "priority": "high"
        }
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test Todo"
        assert data["description"] == "Test Description"
        assert data["status"] == "pending"
        assert data["priority"] == "high"
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_todo_minimal(self, client):
        """Test creating a todo with minimal data"""
        todo_data = {"title": "Minimal Todo"}
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Todo"
        assert data["description"] is None
        assert data["priority"] == "medium"  # default
    
    def test_create_todo_invalid_title(self, client):
        """Test creating a todo with invalid title"""
        todo_data = {"title": ""}  # Empty title
        
        response = client.post("/todos", json=todo_data)
        
        assert response.status_code == 422  # Validation error
    
    def test_get_todo_success(self, client):
        """Test getting an existing todo"""
        # First create a todo
        todo_data = {"title": "Test Todo"}
        create_response = client.post("/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/todos/{todo_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == todo_id
        assert data["title"] == "Test Todo"
    
    def test_get_todo_not_found(self, client):
        """Test getting a non-existent todo"""
        response = client.get("/todos/999")
        
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_list_todos_empty(self, client):
        """Test listing todos when none exist"""
        response = client.get("/todos")
        
        assert response.status_code == 200
        data = response.json()
        assert data["todos"] == []
        assert data["total"] == 0
    
    def test_list_todos_with_data(self, client):
        """Test listing todos with data"""
        # Create multiple todos
        client.post("/todos", json={"title": "Todo 1", "priority": "high"})
        client.post("/todos", json={"title": "Todo 2", "priority": "low"})
        
        response = client.get("/todos")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 2
        assert data["total"] == 2
    
    def test_list_todos_filter_by_status(self, client):
        """Test filtering todos by status"""
        # Create a todo and mark it as completed
        create_response = client.post("/todos", json={"title": "Test Todo"})
        todo_id = create_response.json()["id"]
        client.patch(f"/todos/{todo_id}/complete")
        
        # Create another todo (pending)
        client.post("/todos", json={"title": "Pending Todo"})
        
        # Filter by completed
        response = client.get("/todos?status=completed")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["todos"][0]["status"] == "completed"
        
        # Filter by pending
        response = client.get("/todos?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["todos"][0]["status"] == "pending"
    
    def test_list_todos_filter_by_priority(self, client):
        """Test filtering todos by priority"""
        client.post("/todos", json={"title": "High Priority", "priority": "high"})
        client.post("/todos", json={"title": "Low Priority", "priority": "low"})
        
        response = client.get("/todos?priority=high")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert data["todos"][0]["priority"] == "high"
    
    def test_list_todos_search(self, client):
        """Test searching todos"""
        client.post("/todos", json={"title": "Python Project", "description": "FastAPI development"})
        client.post("/todos", json={"title": "Java Project", "description": "Spring Boot app"})
        
        # Search in title
        response = client.get("/todos?search=Python")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
        assert "Python" in data["todos"][0]["title"]
        
        # Search in description
        response = client.get("/todos?search=FastAPI")
        assert response.status_code == 200
        data = response.json()
        assert len(data["todos"]) == 1
    
    def test_update_todo_success(self, client):
        """Test updating a todo successfully"""
        # Create a todo
        create_response = client.post("/todos", json={"title": "Original Title"})
        todo_id = create_response.json()["id"]
        
        # Update it
        updates = {
            "title": "Updated Title",
            "description": "New description",
            "status": "in_progress"
        }
        response = client.put(f"/todos/{todo_id}", json=updates)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "New description"
        assert data["status"] == "in_progress"
    
    def test_update_todo_not_found(self, client):
        """Test updating a non-existent todo"""
        updates = {"title": "Updated Title"}
        response = client.put("/todos/999", json=updates)
        
        assert response.status_code == 404
    
    def test_update_todo_partial(self, client):
        """Test partial update of a todo"""
        # Create a todo
        create_response = client.post("/todos", json={
            "title": "Original Title",
            "description": "Original description"
        })
        todo_id = create_response.json()["id"]
        
        # Update only the title
        response = client.put(f"/todos/{todo_id}", json={"title": "New Title"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == "Original description"  # Should remain unchanged
    
    def test_delete_todo_success(self, client):
        """Test deleting a todo successfully"""
        # Create a todo
        create_response = client.post("/todos", json={"title": "To Delete"})
        todo_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/todos/{todo_id}")
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/todos/{todo_id}")
        assert get_response.status_code == 404
    
    def test_delete_todo_not_found(self, client):
        """Test deleting a non-existent todo"""
        response = client.delete("/todos/999")
        
        assert response.status_code == 404
    
    def test_mark_todo_completed(self, client):
        """Test marking a todo as completed"""
        # Create a todo
        create_response = client.post("/todos", json={"title": "To Complete"})
        todo_id = create_response.json()["id"]
        
        # Mark as completed
        response = client.patch(f"/todos/{todo_id}/complete")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
    
    def test_mark_todo_completed_not_found(self, client):
        """Test marking a non-existent todo as completed"""
        response = client.patch("/todos/999/complete")
        
        assert response.status_code == 404
    
    def test_clear_completed_todos(self, client):
        """Test clearing completed todos"""
        # Create todos
        todo1_response = client.post("/todos", json={"title": "Todo 1"})
        todo2_response = client.post("/todos", json={"title": "Todo 2"})
        todo3_response = client.post("/todos", json={"title": "Todo 3"})
        
        todo1_id = todo1_response.json()["id"]
        todo3_id = todo3_response.json()["id"]
        
        # Mark some as completed
        client.patch(f"/todos/{todo1_id}/complete")
        client.patch(f"/todos/{todo3_id}/complete")
        
        # Clear completed
        response = client.delete("/todos/completed")
        
        assert response.status_code == 200
        data = response.json()
        assert "2" in data["message"]  # Should mention 2 deleted todos
    
    def test_get_todo_stats_empty(self, client):
        """Test getting stats with no todos"""
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["by_status"]["pending"] == 0
        assert data["by_priority"]["medium"] == 0
    
    def test_get_todo_stats_with_data(self, client):
        """Test getting stats with todos"""
        # Create todos with different priorities
        client.post("/todos", json={"title": "High Priority", "priority": "high"})
        client.post("/todos", json={"title": "Medium Priority", "priority": "medium"})
        todo3_response = client.post("/todos", json={"title": "Low Priority", "priority": "low"})
        
        # Mark one as completed
        todo3_id = todo3_response.json()["id"]
        client.patch(f"/todos/{todo3_id}/complete")
        
        response = client.get("/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert data["by_status"]["pending"] == 2
        assert data["by_status"]["completed"] == 1
        assert data["by_priority"]["high"] == 1
        assert data["by_priority"]["medium"] == 1
        assert data["by_priority"]["low"] == 1

class TestErrorHandling:
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON"""
        response = client.post(
            "/todos",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        response = client.post("/todos", json={})  # Missing title
        
        assert response.status_code == 422