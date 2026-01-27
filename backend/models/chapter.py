"""
Chapter model
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Chapter(Base, UUIDMixin, TimestampMixin):
    """장 (작품의 큰 구분 단위)"""
    
    __tablename__ = "chapters"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    summary = Column(Text, nullable=True)
    status = Column(String(20), nullable=True)  # draft, writing, revision, done
    word_count = Column(Integer, default=0)  # 하위 씬들의 합계 (자동 계산)
    
    # Relationships
    project = relationship("Project", back_populates="chapters")
    scenes = relationship("Scene", back_populates="chapter", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('project_id', 'order_index', name='uk_chapter_order'),
    )
    
    def __repr__(self):
        return f"<Chapter(id={self.id}, title='{self.title}', order={self.order_index})>"
