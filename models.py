"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    """Request model for translation endpoint."""
    text: str
    source_lang: str = Field(pattern="^(gn|es)$")
    target_lang: str = Field(pattern="^(gn|es)$")


class TranslateResponse(BaseModel):
    """Response model for translation endpoint."""
    translated_text: str
