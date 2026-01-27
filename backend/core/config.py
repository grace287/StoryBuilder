"""
Configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://storybuilder:storybuilder123@localhost:5433/storybuilder"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6380/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - 문자열로 받아서 파싱
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string"""
        if self.CORS_ORIGINS.startswith('['):
            # JSON format
            return json.loads(self.CORS_ORIGINS)
        # Comma-separated format
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
settings = Settings()
