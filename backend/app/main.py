"""
FastAPI Application Entry Point
Main application setup with CORS, routing, and lifecycle management.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api import routes, websocket, documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting AI Customer Support Chatbot Backend...")
    print(f"📊 Database: {settings.database_url}")
    print(f"🗄️  ChromaDB Path: {settings.chroma_path}")
    
    # Initialize database
    await init_db()
    
    # TODO: Initialize ChromaDB vector store
    print("✅ Application startup complete")
    
    yield
    
    # Shutdown
    print("👋 Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="AI Customer Support Chatbot API",
    description="FastAPI backend with RAG capabilities using DeepSeek LLM",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for widget embedding
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)
app.include_router(websocket.router)
app.include_router(documents.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "AI Customer Support Chatbot",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
