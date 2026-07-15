"""Database repository for CRUD operations."""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from loguru import logger
from .models import (
    Account,
    DailyStatistics,
    Post,
    Reel,
    Story,
    AccountHistory,
    ReportLog,
)


class DatabaseRepository:
    """Repository for database operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    # ============ ACCOUNT OPERATIONS ============

    def get_or_create_account(self, username: str, full_name: str = None) -> Account:
        """Get existing account or create new one."""
        account = self.session.query(Account).filter_by(username=username).first()
        if not account:
            account = Account(username=username, full_name=full_name)
            self.session.add(account)
            self.session.commit()
            logger.info(f"Created new account: {username}")
        return account

    def update_account(self, username: str, **kwargs) -> Account:
        """Update account information."""
        account = self.session.query(Account).filter_by(username=username).first()
        if account:
            for key, value in kwargs.items():
                if hasattr(account, key):
                    setattr(account, key, value)
            account.updated_at = datetime.utcnow()
            self.session.commit()
            logger.info(f"Updated account: {username}")
        return account

    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Get account by username."""
        return self.session.query(Account).filter_by(username=username).first()

    def get_all_accounts(self, only_active: bool = True) -> List[Account]:
        """Get all accounts."""
        query = self.session.query(Account)
        if only_active:
            query = query.filter_by(is_active=True)
        return query.all()

    def get_account_count(self) -> int:
        """Get total number of accounts."""
        return self.session.query(func.count(Account.id)).scalar()

    # ============ DAILY STATISTICS OPERATIONS ============

    def add_daily_statistics(self, account_id: int, **kwargs) -> DailyStatistics:
        """Add daily statistics record."""
        stats = DailyStatistics(account_id=account_id, date=datetime.utcnow(), **kwargs)
        self.session.add(stats)
        self.session.commit()
        return stats

    def get_latest_statistics(self, account_id: int) -> Optional[DailyStatistics]:
        """Get latest statistics for account."""
        return (
            self.session.query(DailyStatistics)
            .filter_by(account_id=account_id)
            .order_by(DailyStatistics.date.desc())
            .first()
        )

    def get_statistics_range(
        self, account_id: int, days: int = 30
    ) -> List[DailyStatistics]:
        """Get statistics for last N days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        return (
            self.session.query(DailyStatistics)
            .filter(
                DailyStatistics.account_id == account_id,
                DailyStatistics.date >= start_date,
            )
            .order_by(DailyStatistics.date)
            .all()
        )

    # ============ POST OPERATIONS ============

    def add_post(self, account_id: int, post_url: str, **kwargs) -> Post:
        """Add new post."""
        # Check if post already exists
        existing = self.session.query(Post).filter_by(post_url=post_url).first()
        if existing:
            # Update existing post
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.session.commit()
            return existing

        post = Post(account_id=account_id, post_url=post_url, **kwargs)
        self.session.add(post)
        self.session.commit()
        return post

    def get_posts_by_account(
        self, account_id: int, limit: int = 20, skip_deleted: bool = True
    ) -> List[Post]:
        """Get posts for account."""
        query = self.session.query(Post).filter_by(account_id=account_id)
        if skip_deleted:
            query = query.filter_by(is_deleted=False)
        return query.order_by(Post.published_date.desc()).limit(limit).all()

    def get_post_count(self, account_id: int, skip_deleted: bool = True) -> int:
        """Get post count for account."""
        query = self.session.query(func.count(Post.id)).filter_by(account_id=account_id)
        if skip_deleted:
            query = query.filter(Post.is_deleted == False)
        return query.scalar()

    # ============ REEL OPERATIONS ============

    def add_reel(self, account_id: int, reel_url: str, **kwargs) -> Reel:
        """Add new reel."""
        existing = self.session.query(Reel).filter_by(reel_url=reel_url).first()
        if existing:
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.updated_at = datetime.utcnow()
            self.session.commit()
            return existing

        reel = Reel(account_id=account_id, reel_url=reel_url, **kwargs)
        self.session.add(reel)
        self.session.commit()
        return reel

    def get_reels_by_account(
        self, account_id: int, limit: int = 20, skip_deleted: bool = True
    ) -> List[Reel]:
        """Get reels for account."""
        query = self.session.query(Reel).filter_by(account_id=account_id)
        if skip_deleted:
            query = query.filter_by(is_deleted=False)
        return query.order_by(Reel.published_date.desc()).limit(limit).all()

    def get_most_viewed_reel(self, account_id: int = None) -> Optional[Reel]:
        """Get most viewed reel(s)."""
        query = self.session.query(Reel)
        if account_id:
            query = query.filter_by(account_id=account_id)
        return query.order_by(Reel.views.desc()).first()

    # ============ STORY OPERATIONS ============

    def add_story(self, account_id: int, story_id: str, **kwargs) -> Story:
        """Add new story."""
        existing = self.session.query(Story).filter_by(story_id=story_id).first()
        if existing:
            return existing

        story = Story(account_id=account_id, story_id=story_id, **kwargs)
        self.session.add(story)
        self.session.commit()
        return story

    def get_stories_by_account(self, account_id: int, limit: int = 50) -> List[Story]:
        """Get stories for account."""
        return (
            self.session.query(Story)
            .filter_by(account_id=account_id, is_deleted=False)
            .order_by(Story.published_date.desc())
            .limit(limit)
            .all()
        )

    # ============ ACCOUNT HISTORY OPERATIONS ============

    def add_history_record(self, account_id: int, **kwargs) -> AccountHistory:
        """Add account history record."""
        history = AccountHistory(account_id=account_id, **kwargs)
        self.session.add(history)
        self.session.commit()
        return history

    def get_account_history(
        self, account_id: int, days: int = 30
    ) -> List[AccountHistory]:
        """Get account history for N days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        return (
            self.session.query(AccountHistory)
            .filter(
                AccountHistory.account_id == account_id,
                AccountHistory.timestamp >= start_date,
            )
            .order_by(AccountHistory.timestamp)
            .all()
        )

    # ============ REPORT LOG OPERATIONS ============

    def log_report(self, report_type: str, **kwargs) -> ReportLog:
        """Log report generation."""
        log = ReportLog(report_type=report_type, report_date=datetime.utcnow(), **kwargs)
        self.session.add(log)
        self.session.commit()
        return log

    def get_report_logs(self, report_type: str = None, days: int = 7) -> List[ReportLog]:
        """Get report logs."""
        start_date = datetime.utcnow() - timedelta(days=days)
        query = self.session.query(ReportLog).filter(ReportLog.created_at >= start_date)
        if report_type:
            query = query.filter_by(report_type=report_type)
        return query.order_by(ReportLog.created_at.desc()).all()

    # ============ ANALYTICS ============

    def get_top_accounts_by_followers(self, limit: int = 5) -> List[Account]:
        """Get top accounts by followers."""
        return self.session.query(Account).order_by(Account.followers.desc()).limit(limit).all()

    def get_top_accounts_by_engagement(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top accounts by engagement."""
        # Calculate engagement as average across recent posts/reels
        pass

    def get_top_accounts_by_growth(self, days: int = 7, limit: int = 5):
        """Get top accounts by follower growth."""
        pass

    def get_inactive_accounts(self, days: int = 7) -> List[Account]:
        """Get accounts inactive for N days."""
        pass

    def close(self) -> None:
        """Close database session."""
        self.session.close()
