"""Application settings and configuration management."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    CONFIG_DIR: Path = PROJECT_ROOT / "config"
    DATA_DIR: Path = PROJECT_ROOT / "data"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports"

    # Database
    DATABASE_PATH: Path = DATA_DIR / "instagram_monitor.db"
    DATABASE_URL: str = ""

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    # Playwright
    PLAYWRIGHT_HEADLESS: bool = True
    PLAYWRIGHT_TIMEOUT: int = 30000  # milliseconds
    PLAYWRIGHT_STEALTH: bool = True

    # Proxy (optional)
    PROXY_URL: Optional[str] = None

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_PATH: Path = LOGS_DIR

    # Scheduling
    SCHEDULE_TIME: str = "09:00"

    # Instagram Scraper
    INSTAGRAM_MAX_RETRIES: int = 3
    INSTAGRAM_RETRY_DELAY: int = 2
    INSTAGRAM_TIMEOUT: int = 30
    INSTAGRAM_LOAD_POSTS: int = 20

    # Features
    GENERATE_EXCEL: bool = True
    GENERATE_TELEGRAM: bool = True
    GENERATE_DASHBOARD: bool = True
    SEND_TELEGRAM_REPORT: bool = True

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __init__(self, **data):
        """Initialize settings and create necessary directories."""
        super().__init__(**data)
        self._ensure_directories()
        self._set_database_url()

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [self.DATA_DIR, self.LOGS_DIR, self.REPORTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    def _set_database_url(self) -> None:
        """Set SQLite database URL."""
        self.DATABASE_URL = f"sqlite:///{self.DATABASE_PATH}"


# Global settings instance
settings = Settings()
