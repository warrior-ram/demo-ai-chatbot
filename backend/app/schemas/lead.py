"""
Lead capture-related Pydantic schemas.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class LeadCreate(BaseModel):
    """Schema for creating a new lead."""
    session_id: int = Field(..., ge=1)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)


class LeadResponse(BaseModel):
    """Schema for lead responses."""
    id: int
    session_id: int
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


class LeadUpdate(BaseModel):
    """Schema for updating lead information."""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, min_length=1, max_length=50)
