"""
Scene schemas
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class SceneBase(BaseModel):
    """Scene 기본 스키마"""
    title: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    scene_time: Optional[datetime] = None
    tags: Optional[List[str]] = None


class SceneCreate(SceneBase):
    """Scene 생성 스키마"""
    chapter_id: UUID
    order_index: int = Field(..., ge=1)
    pov_character_id: Optional[UUID] = None


class SceneUpdate(BaseModel):
    """Scene 수정 스키마"""
    title: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = None
    pov_character_id: Optional[UUID] = None
    location: Optional[str] = None
    scene_time: Optional[datetime] = None
    order_index: Optional[int] = Field(None, ge=1)
    tags: Optional[List[str]] = None


class SceneResponse(SceneBase):
    """Scene 응답 스키마"""
    id: UUID
    chapter_id: UUID
    order_index: int
    pov_character_id: Optional[UUID]
    word_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
