"""
Project API endpoints
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.project import Project, ProjectStatus
from schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectArchiveResponse

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    """작품 생성"""
    project = Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """작품 목록 조회"""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """작품 상세 조회"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.get("/{project_id}/archive", response_model=ProjectArchiveResponse)
async def get_project_archive(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """아카이브: 로그라인·줄거리·등장인물 등 요약 (소설/시나리오 공통)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    from models.character import Character
    from models.chapter import Chapter
    from models.scene import Scene
    character_count = db.query(Character).filter(Character.project_id == project_id).count()
    chapter_count = db.query(Chapter).filter(Chapter.project_id == project_id).count()
    scene_count = db.query(Scene).join(Chapter).filter(Chapter.project_id == project_id).count()
    base = ProjectResponse.model_validate(project)
    return ProjectArchiveResponse(
        **base.model_dump(),
        character_count=character_count,
        chapter_count=chapter_count,
        scene_count=scene_count,
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """작품 수정"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """작품 삭제 (soft delete)"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.status = ProjectStatus.ARCHIVED
    db.commit()
