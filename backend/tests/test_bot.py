"""
Test bot management endpoints.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_bot():
    """Test bot creation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        bot_data = {
            "name": "Test Bot",
            "system_prompt": "You are a helpful assistant.",
            "welcome_message": "Hello! How can I help you?"
        }
        response = await client.post("/api/v1/bots", json=bot_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Bot"
    assert data["system_prompt"] == "You are a helpful assistant."
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_get_bot():
    """Test retrieving a bot by ID."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a bot first
        bot_data = {
            "name": "Test Bot 2",
            "system_prompt": "You are a helpful assistant.",
            "welcome_message": "Hello!"
        }
        create_response = await client.post("/api/v1/bots", json=bot_data)
        bot_id = create_response.json()["id"]
        
        # Get the bot
        response = await client.get(f"/api/v1/bots/{bot_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == bot_id
    assert data["name"] == "Test Bot 2"


@pytest.mark.asyncio
async def test_get_nonexistent_bot():
    """Test getting a bot that doesn't exist returns 404."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/bots/99999")
    
    assert response.status_code == 404
