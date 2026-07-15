"""Data processor for analytics."""

import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta

from loguru import logger
from instagram_monitor.database import Account, DailyStatistics, Post, Reel


class DataProcessor:
    """Process data for reports and visualizations."""

    @staticmethod
    def accounts_to_dataframe(accounts: List[Account]) -> pd.DataFrame:
        """Convert accounts to DataFrame."""
        data = [
            {
                "username": a.username,
                "full_name": a.full_name,
                "followers": a.followers,
                "following": a.following,
                "posts": a.posts_count,
                "verified": a.verified,
            }
            for a in accounts
        ]
        return pd.DataFrame(data)

    @staticmethod
    def statistics_to_dataframe(stats: List[DailyStatistics]) -> pd.DataFrame:
        """Convert statistics to DataFrame."""
        data = [
            {
                "date": s.date,
                "followers": s.followers,
                "following": s.following,
                "posts": s.posts_count,
                "avg_likes": s.avg_likes,
                "avg_comments": s.avg_comments,
                "engagement": s.avg_engagement,
            }
            for s in stats
        ]
        return pd.DataFrame(data)

    @staticmethod
    def posts_to_dataframe(posts: List[Post]) -> pd.DataFrame:
        """Convert posts to DataFrame."""
        data = [
            {
                "url": p.post_url,
                "date": p.published_date,
                "likes": p.likes,
                "comments": p.comments,
                "media_type": p.media_type,
                "views": p.views,
            }
            for p in posts
        ]
        return pd.DataFrame(data)

    @staticmethod
    def reels_to_dataframe(reels: List[Reel]) -> pd.DataFrame:
        """Convert reels to DataFrame."""
        data = [
            {
                "url": r.reel_url,
                "date": r.published_date,
                "views": r.views,
                "likes": r.likes,
                "comments": r.comments,
                "shares": r.shares,
                "saves": r.saves,
            }
            for r in reels
        ]
        return pd.DataFrame(data)
