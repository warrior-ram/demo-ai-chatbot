"""
Bot-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BotCreate(BaseModel):
    """Schema for creating a new bot."""
    name: str = Field(..., min_length=1, max_length=255)
    system_prompt: str = Field(..., min_length=1)
    welcome_message: str = Field(..., min_length=1)


class BotResponse(BaseModel):
    """Schema for bot responses."""
    id: int
    name: str
    system_prompt: str
    welcome_message: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class BotUpdate(BaseModel):
    """Schema for updating bot configuration."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    system_prompt: Optional[str] = Field(None, min_length=1)
    welcome_message: Optional[str] = Field(None, min_length=1)
