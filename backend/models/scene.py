"""
Scene model
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


# Many-to-Many: Scene ↔ Character
scene_characters = Table(
    'scene_characters',
    Base.metadata,
    Column('scene_id', UUID(as_uuid=True), ForeignKey('scenes.id'), primary_key=True),
    Column('character_id', UUID(as_uuid=True), ForeignKey('characters.id'), primary_key=True),
    Column('role_in_scene', String(50), nullable=True)  # main, background, mentioned
)


class Scene(Base, UUIDMixin, TimestampMixin):
    """씬 (실제 집필 단위, 보통 한 장소/시간)"""
    
    __tablename__ = "scenes"
    
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    title = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    pov_character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=True)  # 관점 인물
    location = Column(String(200), nullable=True)
    scene_time = Column(DateTime, nullable=True, index=True)  # 작중 시간
    word_count = Column(Integer, default=0)
    tags = Column(JSON, nullable=True)  # ["액션", "복선", "전환점"]
    
    # Relationships
    chapter = relationship("Chapter", back_populates="scenes")
    manuscripts = relationship("Manuscript", back_populates="scene", cascade="all, delete-orphan")
    pov_character = relationship("Character", foreign_keys=[pov_character_id])
    characters = relationship(
        "Character",
        secondary=scene_characters,
        back_populates="scenes"
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('chapter_id', 'order_index', name='uk_scene_order'),
    )
    
    def __repr__(self):
        return f"<Scene(id={self.id}, title='{self.title}', order={self.order_index})>"
