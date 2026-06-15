"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Data Analyst"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/analyst"

    # Auth
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 60

    # AI Provider
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # File uploads
    max_upload_size_mb: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
