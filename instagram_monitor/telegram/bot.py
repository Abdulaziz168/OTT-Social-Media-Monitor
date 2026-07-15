"""Telegram bot for sending reports."""

from typing import Optional
from pathlib import Path

from loguru import logger
from telegram import Bot
from telegram.error import TelegramError

from instagram_monitor.core.settings import settings


class TelegramBot:
    """Telegram bot for sending reports and notifications."""

    def __init__(self):
        """Initialize Telegram bot."""
        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            logger.warning("Telegram bot token or chat ID not configured")
            self.bot = None
            self.chat_id = None
        else:
            self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            self.chat_id = settings.TELEGRAM_CHAT_ID

    async def send_message(self, message: str, parse_mode: str = "Markdown") -> bool:
        """Send text message to Telegram."""
        if not self.bot or not self.chat_id:
            logger.warning("Telegram bot not configured")
            return False

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode,
            )
            logger.info("Message sent to Telegram")
            return True
        except TelegramError as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    async def send_document(
        self,
        file_path: Path,
        caption: Optional[str] = None,
    ) -> bool:
        """Send file to Telegram."""
        if not self.bot or not self.chat_id:
            logger.warning("Telegram bot not configured")
            return False

        try:
            with open(file_path, "rb") as f:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=f,
                    caption=caption,
                )
            logger.info(f"Document sent to Telegram: {file_path.name}")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram document: {e}")
            return False
