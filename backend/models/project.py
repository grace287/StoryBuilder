"""
Project model
"""

from sqlalchemy import Column, String, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin
import enum


class ProjectStatus(str, enum.Enum):
    """작품 상태"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectType(str, enum.Enum):
    """작품 분류 (소설 vs 시나리오)"""
    NOVEL = "novel"       # 소설 — 장/챕터/씬
    SCENARIO = "scenario" # 시나리오 — 회/씬


class Project(Base, UUIDMixin, TimestampMixin):
    """작품 (소설/시나리오 프로젝트)"""
    
    __tablename__ = "projects"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    project_type = Column(
        Enum(ProjectType),
        default=ProjectType.NOVEL,
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String(50), nullable=True)
    status = Column(
        Enum(ProjectStatus),
        default=ProjectStatus.DRAFT,
        nullable=False,
        index=True
    )
    logline = Column(Text, nullable=True)   # 한 줄 요약 (아카이브)
    synopsis = Column(Text, nullable=True)  # 줄거리 (아카이브)
    project_metadata = Column(JSON, nullable=True)  # {"target_words": 100000, "deadline": "2026-12-31"}
    
    # Relationships
    user = relationship("User", back_populates="projects")
    chapters = relationship("Chapter", back_populates="project", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="project", cascade="all, delete-orphan")
    timelines = relationship("Timeline", back_populates="project", cascade="all, delete-orphan")
    settings = relationship("Setting", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', status='{self.status.value}')>"
