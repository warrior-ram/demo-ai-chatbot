"""
Pydantic schemas for request/response validation.
"""
from app.schemas.bot import BotCreate, BotResponse
from app.schemas.chat import (
    SessionCreate,
    SessionResponse,
    MessageCreate,
    MessageResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse
)
from app.schemas.lead import LeadCreate, LeadResponse
from app.schemas.stats import DashboardStatsResponse

__all__ = [
    "BotCreate",
    "BotResponse",
    "SessionCreate",
    "SessionResponse",
    "MessageCreate",
    "MessageResponse",
    "ChatMessageRequest",
    "ChatMessageResponse",
    "ChatHistoryResponse",
    "LeadCreate",
    "LeadResponse",
    "DashboardStatsResponse",
]
