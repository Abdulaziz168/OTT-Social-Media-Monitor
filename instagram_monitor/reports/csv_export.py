"""CSV export module."""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from loguru import logger
from instagram_monitor.core.settings import settings
from instagram_monitor.database import Account, Post, Reel, DailyStatistics


class CSVExporter:
    """Export data to CSV format."""

    def __init__(self):
        """Initialize CSV exporter."""
        self.reports_dir = settings.REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    def export_accounts(
        self, accounts: List[Account], filename: Optional[str] = None
    ) -> Path:
        """Export accounts to CSV."""
        if not filename:
            filename = f"accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        export_path = self.reports_dir / filename

        try:
            with open(export_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Username",
                        "Full Name",
                        "Bio",
                        "Followers",
                        "Following",
                        "Posts",
                        "Verified",
                        "Category",
                    ]
                )
                for account in accounts:
                    writer.writerow(
                        [
                            account.username,
                            account.full_name or "",
                            account.bio or "",
                            account.followers or 0,
                            account.following or 0,
                            account.posts_count or 0,
                            "Yes" if account.verified else "No",
                            account.business_category or "",
                        ]
                    )
            logger.info(f"Accounts exported to {export_path}")
            return export_path
        except Exception as e:
            logger.error(f"Error exporting accounts: {e}")
            raise

    def export_posts(self, posts: List[Post], filename: Optional[str] = None) -> Path:
        """Export posts to CSV."""
        if not filename:
            filename = f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        export_path = self.reports_dir / filename

        try:
            with open(export_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "URL",
                        "Published Date",
                        "Likes",
                        "Comments",
                        "Views",
                        "Media Type",
                    ]
                )
                for post in posts:
                    writer.writerow(
                        [
                            post.post_url,
                            post.published_date or "",
                            post.likes or 0,
                            post.comments or 0,
                            post.views or 0,
                            post.media_type or "",
                        ]
                    )
            logger.info(f"Posts exported to {export_path}")
            return export_path
        except Exception as e:
            logger.error(f"Error exporting posts: {e}")
            raise
