"""
Chapter API endpoints
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.chapter import Chapter
from schemas.chapter import ChapterCreate, ChapterUpdate, ChapterResponse

router = APIRouter()


@router.post("/", response_model=ChapterResponse, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db)
):
    """장 생성"""
    chapter = Chapter(**chapter_data.model_dump())
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


@router.get("/project/{project_id}", response_model=List[ChapterResponse])
async def list_chapters_by_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """작품별 장 목록 조회"""
    chapters = db.query(Chapter).filter(
        Chapter.project_id == project_id
    ).order_by(Chapter.order_index).all()
    return chapters


@router.get("/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db)
):
    """장 상세 조회"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return chapter


@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    chapter_id: UUID,
    chapter_data: ChapterUpdate,
    db: Session = Depends(get_db)
):
    """장 수정"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    for key, value in chapter_data.model_dump(exclude_unset=True).items():
        setattr(chapter, key, value)
    
    db.commit()
    db.refresh(chapter)
    return chapter


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db)
):
    """장 삭제 (하위 씬들도 cascade delete)"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    db.delete(chapter)
    db.commit()
