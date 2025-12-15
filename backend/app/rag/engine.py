"""
RAG Engine - Orchestrates the complete RAG pipeline.
Combines retrieval, generation, and confidence scoring.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.config import settings
from app.rag.retriever import document_retriever


class RAGEngine:
    """Main RAG engine that orchestrates retrieval and generation."""
    
    def __init__(self):
        """Initialize the RAG engine."""
        self.retriever = document_retriever
        self.confidence_threshold = settings.confidence_threshold
    
    async def generate_response(
        self,
        query: str,
        bot_id: int,
        system_prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a response to a user query using RAG.
        
        Args:
            query: The user's question
            bot_id: The bot ID for knowledge base filtering
            system_prompt: The bot's system prompt
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary with response, confidence, sources, and metadata
        """
        context = ""
        confidence = 1.0
        sources = []
        retrieved_chunks = 0
        
        # Try to retrieve from knowledge base if it exists
        has_knowledge_base = self.retriever.check_collection_exists(bot_id)
        
        if has_knowledge_base:
            # Retrieve relevant documents
            relevant_docs, confidence = await self.retriever.hybrid_search(
                query=query,
                bot_id=bot_id,
                top_k=settings.retrieval_top_k
            )
            
            if relevant_docs and confidence >= self.confidence_threshold:
                context = self._build_context(relevant_docs)
                sources = [doc["metadata"].get("filename", "Unknown") for doc in relevant_docs[:3]]
                retrieved_chunks = len(relevant_docs)
        
        # ALWAYS generate response using LLM (with or without context)
        response_text = await self._generate_with_llm(
            query=query,
            context=context,
            system_prompt=system_prompt,
            conversation_history=conversation_history,
            session_id=session_id
        )
        
        return {
            "response": response_text,
            "confidence": confidence,
            "sources": sources,
            "timestamp": datetime.utcnow().isoformat(),
            "retrieved_chunks": retrieved_chunks
        }
    
    def _build_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """
        Build context string from relevant documents.
        
        Args:
            relevant_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not relevant_docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(relevant_docs[:3], 1):  # Top 3 chunks
            context_parts.append(f"[Source {i}]: {doc['content']}")
        
        return "\n\n".join(context_parts)
    
    async def _generate_with_llm(
        self,
        query: str,
        context: str,
        system_prompt: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        session_id: Optional[int] = None
    ) -> str:
        """
        Generate response using LLM with retrieved context.
        
        Args:
            query: User's query
            context: Retrieved context from knowledge base
            system_prompt: Bot's system prompt
            conversation_history: Previous conversation messages
            
        Returns:
            Generated response text
        """
        # Import Demo Response Engine
        from app.agent.llm import demo_response_engine
        
        # Generate response using demo engine
        response = await demo_response_engine.generate_response(
            query=query,
            system_prompt=system_prompt,
            context=context if context else None,
            conversation_history=conversation_history,
            session_id=session_id
        )
        
        return response
    
    async def _generate_fallback_response(
        self,
        query: str,
        reason: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Generate a fallback response when RAG cannot be used.
        
        Args:
            query: User's query
            reason: Reason for fallback
            system_prompt: Bot's system prompt
            
        Returns:
            Fallback response dictionary
        """
        fallback_messages = {
            "no_knowledge_base": "I don't have any knowledge base configured yet. Please contact support or provide some documents for me to learn from.",
            "service_unavailable": "I'm having trouble accessing my knowledge base right now. Please try again in a moment.",
        }
        
        response_text = fallback_messages.get(
            reason,
            "I'm here to help! However, I need more information to assist you properly."
        )
        
        return {
            "response": response_text,
            "confidence": 0.0,
            "sources": [],
            "timestamp": datetime.utcnow().isoformat(),
            "retrieved_chunks": 0,
            "fallback_reason": reason
        }
    
    async def _generate_low_confidence_response(
        self,
        query: str,
        confidence: float,
        relevant_docs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a response when confidence is below threshold.
        
        Args:
            query: User's query
            confidence: Confidence score
            relevant_docs: Retrieved documents (if any)
            
        Returns:
            Low-confidence response dictionary
        """
        response_text = (
            f"I'm not entirely sure about that. "
            f"Would you like me to connect you with a human agent who can better assist you?"
        )
        
        sources = [doc["metadata"].get("filename", "Unknown") for doc in relevant_docs[:3]]
        
        return {
            "response": response_text,
            "confidence": confidence,
            "sources": sources,
            "timestamp": datetime.utcnow().isoformat(),
            "retrieved_chunks": len(relevant_docs),
            "low_confidence_warning": True
        }


# Global instance
rag_engine = RAGEngine()
