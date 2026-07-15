"""Instagram scraper using Playwright."""

import asyncio
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from bs4 import BeautifulSoup
from loguru import logger

from instagram_monitor.core.settings import settings
from .base_scraper import BaseScraper


class InstagramScraper(BaseScraper):
    """Instagram scraper using Playwright for dynamic content."""

    BASE_URL = "https://www.instagram.com"

    def __init__(self):
        """Initialize Instagram scraper."""
        super().__init__()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()

    async def setup(self) -> None:
        """Setup Playwright browser."""
        try:
            playwright = await async_playwright().start()
            launch_args = {
                "headless": settings.PLAYWRIGHT_HEADLESS,
            }

            if settings.PROXY_URL:
                launch_args["proxy"] = {"server": settings.PROXY_URL}

            self.browser = await playwright.chromium.launch(**launch_args)
            self.context = await self.browser.new_context(
                user_agent=self.get_random_user_agent(),
            )
            logger.info("Playwright browser initialized")
        except Exception as e:
            logger.error(f"Failed to setup Playwright: {e}")
            raise

    async def cleanup(self) -> None:
        """Cleanup Playwright resources."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        logger.info("Playwright browser closed")

    async def scrape_profile(self, username: str) -> Optional[Dict[str, Any]]:
        """Scrape Instagram profile information."""
        if not self.context:
            logger.error("Browser not initialized")
            return None

        page = None
        try:
            page = await self.context.new_page()
            url = f"{self.BASE_URL}/{username}/"
            logger.info(f"Scraping profile: {username}")

            await page.goto(url, wait_until="networkidle", timeout=settings.PLAYWRIGHT_TIMEOUT)
            await asyncio.sleep(2)  # Wait for dynamic content

            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            # Extract profile data from JSON in page
            profile_data = await self._extract_profile_data(page, soup)
            logger.info(f"Successfully scraped profile: {username}")
            return profile_data

        except Exception as e:
            logger.error(f"Error scraping profile {username}: {e}")
            if page:
                await page.screenshot(path=self.take_screenshot(f"profile_error_{username}"))
            return None
        finally:
            if page:
                await page.close()

    async def scrape_posts(self, username: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Scrape Instagram posts."""
        if not self.context:
            logger.error("Browser not initialized")
            return []

        page = None
        posts = []
        try:
            page = await self.context.new_page()
            url = f"{self.BASE_URL}/{username}/"
            logger.info(f"Scraping posts for: {username}")

            await page.goto(url, wait_until="networkidle", timeout=settings.PLAYWRIGHT_TIMEOUT)
            await asyncio.sleep(2)

            # Scroll to load posts
            posts_loaded = 0
            while posts_loaded < limit:
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(1)
                posts_loaded += 1

            content = await page.content()
            posts = await self._extract_posts_data(content, limit)
            logger.info(f"Successfully scraped {len(posts)} posts for {username}")
            return posts

        except Exception as e:
            logger.error(f"Error scraping posts for {username}: {e}")
            if page:
                await page.screenshot(path=self.take_screenshot(f"posts_error_{username}"))
            return posts
        finally:
            if page:
                await page.close()

    async def scrape_reels(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Scrape Instagram reels."""
        if not self.context:
            logger.error("Browser not initialized")
            return []

        page = None
        reels = []
        try:
            page = await self.context.new_page()
            url = f"{self.BASE_URL}/{username}/reels/"
            logger.info(f"Scraping reels for: {username}")

            await page.goto(url, wait_until="networkidle", timeout=settings.PLAYWRIGHT_TIMEOUT)
            await asyncio.sleep(2)

            # Scroll to load reels
            for _ in range(limit // 3):
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(1)

            content = await page.content()
            reels = await self._extract_reels_data(content, limit)
            logger.info(f"Successfully scraped {len(reels)} reels for {username}")
            return reels

        except Exception as e:
            logger.error(f"Error scraping reels for {username}: {e}")
            if page:
                await page.screenshot(path=self.take_screenshot(f"reels_error_{username}"))
            return reels
        finally:
            if page:
                await page.close()

    async def _extract_profile_data(self, page: Page, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract profile data from page."""
        # This is a basic extraction - in production, you'd parse the JSON embedded in the page
        profile_data = {
            "username": None,
            "full_name": None,
            "bio": None,
            "followers": 0,
            "following": 0,
            "posts_count": 0,
            "verified": False,
            "profile_picture_url": None,
            "scraped_at": datetime.utcnow().isoformat(),
        }
        return profile_data

    async def _extract_posts_data(self, content: str, limit: int) -> List[Dict[str, Any]]:
        """Extract posts data from page content."""
        posts = []
        # Parse content and extract posts
        return posts

    async def _extract_reels_data(self, content: str, limit: int) -> List[Dict[str, Any]]:
        """Extract reels data from page content."""
        reels = []
        # Parse content and extract reels
        return reels
