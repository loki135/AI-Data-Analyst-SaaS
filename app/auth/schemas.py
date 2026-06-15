"""Pydantic schemas for authentication."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload for creating a new user."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=256)


class UserResponse(BaseModel):
    """Public representation of a user."""

    id: str
    email: str
    full_name: str
    is_active: bool = True


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str
    exp: int
