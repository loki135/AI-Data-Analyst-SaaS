"""Extended tests for app.auth.service – cover get_user & deactivate paths."""

import pytest

from app.auth.schemas import UserCreate
from app.auth.service import AuthService


@pytest.fixture()
def svc_with_user() -> tuple[AuthService, str]:
    svc = AuthService()
    user = svc.register(
        UserCreate(email="bob@example.com", password="p@ssw0rd!", full_name="Bob Jones")
    )
    return svc, user.id


class TestGetUser:
    def test_existing(self, svc_with_user: tuple[AuthService, str]) -> None:
        svc, uid = svc_with_user
        user = svc.get_user(uid)
        assert user is not None
        assert user.email == "bob@example.com"

    def test_missing(self) -> None:
        svc = AuthService()
        assert svc.get_user("nonexistent") is None


class TestDeactivateUser:
    def test_deactivate_success(self, svc_with_user: tuple[AuthService, str]) -> None:
        svc, uid = svc_with_user
        assert svc.deactivate_user(uid) is True
        user = svc.get_user(uid)
        assert user is not None
        assert not user.is_active

    def test_deactivate_nonexistent(self) -> None:
        svc = AuthService()
        assert svc.deactivate_user("nope") is False

    def test_deactivated_user_cannot_authenticate(
        self, svc_with_user: tuple[AuthService, str]
    ) -> None:
        svc, uid = svc_with_user
        svc.deactivate_user(uid)
        assert svc.authenticate("bob@example.com", "p@ssw0rd!") is None
