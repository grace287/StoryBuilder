"""
Manuscript schemas
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class ManuscriptBase(BaseModel):
    """Manuscript 기본 스키마"""
    content: str
    format: str = Field(default="markdown", max_length=20)


class ManuscriptCreate(ManuscriptBase):
    """Manuscript 생성 스키마"""
    scene_id: UUID


class ManuscriptUpdate(BaseModel):
    """Manuscript 수정 스키마 (자동저장용)"""
    content: str


class ManuscriptResponse(ManuscriptBase):
    """Manuscript 응답 스키마"""
    id: UUID
    scene_id: UUID
    version: int
    word_count: int
    created_at: datetime
    auto_saved_at: Optional[datetime]
    
    class Config:
        from_attributes = True
