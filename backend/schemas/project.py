"""
Project schemas
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from models.project import ProjectStatus


class ProjectBase(BaseModel):
    """프로젝트 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    genre: Optional[str] = None
    metadata: Optional[dict] = None


class ProjectCreate(ProjectBase):
    """프로젝트 생성 스키마"""
    user_id: UUID
    status: ProjectStatus = ProjectStatus.DRAFT


class ProjectUpdate(BaseModel):
    """프로젝트 수정 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    genre: Optional[str] = None
    status: Optional[ProjectStatus] = None
    metadata: Optional[dict] = None


class ProjectResponse(ProjectBase):
    """프로젝트 응답 스키마"""
    id: UUID
    user_id: UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
