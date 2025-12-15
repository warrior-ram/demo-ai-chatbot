"""
REST API routes for the chatbot backend.
Handles session management, message history, lead capture, and health checks.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel

from app.database import get_db, Bot, ChatSession, Message, Lead, Document
from app.config import settings
from app.schemas import (
    SessionCreate,
    SessionResponse,
    MessageResponse,
    LeadCreate,
    LeadResponse,
    BotCreate,
    BotResponse,
    ChatHistoryResponse,
    DashboardStatsResponse
)

router = APIRouter()


# Auth Schemas and Dependencies
class LoginRequest(BaseModel):
    username: str
    password: str


async def verify_admin(x_token: str = Header(None)):
    """Simple token verification middleware"""
    if x_token != "admin-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return True


# Root Endpoint
@router.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "AI Customer Support Chatbot",
        "version": "1.0.0"
    }


# Login Endpoint
@router.post("/api/v1/login", tags=["Auth"])
async def login(creds: LoginRequest):
    if creds.username == settings.admin_username and creds.password == settings.admin_password:
        return {"access_token": "admin-secret-token", "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )


# Health Check
@router.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {
        "status": "healthy",
        "service": "AI Customer Support Chatbot",
        "version": "1.0.0"
    }


# Admin Stats
@router.get("/api/v1/admin/stats", response_model=DashboardStatsResponse, tags=["Admin"], dependencies=[Depends(verify_admin)])
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics for the admin dashboard."""
    # Count sessions
    session_result = await db.execute(select(func.count()).select_from(ChatSession))
    total_sessions = session_result.scalar_one()
    
    # Count leads
    lead_result = await db.execute(select(func.count()).select_from(Lead))
    total_leads = lead_result.scalar_one()
    
    # Count active bots
    bot_result = await db.execute(select(func.count()).select_from(Bot))
    active_bots = bot_result.scalar_one()
    
    # Count documents
    doc_result = await db.execute(select(func.count()).select_from(Document))
    total_documents = doc_result.scalar_one()
    
    return DashboardStatsResponse(
        total_sessions=total_sessions,
        total_leads=total_leads,
        active_bots=active_bots,
        total_documents=total_documents
    )


# Bot Management
@router.post("/api/v1/bots", response_model=BotResponse, tags=["Bots"])
async def create_bot(bot: BotCreate, db: AsyncSession = Depends(get_db)):
    """Create a new bot configuration."""
    db_bot = Bot(
        name=bot.name,
        system_prompt=bot.system_prompt,
        welcome_message=bot.welcome_message
    )
    db.add(db_bot)
    await db.commit()
    await db.refresh(db_bot)
    return db_bot


@router.get("/api/v1/bots/{bot_id}", response_model=BotResponse, tags=["Bots"])
async def get_bot(bot_id: int, db: AsyncSession = Depends(get_db)):
    """Get bot configuration by ID."""
    result = await db.execute(select(Bot).where(Bot.id == bot_id))
    bot = result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot with id {bot_id} not found"
        )
    
    return bot


@router.get("/api/v1/bots", response_model=list[BotResponse], tags=["Bots"])
async def list_bots(db: AsyncSession = Depends(get_db)):
    """List all bot configurations."""
    result = await db.execute(select(Bot).order_by(Bot.id))
    bots = result.scalars().all()
    return bots


# Session Management
@router.post("/api/v1/chat/session", response_model=SessionResponse, tags=["Chat"])
async def create_or_get_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new chat session or retrieve existing session for a visitor.
    This enables conversation continuity across page reloads.
    """
    # Check if session already exists for this visitor and bot
    result = await db.execute(
        select(ChatSession)
        .where(
            ChatSession.visitor_id == session_data.visitor_id,
            ChatSession.bot_id == session_data.bot_id
        )
        .order_by(desc(ChatSession.created_at))
    )
    existing_session = result.scalar_one_or_none()
    
    if existing_session:
        return existing_session
    
    # Verify bot exists
    bot_result = await db.execute(select(Bot).where(Bot.id == session_data.bot_id))
    bot = bot_result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bot with id {session_data.bot_id} not found"
        )
    
    # Create new session
    new_session = ChatSession(
        bot_id=session_data.bot_id,
        visitor_id=session_data.visitor_id
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return new_session


@router.get("/api/v1/chat/session/{session_id}/history", response_model=ChatHistoryResponse, tags=["Chat"])
async def get_chat_history(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get complete chat history for a session."""
    # Verify session exists
    session_result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {session_id} not found"
        )
    
    # Get all messages for this session
    messages_result = await db.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at)
    )
    messages = messages_result.scalars().all()
    
    return ChatHistoryResponse(
        session_id=session_id,
        messages=messages,
        total_messages=len(messages)
    )


# Lead Management
@router.post("/api/v1/leads", response_model=LeadResponse, tags=["Leads"])
async def capture_lead(lead: LeadCreate, db: AsyncSession = Depends(get_db)):
    """Capture lead information from a chat session."""
    # Verify session exists
    session_result = await db.execute(
        select(ChatSession).where(ChatSession.id == lead.session_id)
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with id {lead.session_id} not found"
        )
    
    # Check if lead already exists for this session
    existing_lead_result = await db.execute(
        select(Lead).where(Lead.session_id == lead.session_id)
    )
    existing_lead = existing_lead_result.scalar_one_or_none()
    
    if existing_lead:
        # Update existing lead
        if lead.email:
            existing_lead.email = lead.email
        if lead.name:
            existing_lead.name = lead.name
        if lead.phone:
            existing_lead.phone = lead.phone
        
        await db.commit()
        await db.refresh(existing_lead)
        return existing_lead
    
    # Create new lead
    db_lead = Lead(
        session_id=lead.session_id,
        email=lead.email,
        name=lead.name,
        phone=lead.phone
    )
    db.add(db_lead)
    await db.commit()
    await db.refresh(db_lead)
    
    return db_lead


@router.get("/api/v1/leads", response_model=list[LeadResponse], tags=["Leads"])
async def get_all_leads(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all captured leads with pagination."""
    result = await db.execute(
        select(Lead)
        .order_by(desc(Lead.created_at))
        .offset(skip)
        .limit(limit)
    )
    leads = result.scalars().all()
    return leads


@router.get("/api/v1/leads/{lead_id}", response_model=LeadResponse, tags=["Leads"])
async def get_lead(lead_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific lead by ID."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lead with id {lead_id} not found"
        )
    
    return lead
