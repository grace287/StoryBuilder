"""
Chapter API endpoints (placeholder)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_chapters():
    """장 목록 조회 (추후 구현)"""
    return {"message": "Chapter API - Coming soon"}
