"""
Setting model
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Setting(Base, UUIDMixin, TimestampMixin):
    """세계관 설정 (위키 페이지)"""
    
    __tablename__ = "settings"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # world, magic, tech, social, culture
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)  # 자유 형식 상세 정보
    
    # Relationships
    project = relationship("Project", back_populates="settings")
    
    def __repr__(self):
        return f"<Setting(id={self.id}, name='{self.name}', category='{self.category}')>"
