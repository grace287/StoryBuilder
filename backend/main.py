"""
StoryBuilder FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import engine
from models.base import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StoryBuilder API",
    description="작가용 IDE - 장편 서사 집필 도구",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "app": "StoryBuilder API",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Import routers
from api import projects, chapters, scenes, characters, manuscripts, auth, websocket

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["chapters"])
app.include_router(scenes.router, prefix="/api/scenes", tags=["scenes"])
app.include_router(characters.router, prefix="/api/characters", tags=["characters"])
app.include_router(manuscripts.router, prefix="/api/manuscripts", tags=["manuscripts"])
app.include_router(websocket.router, prefix="/api", tags=["websocket"])
