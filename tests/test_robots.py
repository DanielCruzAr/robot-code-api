"""
Test robot API endpoints
"""
import pytest
from fastapi.testclient import TestClient


def test_get_robots(client: TestClient):
    """Test getting all robots"""
    response = client.get("/api/v1/robots/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # We have sample data


def test_get_robot_by_id(client: TestClient):
    """Test getting a robot by ID"""
    response = client.get("/api/v1/robots/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 1
    assert "name" in data
    assert "model" in data


def test_get_robot_not_found(client: TestClient):
    """Test getting a non-existent robot"""
    response = client.get("/api/v1/robots/999")
    assert response.status_code == 404


def test_create_robot(client: TestClient):
    """Test creating a new robot"""
    robot_data = {
        "name": "TestBot",
        "model": "Test-v1",
        "status": "active",
        "battery_level": 100.0,
        "location": "Test Lab"
    }
    response = client.post("/api/v1/robots/", json=robot_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == robot_data["name"]
    assert data["model"] == robot_data["model"]
    assert "id" in data


def test_update_robot(client: TestClient):
    """Test updating a robot"""
    update_data = {
        "name": "Updated Atlas",
        "battery_level": 90.0
    }
    response = client.put("/api/v1/robots/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["battery_level"] == update_data["battery_level"]


def test_update_robot_not_found(client: TestClient):
    """Test updating a non-existent robot"""
    update_data = {"name": "Non-existent"}
    response = client.put("/api/v1/robots/999", json=update_data)
    assert response.status_code == 404


def test_delete_robot(client: TestClient):
    """Test deleting a robot"""
    # First create a robot to delete
    robot_data = {
        "name": "ToDelete",
        "model": "Delete-v1"
    }
    create_response = client.post("/api/v1/robots/", json=robot_data)
    assert create_response.status_code == 200
    robot_id = create_response.json()["id"]
    
    # Now delete it
    response = client.delete(f"/api/v1/robots/{robot_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/api/v1/robots/{robot_id}")
    assert get_response.status_code == 404


def test_delete_robot_not_found(client: TestClient):
    """Test deleting a non-existent robot"""
    response = client.delete("/api/v1/robots/999")
    assert response.status_code == 404