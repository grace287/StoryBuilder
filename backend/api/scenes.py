"""
Scene API endpoints (placeholder)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_scenes():
    """씬 목록 조회 (추후 구현)"""
    return {"message": "Scene API - Coming soon"}
