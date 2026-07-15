"""JSON export module."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from loguru import logger
from instagram_monitor.core.settings import settings
from instagram_monitor.database import Account, Post, Reel, DailyStatistics


class JSONExporter:
    """Export data to JSON format."""

    def __init__(self):
        """Initialize JSON exporter."""
        self.reports_dir = settings.REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    @staticmethod
    def _serialize_datetime(obj):
        """Serialize datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def export_accounts(self, accounts: List[Account], filename: Optional[str] = None) -> Path:
        """Export accounts to JSON."""
        if not filename:
            filename = f"accounts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_path = self.reports_dir / filename

        try:
            data = {
                "exported_at": datetime.now().isoformat(),
                "total_accounts": len(accounts),
                "accounts": [
                    {
                        "username": a.username,
                        "full_name": a.full_name,
                        "bio": a.bio,
                        "followers": a.followers,
                        "following": a.following,
                        "posts_count": a.posts_count,
                        "verified": a.verified,
                        "business_category": a.business_category,
                    }
                    for a in accounts
                ],
            }

            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=self._serialize_datetime, ensure_ascii=False)

            logger.info(f"Accounts exported to {export_path}")
            return export_path
        except Exception as e:
            logger.error(f"Error exporting accounts: {e}")
            raise

    def export_statistics(self, stats: List[DailyStatistics], filename: Optional[str] = None) -> Path:
        """Export statistics to JSON."""
        if not filename:
            filename = f"statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_path = self.reports_dir / filename

        try:
            data = {
                "exported_at": datetime.now().isoformat(),
                "total_records": len(stats),
                "statistics": [
                    {
                        "account_id": s.account_id,
                        "date": s.date.isoformat(),
                        "followers": s.followers,
                        "following": s.following,
                        "posts": s.posts_count,
                        "avg_likes": s.avg_likes,
                        "avg_comments": s.avg_comments,
                        "engagement_rate": s.avg_engagement,
                    }
                    for s in stats
                ],
            }

            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=self._serialize_datetime, ensure_ascii=False)

            logger.info(f"Statistics exported to {export_path}")
            return export_path
        except Exception as e:
            logger.error(f"Error exporting statistics: {e}")
            raise
