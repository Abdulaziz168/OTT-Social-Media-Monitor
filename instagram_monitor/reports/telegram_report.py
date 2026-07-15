"""Telegram report generator."""

from pathlib import Path
from datetime import datetime
from typing import List, Optional

from loguru import logger
from instagram_monitor.core.settings import settings
from instagram_monitor.database import Account


class TelegramReportGenerator:
    """Generate Telegram-formatted reports."""

    EMOJIS = {
        "chart": "📊",
        "up": "📈",
        "down": "📉",
        "users": "👥",
        "posts": "📸",
        "video": "🎬",
        "fire": "🔥",
        "warning": "⚠️",
        "check": "✅",
    }

    def __init__(self):
        """Initialize Telegram report generator."""
        self.reports_dir = settings.REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    def generate_report(self, accounts: List[Account]) -> str:
        """Generate Telegram-formatted report."""
        report = []
        report.append(f"{self.EMOJIS['chart']} OTT Instagram Report")
        report.append(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append(f"{self.EMOJIS['users']} Total Accounts: {len(accounts)}")
        
        total_followers = sum(a.followers or 0 for a in accounts)
        report.append(f"{self.EMOJIS['users']} Total Followers: {total_followers:,}")
        
        markdown = "\n".join(report)
        logger.info(f"Telegram report generated")
        return markdown

    def save_report(self, content: str, filename: Optional[str] = None) -> Path:
        """Save Telegram report to file."""
        if not filename:
            filename = f"telegram_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report_path = self.reports_dir / filename
        
        try:
            report_path.write_text(content, encoding="utf-8")
            logger.info(f"Telegram report saved to {report_path}")
            return report_path
        except Exception as e:
            logger.error(f"Error saving Telegram report: {e}")
            raise
