"""
Agent tools for specialized tasks.
Implements tool functions for lead capture, question answering, etc.
"""
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import re

from app.database import Lead, ChatSession
from app.rag.engine import rag_engine


class AgentTools:
    """Collection of tools the AI agent can use."""
    
    @staticmethod
    async def answer_question(
        query: str,
        bot_id: int,
        system_prompt: str,
        conversation_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Answer a question using RAG.
        
        Args:
            query: User's question
            bot_id: Bot ID for knowledge base
            system_prompt: Bot's system prompt
            conversation_history: Previous conversation messages
            
        Returns:
            Response dictionary with answer and metadata
        """
        response = await rag_engine.generate_response(
            query=query,
            bot_id=bot_id,
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )
        
        return response
    
    @staticmethod
    async def capture_lead(
        session_id: int,
        email: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        db: AsyncSession = None
    ) -> Dict[str, Any]:
        """
        Capture lead information from conversation.
        
        Args:
            session_id: Chat session ID
            email: Lead's email address
            name: Lead's name
            phone: Lead's phone number
            db: Database session
            
        Returns:
            Dictionary with capture status
        """
        if not db:
            return {
                "success": False,
                "error": "Database session not provided"
            }
        
        try:
            # Check if session exists
            session_result = await db.execute(
                select(ChatSession).where(ChatSession.id == session_id)
            )
            session = session_result.scalar_one_or_none()
            
            if not session:
                return {
                    "success": False,
                    "error": f"Session {session_id} not found"
                }
            
            # Check if lead already exists
            lead_result = await db.execute(
                select(Lead).where(Lead.session_id == session_id)
            )
            existing_lead = lead_result.scalar_one_or_none()
            
            if existing_lead:
                # Update existing lead
                if email:
                    existing_lead.email = email
                if name:
                    existing_lead.name = name
                if phone:
                    existing_lead.phone = phone
                
                await db.commit()
                
                return {
                    "success": True,
                    "message": "Lead updated successfully",
                    "lead_id": existing_lead.id,
                    "action": "updated"
                }
            else:
                # Create new lead
                new_lead = Lead(
                    session_id=session_id,
                    email=email,
                    name=name,
                    phone=phone
                )
                db.add(new_lead)
                await db.commit()
                await db.refresh(new_lead)
                
                return {
                    "success": True,
                    "message": "Lead captured successfully",
                    "lead_id": new_lead.id,
                    "action": "created"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def detect_lead_intent(message: str) -> Dict[str, Any]:
        """
        Detect if user wants to provide contact information.
        
        Args:
            message: User's message
            
        Returns:
            Dictionary with intent detection results
        """
        message_lower = message.lower()
        
        # Intent keywords
        contact_keywords = [
            "contact", "reach out", "get in touch", "call me",
            "email me", "sign up", "register", "interested",
            "demo", "pricing", "quote", "sales"
        ]
        
        has_intent = any(keyword in message_lower for keyword in contact_keywords)
        
        # Extract email if present
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        
        # Extract phone if present
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, message)
        
        return {
            "has_lead_intent": has_intent,
            "extracted_email": emails[0] if emails else None,
            "extracted_phone": phones[0] if phones else None,
            "should_ask_for_contact": has_intent and not emails and not phones
        }
    
    @staticmethod
    def should_escalate_to_human(
        message: str,
        confidence: float
    ) -> bool:
        """
        Determine if conversation should be escalated to human agent.
        
        Args:
            message: User's message
            confidence: Confidence score of RAG response
            
        Returns:
            True if should escalate, False otherwise
        """
        message_lower = message.lower()
        
        # Escalation keywords
        escalation_keywords = [
            "human", "agent", "representative", "person",
            "speak to someone", "talk to someone", "real person"
        ]
        
        has_escalation_request = any(kw in message_lower for kw in escalation_keywords)
        
        # Escalate if explicitly requested or confidence too low
        return has_escalation_request or confidence < 0.5


# Global instance
agent_tools = AgentTools()
