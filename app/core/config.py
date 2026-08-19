# This file contains the application settings and configuration loaded from environment variables.
from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Application settings class that loads configuration from environment variables.
class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "BuddyLearnAI"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production", "test"] = "development"
    debug: bool = True

    api_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    database_url: str = "postgresql+psycopg://buddylearn:buddylearn@localhost:5432/buddylearn"
    redis_url: str = "redis://localhost:6379/0"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None

    openai_api_key: str | None = None

    access_token_expire_minutes: int = 60
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="BUDDYLEARN_",
        extra="ignore",
    )

# Function to get the application settings with caching to avoid reloading from environment variables multiple times.
@lru_cache
def get_settings() -> Settings:
    return Settings()
