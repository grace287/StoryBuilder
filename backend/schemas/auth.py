"""
Auth schemas
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """회원가입 스키마"""
    email: EmailStr
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """로그인 스키마"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """사용자 정보 응답"""
    id: UUID
    email: str
    username: str
    
    class Config:
        from_attributes = True
