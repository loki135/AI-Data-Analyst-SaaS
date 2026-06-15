"""Tests for app.auth.utils – password hashing & JWT."""

from app.auth.utils import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_and_verify(self) -> None:
        hashed = hash_password("s3cureP@ss")
        assert verify_password("s3cureP@ss", hashed)

    def test_wrong_password_fails(self) -> None:
        hashed = hash_password("correct")
        assert not verify_password("wrong", hashed)


class TestJWT:
    def test_roundtrip(self) -> None:
        token = create_access_token(subject="user-123")
        payload = decode_access_token(token)
        assert payload["sub"] == "user-123"
