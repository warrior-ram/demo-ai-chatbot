"""
Test chat session management.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_session():
    """Test creating a new chat session."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a bot first
        bot_data = {
            "name": "Session Test Bot",
            "system_prompt": "You are helpful.",
            "welcome_message": "Hi!"
        }
        bot_response = await client.post("/api/v1/bots", json=bot_data)
        bot_id = bot_response.json()["id"]
        
        # Create session
        session_data = {
            "visitor_id": "test-visitor-123",
            "bot_id": bot_id
        }
        response = await client.post("/api/v1/chat/session", json=session_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["visitor_id"] == "test-visitor-123"
    assert data["bot_id"] == bot_id
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_session_reuse():
    """Test that existing session is returned for same visitor."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create bot
        bot_data = {
            "name": "Reuse Test Bot",
            "system_prompt": "You are helpful.",
            "welcome_message": "Hi!"
        }
        bot_response = await client.post("/api/v1/bots", json=bot_data)
        bot_id = bot_response.json()["id"]
        
        # Create first session
        session_data = {
            "visitor_id": "test-visitor-456",
            "bot_id": bot_id
        }
        response1 = await client.post("/api/v1/chat/session", json=session_data)
        session_id_1 = response1.json()["id"]
        
        # Try to create another session with same visitor
        response2 = await client.post("/api/v1/chat/session", json=session_data)
        session_id_2 = response2.json()["id"]
    
    # Should return the same session
    assert session_id_1 == session_id_2


@pytest.mark.asyncio
async def test_get_chat_history():
    """Test retrieving chat history."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create bot and session
        bot_data = {
            "name": "History Test Bot",
            "system_prompt": "You are helpful.",
            "welcome_message": "Hi!"
        }
        bot_response = await client.post("/api/v1/bots", json=bot_data)
        bot_id = bot_response.json()["id"]
        
        session_data = {
            "visitor_id": "test-visitor-789",
            "bot_id": bot_id
        }
        session_response = await client.post("/api/v1/chat/session", json=session_data)
        session_id = session_response.json()["id"]
        
        # Get history
        response = await client.get(f"/api/v1/chat/session/{session_id}/history")
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert "messages" in data
    assert "total_messages" in data
