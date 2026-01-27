"""
Character API endpoints (placeholder)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_characters():
    """인물 목록 조회 (추후 구현)"""
    return {"message": "Character API - Coming soon"}
