"""
Timeline model
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin


class Timeline(Base, UUIDMixin):
    """타임라인 (작중 시간 순서 사건)"""
    
    __tablename__ = "timelines"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    event_time = Column(DateTime, nullable=False, index=True)  # 작중 시간
    description = Column(Text, nullable=True)
    type = Column(String(20), nullable=True)  # plot, world, character
    created_at = Column(DateTime, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="timelines")
    
    # Indexes
    __table_args__ = (
        Index('idx_timeline_project_time', 'project_id', 'event_time'),
    )
    
    def __repr__(self):
        return f"<Timeline(id={self.id}, title='{self.title}', event_time={self.event_time})>"
