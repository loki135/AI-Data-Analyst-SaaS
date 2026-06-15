"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analyses, auth, datasets
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]

# Routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(datasets.router, prefix="/api/v1")
app.include_router(analyses.router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
