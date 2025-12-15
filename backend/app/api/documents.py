"""
Document management endpoints for knowledge base.
Handles document upload, processing, and ingestion.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import pypdf
from datetime import datetime

from app.database import get_db, Document, Bot
from app.rag.ingestion import document_ingestion

router = APIRouter()


@router.post("/api/v1/documents/upload", tags=["Documents"])
async def upload_document(
    bot_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and ingest a document into the bot's knowledge base.
    Supports PDF and text files.
    """
    # Verify bot exists
    bot_result = await db.execute(select(Bot).where(Bot.id == bot_id))
    bot = bot_result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found")
    
    # Check file type
    filename = file.filename
    file_extension = filename.split(".")[-1].lower()
    
    if file_extension not in ["pdf", "txt"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        if file_extension == "pdf":
            text_content = extract_text_from_pdf(file_content)
        else:  # txt
            text_content = file_content.decode("utf-8")
        
        if not text_content.strip():
            raise HTTPException(
                status_code=400,
                detail="Document appears to be empty or text could not be extracted"
            )
        
        # Store document in database
        db_document = Document(
            bot_id=bot_id,
            filename=filename,
            content=text_content,
            chunk_count=0  # Will be updated after ingestion
        )
        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)
        
        # Ingest document into vector store
        metadata = {
            "filename": filename,
            "document_id": db_document.id,
            "upload_date": datetime.utcnow().isoformat(),
            "file_type": file_extension
        }
        
        ingestion_result = await document_ingestion.ingest_document(
            content=text_content,
            metadata=metadata,
            bot_id=bot_id
        )
        
        if ingestion_result["success"]:
            # Update chunk count
            db_document.chunk_count = ingestion_result["chunk_count"]
            await db.commit()
            
            return {
                "success": True,
                "message": "Document uploaded and ingested successfully",
                "document_id": db_document.id,
                "filename": filename,
                "chunk_count": ingestion_result["chunk_count"],
                "collection_name": ingestion_result["collection_name"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ingestion failed: {ingestion_result.get('error', 'Unknown error')}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


@router.post("/api/v1/documents/text", tags=["Documents"])
async def add_text_document(
    bot_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Add text content directly to the bot's knowledge base.
    """
    # Verify bot exists
    bot_result = await db.execute(select(Bot).where(Bot.id == bot_id))
    bot = bot_result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found")
    
    if not content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
    
    try:
        # Store document in database
        db_document = Document(
            bot_id=bot_id,
            filename=f"{title}.txt",
            content=content,
            chunk_count=0
        )
        db.add(db_document)
        await db.commit()
        await db.refresh(db_document)
        
        # Ingest into vector store
        metadata = {
            "filename": f"{title}.txt",
            "document_id": db_document.id,
            "upload_date": datetime.utcnow().isoformat(),
            "file_type": "text"
        }
        
        ingestion_result = await document_ingestion.ingest_document(
            content=content,
            metadata=metadata,
            bot_id=bot_id
        )
        
        if ingestion_result["success"]:
            db_document.chunk_count = ingestion_result["chunk_count"]
            await db.commit()
            
            return {
                "success": True,
                "message": "Text content added successfully",
                "document_id": db_document.id,
                "chunk_count": ingestion_result["chunk_count"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Ingestion failed: {ingestion_result.get('error', 'Unknown error')}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing content: {str(e)}"
        )


@router.get("/api/v1/documents/bot/{bot_id}", tags=["Documents"])
async def get_bot_documents(
    bot_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all documents for a specific bot.
    """
    # Verify bot exists
    bot_result = await db.execute(select(Bot).where(Bot.id == bot_id))
    bot = bot_result.scalar_one_or_none()
    
    if not bot:
        raise HTTPException(status_code=404, detail=f"Bot {bot_id} not found")
    
    # Get documents
    result = await db.execute(
        select(Document)
        .where(Document.bot_id == bot_id)
        .order_by(desc(Document.created_at))
        .offset(skip)
        .limit(limit)
    )
    documents = result.scalars().all()
    
    # Get collection stats
    stats = document_ingestion.get_collection_stats(bot_id)
    
    return {
        "documents": [
            {
                "id": doc.id,
                "filename": doc.filename,
                "chunk_count": doc.chunk_count,
                "created_at": doc.created_at.isoformat()
            }
            for doc in documents
        ],
        "total_documents": len(documents),
        "collection_stats": stats
    }


@router.delete("/api/v1/documents/{document_id}", tags=["Documents"])
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a document from the knowledge base.
    Note: This removes from database but not from ChromaDB (would need collection rebuild).
    """
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    
    await db.delete(document)
    await db.commit()
    
    return {
        "success": True,
        "message": "Document deleted successfully",
        "document_id": document_id
    }


def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extract text from PDF file content.
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Extracted text
    """
    try:
        import io
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = pypdf.PdfReader(pdf_file)
        
        text_parts = []
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text.strip():
                text_parts.append(f"[Page {page_num + 1}]\n{text}")
        
        return "\n\n".join(text_parts)
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")
