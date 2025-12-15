"""
Document retrieval for RAG.
Implements hybrid search (vector similarity + keyword matching).
"""
from typing import List, Dict, Any, Tuple
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings


class DocumentRetriever:
    """Handles retrieval of relevant documents for user queries."""
    
    def __init__(self):
        """Initialize the retriever with embeddings and ChromaDB client."""
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
    
    async def retrieve_relevant_docs(
        self,
        query: str,
        bot_id: int,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query using vector similarity search.
        
        Args:
            query: The user's query
            bot_id: The bot ID to search within
            top_k: Number of top results to return (default from settings)
            
        Returns:
            List of relevant documents with metadata and scores
        """
        if top_k is None:
            top_k = settings.retrieval_top_k
        
        try:
            collection_name = f"{settings.chroma_collection_name}_bot_{bot_id}"
            
            # Create vector store
            vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
            
            # Perform similarity search with scores
            results = vectorstore.similarity_search_with_score(
                query=query,
                k=top_k
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score),
                    "relevance": self._calculate_relevance(score)
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return []
    
    def _calculate_relevance(self, distance_score: float) -> float:
        """
        Convert distance score to relevance score (0-1 range).
        Lower distance = higher relevance.
        
        Args:
            distance_score: The distance score from similarity search
            
        Returns:
            Relevance score between 0 and 1
        """
        # ChromaDB uses L2 distance, convert to similarity score
        # Using exponential decay: relevance = e^(-distance)
        import math
        relevance = math.exp(-distance_score)
        return min(max(relevance, 0.0), 1.0)
    
    async def hybrid_search(
        self,
        query: str,
        bot_id: int,
        top_k: int = None
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Perform hybrid search combining vector similarity and keyword matching.
        
        Args:
            query: The user's query
            bot_id: The bot ID to search within
            top_k: Number of top results to return
            
        Returns:
            Tuple of (relevant documents, confidence score)
        """
        # Retrieve documents
        results = await self.retrieve_relevant_docs(query, bot_id, top_k)
        
        if not results:
            return [], 0.0
        
        # Calculate overall confidence based on top result
        confidence = results[0]["relevance"] if results else 0.0
        
        # Apply keyword boosting (simple implementation)
        query_keywords = set(query.lower().split())
        for result in results:
            content_lower = result["content"].lower()
            keyword_matches = sum(1 for kw in query_keywords if kw in content_lower)
            
            # Boost score if keywords match
            if keyword_matches > 0:
                boost = min(keyword_matches * 0.05, 0.2)  # Max 20% boost
                result["relevance"] = min(result["relevance"] + boost, 1.0)
        
        # Re-sort by boosted relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        
        # Recalculate confidence
        confidence = results[0]["relevance"] if results else 0.0
        
        return results, confidence
    
    def check_collection_exists(self, bot_id: int) -> bool:
        """
        Check if a collection exists for a bot.
        
        Args:
            bot_id: The bot ID to check
            
        Returns:
            True if collection exists, False otherwise
        """
        try:
            collection_name = f"{settings.chroma_collection_name}_bot_{bot_id}"
            self.chroma_client.get_collection(name=collection_name)
            return True
        except Exception:
            return False


# Global instance
document_retriever = DocumentRetriever()
