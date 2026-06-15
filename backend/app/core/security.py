"""Authentication and authorization utilities.

Shared helpers for JWT creation/validation and password hashing,
avoiding repeated auth logic across routes.
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AuthenticationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(
    subject: str | int,
    extra_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT with the given subject and optional claims."""
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": str(subject), "exp": expire, **(extra_claims or {})}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT, raising AuthenticationError on failure."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHM]
        )
        if payload.get("sub") is None:
            raise AuthenticationError("Invalid token: missing subject")
        return payload
    except JWTError as e:
        raise AuthenticationError(f"Invalid token: {e}") from e
