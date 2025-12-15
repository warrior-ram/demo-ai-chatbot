"""
Configuration management for the AI Customer Support Chatbot backend.
Uses Pydantic Settings for type-safe environment variable handling.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./chatbot.db"
    
    # ChromaDB Configuration
    chroma_path: str = "./chroma_db"
    chroma_collection_name: str = "knowledge_base"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # CORS Configuration
    allowed_origins: str = "*"
    
    # RAG Configuration
    chunk_size: int = 800
    chunk_overlap: int = 100
    retrieval_top_k: int = 5
    confidence_threshold: float = 0.7
    
    # Rate Limiting
    rate_limit_messages_per_hour: int = 50

    # Authentication
    admin_username: str = "admin"
    admin_password: str = "admin"

    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
