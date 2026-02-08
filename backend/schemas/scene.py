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


class SceneOrderItem(BaseModel):
    """순서 변경 항목"""
    id: UUID
    order_index: int = Field(..., ge=0)


class SceneReorderRequest(BaseModel):
    """바인더 드래그 후 씬 순서 일괄 변경"""
    chapter_id: UUID
    order: List[SceneOrderItem]
