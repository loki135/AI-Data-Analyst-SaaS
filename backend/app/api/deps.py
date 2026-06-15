"""Shared FastAPI dependencies.

Centralizes auth extraction and common dependency injection
to avoid repeating token-parsing logic in every route.
"""

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthenticationError, NotFoundError
from app.core.security import decode_access_token
from app.models.user import User


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate the current user from the Authorization header."""
    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header format")
    token = authorization.removeprefix("Bearer ")
    payload = decode_access_token(token)
    user_id = payload["sub"]

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise NotFoundError("User", user_id)
    if not user.is_active:
        raise AuthenticationError("Account is deactivated")
    return user
