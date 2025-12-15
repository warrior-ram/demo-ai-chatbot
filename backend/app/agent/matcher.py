"""
Pattern matching engine for demo responses.
Maps user queries to appropriate response categories.
"""
from typing import Tuple, List, Dict, Optional
import re
import random

from app.agent.demo_responses import DEMO_RESPONSES, ESCALATION_CONFIG, LEAD_INTENT_TRIGGERS


class DemoMatcher:
    """Match user queries to appropriate demo responses."""
    
    def __init__(self):
        self.last_responses = {}  # Track last responses per session to avoid repetition
        self.fallback_counts = {}  # Track fallback usage for escalation
        
    def match_intent(self, query: str, session_id: int = None) -> Tuple[str, float]:
        """
        Match user query to intent category.
        
        Args:
            query: User's message
            session_id: Session ID for tracking context
            
        Returns:
            Tuple of (category, confidence)
        """
        query_lower = query.lower().strip()
        
        # Empty query
        if not query_lower:
            return ("fallback", 0.3)
        
        # Check each category for keyword matches
        best_match = ("fallback", 0.0)
        
        for category, data in DEMO_RESPONSES.items():
            if category == "fallback":
                continue
                
            keywords = data.get("keywords", [])
            if not keywords:
                continue
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in query_lower)
            
            if matches > 0:
                # Calculate confidence based on match count and keyword specificity
                confidence = min(0.9, 0.5 + (matches * 0.2))
                
                if confidence > best_match[1]:
                    best_match = (category, confidence)
        
        # Special handling for multi-word phrases
        if "get started" in query_lower or "how to start" in query_lower:
            return ("getting_started", 0.95)
        
        if "thank" in query_lower:
            return ("thanks", 0.95)
            
        if any(word in query_lower for word in ["bye", "goodbye", "see you later"]):
            return ("goodbye", 0.95)
        
        # Check for frustration/complaint
        frustration_words = ESCALATION_CONFIG["frustration_keywords"]
        if any(word in query_lower for word in frustration_words):
            return ("complaint", 0.9)
        
        # Check for lead intent
        if any(trigger in query_lower for trigger in LEAD_INTENT_TRIGGERS):
            return ("lead_capture", 0.85)
        
        return best_match
    
    def get_response(
        self,
        category: str,
        query: str,
        session_id: int = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Get appropriate response for matched category.
        
        Args:
            category: Matched intent category
            query: Original user query
            session_id: Session ID for context tracking
            conversation_history: Previous messages
            
        Returns:
            Response text
        """
        data = DEMO_RESPONSES.get(category, DEMO_RESPONSES["fallback"])
        responses = data.get("responses", [])
        
        if not responses:
            return self._get_fallback_response(session_id, conversation_history)
        
        # Select response (avoid repeating the last one for this session)
        if session_id:
            last_response = self.last_responses.get(session_id, {}).get(category)
            available_responses = [r for r in responses if r != last_response]
            
            if not available_responses:
                available_responses = responses
            
            response = random.choice(available_responses)
            
            # Track this response
            if session_id not in self.last_responses:
                self.last_responses[session_id] = {}
            self.last_responses[session_id][category] = response
        else:
            response = random.choice(responses)
        
        # Add follow-up if available and appropriate
        follow_ups = data.get("follow_ups", [])
        if follow_ups and random.random() < 0.4:  # 40% chance to add follow-up
            response += "\n\n" + random.choice(follow_ups)
        
        # Check if we should suggest escalation
        if conversation_history and len(conversation_history) > ESCALATION_CONFIG["max_conversation_length"]:
            response += "\n\n_I've provided a lot of information! Would you like me to connect you with a human agent for more personalized assistance?_"
        
        return response
    
    def _get_fallback_response(
        self,
        session_id: int = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Get fallback response and track usage for escalation."""
        responses = DEMO_RESPONSES["fallback"]["responses"]
        
        # Track fallback count
        if session_id:
            if session_id not in self.fallback_counts:
                self.fallback_counts[session_id] = 0
            self.fallback_counts[session_id] += 1
            
            # Escalate after multiple fallbacks
            if self.fallback_counts[session_id] >= ESCALATION_CONFIG["max_fallback_count"]:
                return (
                    "I want to make sure you get the best help possible. "
                    "It seems like your question might need a specialist. "
                    "Would you like me to connect you with our team? "
                    "I just need your email address to have someone reach out to you."
                )
        
        return random.choice(responses)
    
    def detect_context_from_history(
        self,
        query: str,
        conversation_history: Optional[List[Dict]]
    ) -> Optional[str]:
        """
        Detect if current query relates to previous conversation context.
        
        Args:
            query: Current user query
            conversation_history: Previous messages
            
        Returns:
            Related category if found, None otherwise
        """
        if not conversation_history or len(conversation_history) < 2:
            return None
        
        query_lower = query.lower()
        
        # Simple context references
        context_references = {
            "what about": True,
            "tell me more": True,
            "more about": True,
            "and": True,
            "also": True,
        }
        
        # Check if query is a context reference
        has_context_reference = any(ref in query_lower for ref in context_references)
        
        if has_context_reference:
            # Look at last 2 bot messages for category hints
            recent_messages = conversation_history[-4:]  # Last 2 exchanges
            
            for msg in reversed(recent_messages):
                if msg.get("role") == "assistant":
                    content = msg.get("content", "").lower()
                    
                    # Try to detect what was discussed
                    for category, data in DEMO_RESPONSES.items():
                        keywords = data.get("keywords", [])
                        if any(keyword in content for keyword in keywords[:3]):  # Check top keywords
                            return category
        
        return None
    
    def should_capture_lead(self, query: str) -> bool:
        """Check if message indicates user wants to be contacted."""
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in LEAD_INTENT_TRIGGERS)
    
    def reset_session_tracking(self, session_id: int):
        """Reset tracking for a session (when session ends)."""
        if session_id in self.last_responses:
            del self.last_responses[session_id]
        if session_id in self.fallback_counts:
            del self.fallback_counts[session_id]


# Global matcher instance
demo_matcher = DemoMatcher()
