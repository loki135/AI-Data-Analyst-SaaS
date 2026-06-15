"""FastAPI application entry-point."""

from __future__ import annotations

from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
