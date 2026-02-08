"""
Chapter schemas
"""

from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class ChapterBase(BaseModel):
    """Chapter 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200)
    summary: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)


class ChapterCreate(ChapterBase):
    """Chapter 생성 스키마"""
    project_id: UUID
    order_index: int = Field(..., ge=1)


class ChapterUpdate(BaseModel):
    """Chapter 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    summary: Optional[str] = None
    status: Optional[str] = None
    order_index: Optional[int] = Field(None, ge=1)


class ChapterResponse(ChapterBase):
    """Chapter 응답 스키마"""
    id: UUID
    project_id: UUID
    order_index: int
    word_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChapterOrderItem(BaseModel):
    """순서 변경 항목"""
    id: UUID
    order_index: int = Field(..., ge=0)


class ChapterReorderRequest(BaseModel):
    """바인더 드래그 후 장/회 순서 일괄 변경"""
    project_id: UUID
    order: List[ChapterOrderItem]
