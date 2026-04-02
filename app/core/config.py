"""
app/core/config.py

Central configuration for the Finance Tracker application.
Uses environment variables with sensible defaults — ready for production.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application metadata
    APP_NAME: str = "Finance Tracker API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A production-style REST API for managing personal financial transactions "
        "with analytics and reporting capabilities."
    )
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./finance_tracker.db"

    # Pagination defaults
    DEFAULT_PAGE_LIMIT: int = 20
    MAX_PAGE_LIMIT: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


# Module-level singleton — import this everywhere
settings = Settings()
