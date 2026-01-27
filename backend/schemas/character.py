"""
Character schemas
"""

from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class CharacterBase(BaseModel):
    """Character 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=100)
    role: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[dict] = None
    appearance: Optional[dict] = None
    background: Optional[dict] = None
    avatar_url: Optional[str] = None


class CharacterCreate(CharacterBase):
    """Character 생성 스키마"""
    project_id: UUID


class CharacterUpdate(BaseModel):
    """Character 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = None
    description: Optional[str] = None
    personality: Optional[dict] = None
    appearance: Optional[dict] = None
    background: Optional[dict] = None
    avatar_url: Optional[str] = None


class CharacterResponse(CharacterBase):
    """Character 응답 스키마"""
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Character Relation schemas
class CharacterRelationBase(BaseModel):
    """CharacterRelation 기본 스키마"""
    relation_type: str = Field(..., max_length=50)
    description: Optional[str] = None
    strength: int = Field(default=0, ge=-100, le=100)


class CharacterRelationCreate(CharacterRelationBase):
    """CharacterRelation 생성 스키마"""
    character_a_id: UUID
    character_b_id: UUID


class CharacterRelationUpdate(BaseModel):
    """CharacterRelation 수정 스키마"""
    relation_type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    strength: Optional[int] = Field(None, ge=-100, le=100)


class CharacterRelationResponse(CharacterRelationBase):
    """CharacterRelation 응답 스키마"""
    id: UUID
    character_a_id: UUID
    character_b_id: UUID
    created_at: str
    
    class Config:
        from_attributes = True
