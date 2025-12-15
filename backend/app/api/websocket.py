"""
WebSocket handler for real-time chat communication.
Handles bidirectional messaging between clients and the AI chatbot.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import json
from typing import Optional

from app.database import get_db, ChatSession, Message, Bot
from app.schemas import ChatMessageRequest, ChatMessageResponse

router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections."""
    
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: int):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, session_id: int):
        """Remove a WebSocket connection."""
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
    
    async def send_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict, session_id: int):
        """Broadcast a message to all connections in a session."""
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                await connection.send_json(message)


manager = ConnectionManager()


async def get_db_session():
    """Get database session for WebSocket handlers."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    session_id: int
):
    """
    WebSocket endpoint for real-time chat.
    Handles incoming user messages and sends AI-generated responses.
    """
    from app.database import AsyncSessionLocal
    
    # Create database session
    db = AsyncSessionLocal()
    
    try:
        # Verify session exists
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        chat_session = result.scalar_one_or_none()
        
        if not chat_session:
            await websocket.close(code=1008, reason="Session not found")
            return
        
        # Get bot configuration
        bot_result = await db.execute(
            select(Bot).where(Bot.id == chat_session.bot_id)
        )
        bot = bot_result.scalar_one_or_none()
        
        if not bot:
            await websocket.close(code=1008, reason="Bot configuration not found")
            return
        
        # Accept connection
        await manager.connect(websocket, session_id)
        
        # Send welcome message
        welcome_response = ChatMessageResponse(
            role="assistant",
            content=bot.welcome_message,
            session_id=session_id,
            timestamp=datetime.utcnow()
        )
        await manager.send_message(welcome_response.model_dump(mode="json"), websocket)
        
        # Listen for messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Validate and parse message
            user_message = message_data.get("message", "")
            
            if not user_message.strip():
                continue
            
            # Save user message to database
            user_msg = Message(
                session_id=session_id,
                role="user",
                content=user_message
            )
            db.add(user_msg)
            await db.commit()
            
            # Echo user message back (for confirmation)
            user_response = ChatMessageResponse(
                role="user",
                content=user_message,
                session_id=session_id,
                timestamp=datetime.utcnow()
            )
            await manager.send_message(user_response.model_dump(mode="json"), websocket)
            
            # Send typing indicator
            typing_indicator = {
                "role": "system",
                "content": "typing",
                "session_id": session_id
            }
            await manager.send_message(typing_indicator, websocket)
            
            # Get conversation history for context
            history_result = await db.execute(
                select(Message)
                .where(Message.session_id == session_id)
                .order_by(Message.created_at)
                .limit(10)
            )
            history_messages = history_result.scalars().all()
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in history_messages
            ]
            
            # Generate AI response using RAG engine
            from app.rag.engine import rag_engine
            from app.agent.tools import agent_tools
            
            # Check for lead intent
            lead_intent = agent_tools.detect_lead_intent(user_message)
            
            # Generate response
            rag_response = await rag_engine.generate_response(
                query=user_message,
                bot_id=chat_session.bot_id,
                system_prompt=bot.system_prompt,
                conversation_history=conversation_history,
                session_id=session_id
            )
            
            ai_response_content = rag_response["response"]
            confidence = rag_response.get("confidence", 0.0)
            
            # Handle lead capture if email/phone detected
            if lead_intent["extracted_email"] or lead_intent["extracted_phone"]:
                lead_capture_result = await agent_tools.capture_lead(
                    session_id=session_id,
                    email=lead_intent["extracted_email"],
                    phone=lead_intent["extracted_phone"],
                    db=db
                )
                
                if lead_capture_result["success"]:
                    ai_response_content += "\n\nThank you! I've saved your contact information. Someone from our team will reach out to you soon."
            
            # Ask for contact info if lead intent detected but no details
            elif lead_intent["should_ask_for_contact"]:
                ai_response_content += "\n\nI'd be happy to help! Could you please share your email address so our team can get in touch with you?"
            
            # Save AI response to database
            ai_msg = Message(
                session_id=session_id,
                role="assistant",
                content=ai_response_content
            )
            db.add(ai_msg)
            await db.commit()
            
            # Send AI response to client
            ai_response = ChatMessageResponse(
                role="assistant",
                content=ai_response_content,
                session_id=session_id,
                timestamp=datetime.utcnow(),
                confidence=confidence,
                sources=rag_response.get("sources", [])
            )
            await manager.send_message(ai_response.model_dump(mode="json"), websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        print(f"Client disconnected from session {session_id}")
    
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.close(code=1011, reason="Internal server error")
    
    finally:
        await db.close()
