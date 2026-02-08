"""
Scene API endpoints
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.scene import Scene
from schemas.scene import SceneCreate, SceneUpdate, SceneResponse, SceneReorderRequest

router = APIRouter()


@router.post("/", response_model=SceneResponse, status_code=status.HTTP_201_CREATED)
async def create_scene(
    scene_data: SceneCreate,
    db: Session = Depends(get_db)
):
    """씬 생성"""
    scene = Scene(**scene_data.model_dump())
    db.add(scene)
    db.commit()
    db.refresh(scene)
    return scene


@router.get("/chapter/{chapter_id}", response_model=List[SceneResponse])
async def list_scenes_by_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db)
):
    """장별 씬 목록 조회"""
    scenes = db.query(Scene).filter(
        Scene.chapter_id == chapter_id
    ).order_by(Scene.order_index).all()
    return scenes


@router.patch("/reorder", response_model=List[SceneResponse])
async def reorder_scenes(
    body: SceneReorderRequest,
    db: Session = Depends(get_db)
):
    """바인더 드래그: 씬 순서 일괄 변경"""
    for item in body.order:
        scene = db.query(Scene).filter(
            Scene.id == item.id,
            Scene.chapter_id == body.chapter_id
        ).first()
        if scene:
            scene.order_index = item.order_index
    db.commit()
    return db.query(Scene).filter(
        Scene.chapter_id == body.chapter_id
    ).order_by(Scene.order_index).all()


@router.get("/{scene_id}", response_model=SceneResponse)
async def get_scene(
    scene_id: UUID,
    db: Session = Depends(get_db)
):
    """씬 상세 조회"""
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )
    return scene


@router.put("/{scene_id}", response_model=SceneResponse)
async def update_scene(
    scene_id: UUID,
    scene_data: SceneUpdate,
    db: Session = Depends(get_db)
):
    """씬 수정"""
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )
    
    for key, value in scene_data.model_dump(exclude_unset=True).items():
        setattr(scene, key, value)
    
    db.commit()
    db.refresh(scene)
    return scene


@router.delete("/{scene_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scene(
    scene_id: UUID,
    db: Session = Depends(get_db)
):
    """씬 삭제 (하위 원고들도 cascade delete)"""
    scene = db.query(Scene).filter(Scene.id == scene_id).first()
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scene not found"
        )
    
    db.delete(scene)
    db.commit()
