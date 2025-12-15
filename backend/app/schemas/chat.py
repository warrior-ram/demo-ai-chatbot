"""
Chat session and message-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class SessionCreate(BaseModel):
    """Schema for creating a new chat session."""
    visitor_id: str = Field(..., min_length=1, max_length=255)
    bot_id: int = Field(default=1, ge=1)


class SessionResponse(BaseModel):
    """Schema for chat session responses."""
    id: int
    bot_id: int
    visitor_id: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    session_id: int = Field(..., ge=1)
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1)


class MessageResponse(BaseModel):
    """Schema for message responses."""
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class ChatMessageRequest(BaseModel):
    """Schema for incoming chat messages via WebSocket or API."""
    message: str = Field(..., min_length=1, max_length=5000)
    session_id: Optional[int] = None
    visitor_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Schema for outgoing chat message responses."""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    session_id: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confidence: Optional[float] = None
    sources: Optional[List[str]] = None


class ChatHistoryResponse(BaseModel):
    """Schema for chat history responses."""
    session_id: int
    messages: List[MessageResponse]
    total_messages: int
