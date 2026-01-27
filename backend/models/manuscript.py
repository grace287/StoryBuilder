"""
Manuscript model
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin


class Manuscript(Base, UUIDMixin):
    """원고 (실제 텍스트, 버전 관리)"""
    
    __tablename__ = "manuscripts"
    
    scene_id = Column(UUID(as_uuid=True), ForeignKey("scenes.id"), nullable=False, index=True)
    version = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)  # 실제 원고
    format = Column(String(20), default="markdown", nullable=False)  # markdown, html, plain
    word_count = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False)
    auto_saved_at = Column(DateTime, nullable=True)
    
    # Relationships
    scene = relationship("Scene", back_populates="manuscripts")
    
    # Indexes
    __table_args__ = (
        Index('idx_manuscript_scene_version', 'scene_id', 'version'),
    )
    
    def __repr__(self):
        return f"<Manuscript(id={self.id}, scene_id={self.scene_id}, version={self.version})>"
