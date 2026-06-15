"""Tests for shared validation utilities."""

import pytest

from app.core.exceptions import ValidationError
from app.utils.validators import validate_email, validate_non_empty, validate_password


def test_validate_email_valid():
    assert validate_email("User@Example.COM") == "user@example.com"


def test_validate_email_invalid():
    with pytest.raises(ValidationError):
        validate_email("not-an-email")


def test_validate_password_valid():
    assert validate_password("StrongPass1") == "StrongPass1"


def test_validate_password_too_short():
    with pytest.raises(ValidationError):
        validate_password("Ab1")


def test_validate_password_no_uppercase():
    with pytest.raises(ValidationError):
        validate_password("lowercase1")


def test_validate_non_empty_valid():
    assert validate_non_empty("  hello  ", "name") == "hello"


def test_validate_non_empty_blank():
    with pytest.raises(ValidationError):
        validate_non_empty("   ", "name")
