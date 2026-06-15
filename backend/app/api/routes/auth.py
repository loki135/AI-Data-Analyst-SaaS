"""Authentication routes."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.core.response import ok
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.utils.validators import validate_email, validate_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = validate_email(body.email)
    validate_password(body.password)

    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise AuthenticationError("Email already registered")

    user = User(
        email=email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
    )
    db.add(user)
    await db.flush()

    token = create_access_token(subject=user.id)
    return ok({"token": token, "user_id": user.id})


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    email = validate_email(body.email)

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise AuthenticationError("Invalid email or password")

    token = create_access_token(subject=user.id)
    return ok({"token": token, "user_id": user.id})
