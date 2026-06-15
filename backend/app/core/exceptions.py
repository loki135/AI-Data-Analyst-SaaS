"""Centralized exception definitions and handlers.

All API errors inherit from AppError so they share a consistent
JSON response shape and avoid duplicated error-formatting logic.
"""

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error with status code and structured detail."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        detail: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.detail = detail or {}
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str | int) -> None:
        super().__init__(
            message=f"{resource} not found",
            status_code=404,
            detail={"resource": resource, "id": str(resource_id)},
        )


class ValidationError(AppError):
    def __init__(
        self, message: str, errors: list[dict[str, Any]] | None = None
    ) -> None:
        super().__init__(
            message=message,
            status_code=422,
            detail={"errors": errors or []},
        )


class AuthenticationError(AppError):
    def __init__(self, message: str = "Not authenticated") -> None:
        super().__init__(message=message, status_code=401)


class PermissionError(AppError):
    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message=message, status_code=403)


class AIServiceError(AppError):
    def __init__(self, message: str = "AI service unavailable") -> None:
        super().__init__(message=message, status_code=503)


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Unified error response handler registered on the FastAPI app."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "status_code": exc.status_code,
                **exc.detail,
            }
        },
    )
