"""Shared API response utilities.

Provides a consistent envelope for all API responses, eliminating
duplicated response-formatting code across route handlers.
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int


class ApiResponse(BaseModel, Generic[T]):
    """Standard envelope for all successful API responses."""

    success: bool = True
    data: T
    meta: dict[str, Any] | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard envelope for paginated list responses."""

    success: bool = True
    data: list[T]
    pagination: PaginationMeta


def ok(data: Any, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Shorthand to build a successful response dict."""
    resp: dict[str, Any] = {"success": True, "data": data}
    if meta:
        resp["meta"] = meta
    return resp


def paginated(
    items: list[Any],
    page: int,
    per_page: int,
    total: int,
) -> dict[str, Any]:
    """Shorthand to build a paginated response dict."""
    return {
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
        },
    }
