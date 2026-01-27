"""
Pydantic schemas
"""

from .project import ProjectCreate, ProjectUpdate, ProjectResponse
from .chapter import ChapterCreate, ChapterUpdate, ChapterResponse
from .scene import SceneCreate, SceneUpdate, SceneResponse
from .character import (
    CharacterCreate, CharacterUpdate, CharacterResponse,
    CharacterRelationCreate, CharacterRelationUpdate, CharacterRelationResponse
)
from .manuscript import ManuscriptCreate, ManuscriptUpdate, ManuscriptResponse

__all__ = [
    "ProjectCreate", "ProjectUpdate", "ProjectResponse",
    "ChapterCreate", "ChapterUpdate", "ChapterResponse",
    "SceneCreate", "SceneUpdate", "SceneResponse",
    "CharacterCreate", "CharacterUpdate", "CharacterResponse",
    "CharacterRelationCreate", "CharacterRelationUpdate", "CharacterRelationResponse",
    "ManuscriptCreate", "ManuscriptUpdate", "ManuscriptResponse",
]
