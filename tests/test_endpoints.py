import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(client: TestClient):
    """Test user registration endpoint."""
    response = client.post("/auth/register/", json={
        "username": "newuser1",
        "password": "password123",
        "email": "newuser1@example.com"
    })
    assert response.status_code == 200
    assert "username" in response.json()


@pytest.mark.asyncio
async def test_login_user(client: TestClient):
    """Test user login endpoint."""
    response = client.post("/auth/login/", json={
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_task(client: TestClient):
    """Test task creation endpoint."""
    token = await get_user_token(client)
    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Test Task Description"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert "title" in response.json()


@pytest.mark.asyncio
async def test_read_tasks(client: TestClient):
    """Test retrieving all tasks for the authenticated user."""
    token = await get_user_token(client)
    response = client.get("/tasks/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_task(client: TestClient):
    """Test updating a task endpoint."""
    token = await get_user_token(client)
    task_id = await create_test_task(client, token)
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Title",
        "description": "Updated Description"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


# Helper functions
async def get_user_token(client: TestClient):
    response = client.post("/auth/login/", json={
        "username": "newuser",
        "password": "password123"
    })
    return response.json()["access_token"]


async def create_test_task(client: TestClient, token):
    response = client.post("/tasks/", json={
        "title": "Initial Task",
        "description": "Initial Task Description"
    }, headers={"Authorization": f"Bearer {token}"})
    return response.json()["id"]
