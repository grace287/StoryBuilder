"""
Character API endpoints
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.character import Character, CharacterRelation
from schemas.character import (
    CharacterCreate, CharacterUpdate, CharacterResponse,
    CharacterRelationCreate, CharacterRelationUpdate, CharacterRelationResponse
)

router = APIRouter()


# Character CRUD
@router.post("/", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
async def create_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db)
):
    """인물 생성"""
    character = Character(**character_data.model_dump())
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


@router.get("/project/{project_id}", response_model=List[CharacterResponse])
async def list_characters_by_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """작품별 인물 목록 조회"""
    characters = db.query(Character).filter(
        Character.project_id == project_id
    ).all()
    return characters


@router.get("/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: UUID,
    db: Session = Depends(get_db)
):
    """인물 상세 조회"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: UUID,
    character_data: CharacterUpdate,
    db: Session = Depends(get_db)
):
    """인물 수정"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    for key, value in character_data.model_dump(exclude_unset=True).items():
        setattr(character, key, value)
    
    db.commit()
    db.refresh(character)
    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: UUID,
    db: Session = Depends(get_db)
):
    """인물 삭제"""
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    db.delete(character)
    db.commit()


# Character Relation CRUD
@router.post("/relations/", response_model=CharacterRelationResponse, status_code=status.HTTP_201_CREATED)
async def create_character_relation(
    relation_data: CharacterRelationCreate,
    db: Session = Depends(get_db)
):
    """인물 관계 생성"""
    from datetime import datetime
    relation = CharacterRelation(
        **relation_data.model_dump(),
        created_at=datetime.utcnow().isoformat()
    )
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


@router.get("/{character_id}/relations/", response_model=List[CharacterRelationResponse])
async def get_character_relations(
    character_id: UUID,
    db: Session = Depends(get_db)
):
    """특정 인물의 관계 목록"""
    relations = db.query(CharacterRelation).filter(
        (CharacterRelation.character_a_id == character_id) |
        (CharacterRelation.character_b_id == character_id)
    ).all()
    return relations


@router.delete("/relations/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character_relation(
    relation_id: UUID,
    db: Session = Depends(get_db)
):
    """인물 관계 삭제"""
    relation = db.query(CharacterRelation).filter(CharacterRelation.id == relation_id).first()
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relation not found"
        )
    
    db.delete(relation)
    db.commit()
