"""Base scraper with common functionality."""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from loguru import logger
from fake_useragent import UserAgent

from instagram_monitor.core.settings import settings


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self):
        """Initialize base scraper."""
        self.ua = UserAgent()
        self.max_retries = settings.INSTAGRAM_MAX_RETRIES
        self.retry_delay = settings.INSTAGRAM_RETRY_DELAY
        self.timeout = settings.INSTAGRAM_TIMEOUT
        self.screenshots_dir = settings.DATA_DIR / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)

    def get_random_user_agent(self) -> str:
        """Get random user agent."""
        return self.ua.random

    def take_screenshot(self, name: str) -> Path:
        """Take screenshot for debugging."""
        screenshot_path = self.screenshots_dir / f"{name}_{datetime.now().timestamp()}.png"
        logger.info(f"Screenshot saved to {screenshot_path}")
        return screenshot_path

    async def retry_operation(
        self,
        operation,
        *args,
        **kwargs
    ) -> Optional[Any]:
        """Retry operation with exponential backoff."""
        for attempt in range(self.max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Operation failed after {self.max_retries} retries: {e}")
                    return None
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
                await asyncio.sleep(wait_time)
        return None

    @abstractmethod
    async def scrape_profile(self, username: str) -> Dict[str, Any]:
        """Scrape profile information."""
        pass

    @abstractmethod
    async def scrape_posts(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Scrape posts."""
        pass
