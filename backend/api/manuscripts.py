"""
Manuscript API endpoints
"""

from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from core.database import get_db
from models.manuscript import Manuscript
from schemas.manuscript import ManuscriptCreate, ManuscriptUpdate, ManuscriptResponse

router = APIRouter()


@router.post("/", response_model=ManuscriptResponse, status_code=status.HTTP_201_CREATED)
async def create_manuscript(
    manuscript_data: ManuscriptCreate,
    db: Session = Depends(get_db)
):
    """원고 생성 (새 버전)"""
    # 기존 버전 확인
    last_version = db.query(Manuscript).filter(
        Manuscript.scene_id == manuscript_data.scene_id
    ).order_by(desc(Manuscript.version)).first()
    
    next_version = (last_version.version + 1) if last_version else 1
    
    # 단어 수 계산 (간단한 공백 기준)
    word_count = len(manuscript_data.content.split())
    
    manuscript = Manuscript(
        scene_id=manuscript_data.scene_id,
        content=manuscript_data.content,
        format=manuscript_data.format,
        version=next_version,
        word_count=word_count,
        created_at=datetime.utcnow(),
        auto_saved_at=datetime.utcnow()
    )
    
    db.add(manuscript)
    db.commit()
    db.refresh(manuscript)
    
    # Scene의 word_count 업데이트
    from models.scene import Scene
    scene = db.query(Scene).filter(Scene.id == manuscript_data.scene_id).first()
    if scene:
        scene.word_count = word_count
        db.commit()
    
    return manuscript


@router.get("/scene/{scene_id}", response_model=List[ManuscriptResponse])
async def list_manuscripts_by_scene(
    scene_id: UUID,
    db: Session = Depends(get_db)
):
    """씬별 원고 버전 목록"""
    manuscripts = db.query(Manuscript).filter(
        Manuscript.scene_id == scene_id
    ).order_by(desc(Manuscript.version)).all()
    return manuscripts


@router.get("/scene/{scene_id}/latest", response_model=ManuscriptResponse)
async def get_latest_manuscript(
    scene_id: UUID,
    db: Session = Depends(get_db)
):
    """씬의 최신 원고 조회"""
    manuscript = db.query(Manuscript).filter(
        Manuscript.scene_id == scene_id
    ).order_by(desc(Manuscript.version)).first()
    
    if not manuscript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No manuscript found for this scene"
        )
    
    return manuscript


@router.get("/{manuscript_id}", response_model=ManuscriptResponse)
async def get_manuscript(
    manuscript_id: UUID,
    db: Session = Depends(get_db)
):
    """원고 상세 조회"""
    manuscript = db.query(Manuscript).filter(Manuscript.id == manuscript_id).first()
    if not manuscript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manuscript not found"
        )
    return manuscript


@router.put("/scene/{scene_id}/autosave", response_model=ManuscriptResponse)
async def autosave_manuscript(
    scene_id: UUID,
    manuscript_data: ManuscriptUpdate,
    db: Session = Depends(get_db)
):
    """자동저장 (기존 최신 버전 덮어쓰기)"""
    manuscript = db.query(Manuscript).filter(
        Manuscript.scene_id == scene_id
    ).order_by(desc(Manuscript.version)).first()
    
    if not manuscript:
        # 첫 원고 생성
        return await create_manuscript(
            ManuscriptCreate(
                scene_id=scene_id,
                content=manuscript_data.content
            ),
            db
        )
    
    # 기존 원고 업데이트
    manuscript.content = manuscript_data.content
    manuscript.word_count = len(manuscript_data.content.split())
    manuscript.auto_saved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(manuscript)
    
    # Scene의 word_count 업데이트
    from models.scene import Scene
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if scene:
        scene.word_count = manuscript.word_count
        db.commit()
    
    return manuscript


@router.delete("/{manuscript_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_manuscript(
    manuscript_id: UUID,
    db: Session = Depends(get_db)
):
    """원고 버전 삭제"""
    manuscript = db.query(Manuscript).filter(Manuscript.id == manuscript_id).first()
    if not manuscript:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manuscript not found"
        )
    
    db.delete(manuscript)
    db.commit()
