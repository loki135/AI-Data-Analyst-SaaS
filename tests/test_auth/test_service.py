"""Tests for app.auth.service – AuthService."""

import pytest

from app.auth.schemas import UserCreate
from app.auth.service import AuthService


@pytest.fixture()
def auth_svc() -> AuthService:
    return AuthService()


@pytest.fixture()
def user_payload() -> UserCreate:
    return UserCreate(email="alice@example.com", password="str0ngP@ss!", full_name="Alice Smith")


class TestRegister:
    def test_register_success(self, auth_svc: AuthService, user_payload: UserCreate) -> None:
        user = auth_svc.register(user_payload)
        assert user.email == "alice@example.com"
        assert user.full_name == "Alice Smith"
        assert user.is_active

    def test_duplicate_email_raises(
        self, auth_svc: AuthService, user_payload: UserCreate
    ) -> None:
        auth_svc.register(user_payload)
        with pytest.raises(ValueError, match="already registered"):
            auth_svc.register(user_payload)


class TestAuthenticate:
    def test_valid_credentials(self, auth_svc: AuthService, user_payload: UserCreate) -> None:
        auth_svc.register(user_payload)
        token = auth_svc.authenticate("alice@example.com", "str0ngP@ss!")
        assert token is not None

    def test_wrong_password(self, auth_svc: AuthService, user_payload: UserCreate) -> None:
        auth_svc.register(user_payload)
        assert auth_svc.authenticate("alice@example.com", "wrongpass") is None

    def test_unknown_email(self, auth_svc: AuthService) -> None:
        assert auth_svc.authenticate("nobody@example.com", "pass") is None
