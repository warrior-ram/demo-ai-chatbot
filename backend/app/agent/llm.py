"""
Demo response engine for pattern-based conversational AI.
No API keys or external calls needed - perfect for demos and development.
"""
from typing import List, Dict, Optional
import asyncio
import random

from app.agent.matcher import demo_matcher


class DemoResponseEngine:
    """Demo response engine with intelligent pattern matching."""
    
    def __init__(self):
        """Initialize demo response engine."""
        self.matcher = demo_matcher
    
    async def generate_response(
        self,
        query: str,
        system_prompt: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[int] = None
    ) -> str:
        """
        Generate a response using pattern matching.
        
        Args:
            query: The user's question
            system_prompt: System prompt for the bot (not used in demo mode)
            context: Retrieved context from RAG (incorporated if available)
            conversation_history: Previous messages in conversation
            session_id: Session ID for tracking
            
        Returns:
            Generated response text
        """
        # Simulate processing delay for realism
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        # Check for context-based queries (e.g., "what about that?")
        context_category = self.matcher.detect_context_from_history(query, conversation_history)
        
        if context_category:
            category = context_category
            confidence = 0.85
        else:
            # Match intent
            category, confidence = self.matcher.match_intent(query, session_id)
        
        # Get response
        response = self.matcher.get_response(
            category=category,
            query=query,
            session_id=session_id,
            conversation_history=conversation_history
        )
        
        # If we have RAG context and it's a knowledge-seeking query, incorporate it
        if context and confidence > 0.6 and category not in ["greetings", "thanks", "goodbye"]:
            # Add a knowledge-based intro
            response = f"Based on our documentation: {response}"
        
        return response
    
    async def generate_streaming_response(
        self,
        query: str,
        system_prompt: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[int] = None
    ):
        """
        Generate a streaming response (simulated for demo).
        
        Args:
            query: The user's question
            system_prompt: System prompt for the bot
            context: Retrieved context from RAG
            conversation_history: Previous messages in conversation
            session_id: Session ID for tracking
            
        Yields:
            Response chunks as they're generated
        """
        # Generate full response
        response = await self.generate_response(
            query=query,
            system_prompt=system_prompt,
            context=context,
            conversation_history=conversation_history,
            session_id=session_id
        )
        
        # Stream it word by word for realistic effect
        words = response.split()
        for i, word in enumerate(words):
            # Add space except for first word
            chunk = word if i == 0 else f" {word}"
            yield chunk
            
            # Small delay between words
            await asyncio.sleep(random.uniform(0.05, 0.15))
    
    def is_available(self) -> bool:
        """
        Check if the response engine is available.
        
        Returns:
            Always True for demo mode
        """
        return True


# Global instance
demo_response_engine = DemoResponseEngine()

# Alias for backwards compatibility
deepseek_llm = demo_response_engine
