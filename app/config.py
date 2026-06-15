"""Application configuration."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Global application settings."""

    app_name: str = "AI Data Analyst"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    max_upload_size_mb: int = 50
    allowed_extensions: list[str] = Field(
        default_factory=lambda: [".csv", ".json", ".xlsx", ".xls"]
    )

    def is_extension_allowed(self, filename: str) -> bool:
        """Check whether *filename* has an allowed extension."""
        return any(filename.lower().endswith(ext) for ext in self.allowed_extensions)

    def max_upload_bytes(self) -> int:
        """Return the upload-size limit in bytes."""
        return self.max_upload_size_mb * 1024 * 1024


settings = Settings()
