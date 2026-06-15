"""Shared validation helpers.

Centralizes common validation patterns to avoid duplicate checks
across different route handlers and services.
"""

import re

from app.core.exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> str:
    """Validate and normalize an email address."""
    email = email.strip().lower()
    if not EMAIL_REGEX.match(email):
        raise ValidationError(
            "Invalid email format",
            errors=[{"field": "email", "message": "Must be a valid email address"}],
        )
    return email


def validate_password(password: str, min_length: int = 8) -> str:
    """Validate password strength."""
    errors: list[dict[str, str]] = []
    if len(password) < min_length:
        errors.append({
            "field": "password",
            "message": f"Must be at least {min_length} characters",
        })
    if not re.search(r"[A-Z]", password):
        errors.append({
            "field": "password",
            "message": "Must contain an uppercase letter",
        })
    if not re.search(r"[a-z]", password):
        errors.append({
            "field": "password",
            "message": "Must contain a lowercase letter",
        })
    if not re.search(r"\d", password):
        errors.append({
            "field": "password",
            "message": "Must contain a digit",
        })
    if errors:
        raise ValidationError("Password does not meet requirements", errors=errors)
    return password


def validate_non_empty(value: str, field_name: str) -> str:
    """Ensure a string field is not empty or whitespace-only."""
    value = value.strip()
    if not value:
        raise ValidationError(
            f"{field_name} is required",
            errors=[{"field": field_name, "message": "Cannot be empty"}],
        )
    return value
