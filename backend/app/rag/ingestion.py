"""
Document ingestion and chunking for RAG.
Processes documents, splits them into chunks, and stores embeddings.
"""
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings


class DocumentIngestion:
    """Handles document processing and embedding storage."""
    
    def __init__(self):
        """Initialize the ingestion pipeline with text splitter and embeddings."""
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize embeddings model (using free HuggingFace embeddings)
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
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks using recursive character splitting.
        
        Args:
            text: The text content to chunk
            
        Returns:
            List of text chunks
        """
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    async def ingest_document(
        self,
        content: str,
        metadata: Dict[str, Any],
        bot_id: int
    ) -> Dict[str, Any]:
        """
        Ingest a document: chunk it, generate embeddings, and store in ChromaDB.
        
        Args:
            content: The document text content
            metadata: Document metadata (filename, source, etc.)
            bot_id: The bot ID this document belongs to
            
        Returns:
            Dictionary with ingestion results
        """
        # Chunk the document
        chunks = self.chunk_text(content)
        
        if not chunks:
            return {
                "success": False,
                "error": "No chunks generated from document",
                "chunk_count": 0
            }
        
        # Add bot_id to metadata for filtering
        enhanced_metadata = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                **metadata,
                "bot_id": bot_id,
                "chunk_index": i,
                "chunk_count": len(chunks)
            }
            enhanced_metadata.append(chunk_metadata)
        
        try:
            # Get or create collection for this bot
            collection_name = f"{settings.chroma_collection_name}_bot_{bot_id}"
            
            # Create vector store
            vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=collection_name,
                embedding_function=self.embeddings
            )
            
            # Add documents to vector store
            vectorstore.add_texts(
                texts=chunks,
                metadatas=enhanced_metadata
            )
            
            return {
                "success": True,
                "chunk_count": len(chunks),
                "collection_name": collection_name,
                "document_id": metadata.get("document_id", "unknown")
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chunk_count": len(chunks)
            }
    
    def get_collection_stats(self, bot_id: int) -> Dict[str, Any]:
        """
        Get statistics about a bot's knowledge base collection.
        
        Args:
            bot_id: The bot ID to get stats for
            
        Returns:
            Dictionary with collection statistics
        """
        try:
            collection_name = f"{settings.chroma_collection_name}_bot_{bot_id}"
            collection = self.chroma_client.get_collection(name=collection_name)
            
            return {
                "success": True,
                "collection_name": collection_name,
                "document_count": collection.count(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "document_count": 0
            }


# Global instance
document_ingestion = DocumentIngestion()
