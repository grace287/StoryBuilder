"""
Character models
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from .base import Base, UUIDMixin, TimestampMixin


class Character(Base, UUIDMixin, TimestampMixin):
    """인물 (등장인물)"""
    
    __tablename__ = "characters"
    
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=True)  # protagonist, antagonist, supporting, minor
    description = Column(Text, nullable=True)
    personality = Column(JSON, nullable=True)  # {"mbti": "INTJ", "traits": [...]}
    appearance = Column(JSON, nullable=True)   # {"age": 35, "height": 178}
    background = Column(JSON, nullable=True)   # {"출신": "서울", "직업": "..."}
    avatar_url = Column(String(500), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="characters")
    scenes = relationship(
        "Scene",
        secondary="scene_characters",
        back_populates="characters"
    )
    
    # 관계들
    relations_from = relationship(
        "CharacterRelation",
        foreign_keys="CharacterRelation.character_a_id",
        back_populates="character_a",
        cascade="all, delete-orphan"
    )
    relations_to = relationship(
        "CharacterRelation",
        foreign_keys="CharacterRelation.character_b_id",
        back_populates="character_b",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Character(id={self.id}, name='{self.name}', role='{self.role}')>"


class CharacterRelation(Base, UUIDMixin):
    """인물 관계 (A → B)"""
    
    __tablename__ = "character_relations"
    
    character_a_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False, index=True)
    character_b_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False, index=True)
    relation_type = Column(String(50), nullable=False)  # family, friend, enemy, lover, mentor
    description = Column(Text, nullable=True)
    strength = Column(Integer, default=0)  # -100 ~ 100 (음수=적대, 양수=우호)
    created_at = Column(String, nullable=False)
    
    # Relationships
    character_a = relationship("Character", foreign_keys=[character_a_id], back_populates="relations_from")
    character_b = relationship("Character", foreign_keys=[character_b_id], back_populates="relations_to")
    
    def __repr__(self):
        return f"<CharacterRelation({self.character_a_id} --{self.relation_type}-> {self.character_b_id})>"
