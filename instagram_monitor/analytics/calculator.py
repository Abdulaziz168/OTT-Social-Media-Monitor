"""Analytics calculator for metrics and insights."""

from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from loguru import logger
from instagram_monitor.database import DatabaseRepository, Account, DailyStatistics, Post, Reel


class AnalyticsCalculator:
    """Calculate analytics and metrics from scraped data."""

    def __init__(self, session: Session):
        """Initialize analytics calculator."""
        self.db = DatabaseRepository(session)

    def calculate_engagement_rate(self, likes: int, comments: int, followers: int) -> float:
        """Calculate engagement rate."""
        if followers == 0:
            return 0.0
        return ((likes + comments) / followers) * 100

    def calculate_growth_rate(self, current: int, previous: int) -> float:
        """Calculate growth rate percentage."""
        if previous == 0:
            return 0.0
        return ((current - previous) / previous) * 100

    def calculate_posting_frequency(self, account_id: int, days: int = 30) -> float:
        """Calculate average posts per day."""
        posts = self.db.get_statistics_range(account_id, days)
        if not posts:
            return 0.0
        total_posts = sum(p.posts_count or 0 for p in posts)
        return total_posts / days if days > 0 else 0.0

    def get_top_accounts_by_followers(self, limit: int = 5) -> List[Account]:
        """Get top accounts by follower count."""
        return self.db.get_top_accounts_by_followers(limit)

    def get_top_accounts_by_engagement(self, limit: int = 5) -> List[Tuple[Account, float]]:
        """Get top accounts by engagement rate."""
        accounts = self.db.get_all_accounts()
        engagement_rates = []
        
        for account in accounts:
            latest = self.db.get_latest_statistics(account.id)
            if latest and latest.avg_engagement:
                engagement_rates.append((account, latest.avg_engagement))
        
        return sorted(engagement_rates, key=lambda x: x[1], reverse=True)[:limit]

    def get_top_accounts_by_growth(self, days: int = 7, limit: int = 5) -> List[Tuple[Account, float]]:
        """Get top accounts by follower growth."""
        accounts = self.db.get_all_accounts()
        growth_rates = []
        
        for account in accounts:
            stats = self.db.get_statistics_range(account.id, days)
            if len(stats) >= 2:
                first_followers = stats[0].followers or 0
                last_followers = stats[-1].followers or 0
                growth = self.calculate_growth_rate(last_followers, first_followers)
                growth_rates.append((account, growth))
        
        return sorted(growth_rates, key=lambda x: x[1], reverse=True)[:limit]

    def get_inactive_accounts(self, days: int = 7) -> List[Account]:
        """Get accounts without posts in N days."""
        accounts = self.db.get_all_accounts()
        inactive = []
        
        for account in accounts:
            latest = self.db.get_latest_statistics(account.id)
            if latest and latest.days_since_last_post and latest.days_since_last_post > days:
                inactive.append(account)
        
        return inactive

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall summary statistics."""
        accounts = self.db.get_all_accounts()
        
        total_followers = sum(a.followers or 0 for a in accounts)
        total_posts = sum(a.posts_count or 0 for a in accounts)
        
        return {
            "total_accounts": len(accounts),
            "total_followers": total_followers,
            "total_posts": total_posts,
            "average_followers": total_followers // len(accounts) if accounts else 0,
            "average_posts": total_posts // len(accounts) if accounts else 0,
        }
