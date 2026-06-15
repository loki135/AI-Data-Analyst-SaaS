"""Auth business-logic layer."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from app.auth.schemas import UserCreate, UserResponse
from app.auth.utils import create_access_token, hash_password, verify_password


@dataclass
class _UserRecord:
    id: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True


@dataclass
class AuthService:
    """In-memory auth service (swap with DB-backed implementation later)."""

    _users: dict[str, _UserRecord] = field(default_factory=dict)
    _email_index: dict[str, str] = field(default_factory=dict)

    def register(self, payload: UserCreate) -> UserResponse:
        """Register a new user. Raises ``ValueError`` on duplicate email."""
        if payload.email in self._email_index:
            raise ValueError(f"Email already registered: {payload.email}")
        uid = uuid.uuid4().hex
        record = _UserRecord(
            id=uid,
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        self._users[uid] = record
        self._email_index[payload.email] = uid
        return UserResponse(
            id=uid, email=record.email, full_name=record.full_name, is_active=record.is_active
        )

    def authenticate(self, email: str, password: str) -> str | None:
        """Return an access token if credentials are valid, else ``None``."""
        uid = self._email_index.get(email)
        if uid is None:
            return None
        record = self._users[uid]
        if not record.is_active:
            return None
        if not verify_password(password, record.hashed_password):
            return None
        return create_access_token(subject=uid)

    def get_user(self, user_id: str) -> UserResponse | None:
        """Look up a user by ID."""
        record = self._users.get(user_id)
        if record is None:
            return None
        return UserResponse(
            id=record.id,
            email=record.email,
            full_name=record.full_name,
            is_active=record.is_active,
        )

    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user. Returns ``True`` if the user existed."""
        record = self._users.get(user_id)
        if record is None:
            return False
        record.is_active = False
        return True
