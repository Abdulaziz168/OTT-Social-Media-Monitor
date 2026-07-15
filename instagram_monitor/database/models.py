"""SQLAlchemy ORM models for Instagram monitoring data."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Account(Base):
    """Instagram account model."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    bio = Column(Text)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    profile_picture_url = Column(String(512))
    verified = Column(Boolean, default=False)
    external_website = Column(String(512))
    business_category = Column(String(255))
    account_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    daily_statistics = relationship("DailyStatistics", back_populates="account", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="account", cascade="all, delete-orphan")
    reels = relationship("Reel", back_populates="account", cascade="all, delete-orphan")
    stories = relationship("Story", back_populates="account", cascade="all, delete-orphan")
    history = relationship("AccountHistory", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Account(username={self.username}, followers={self.followers})>"


class DailyStatistics(Base):
    """Daily statistics for each account."""

    __tablename__ = "daily_statistics"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    followers = Column(Integer)
    following = Column(Integer)
    posts_count = Column(Integer)
    avg_likes = Column(Float)
    avg_comments = Column(Float)
    avg_engagement = Column(Float)
    posting_frequency = Column(Float)
    days_since_last_post = Column(Integer)
    total_posts_scraped = Column(Integer)
    total_reels_scraped = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="daily_statistics")

    def __repr__(self) -> str:
        return f"<DailyStatistics(account_id={self.account_id}, date={self.date})>"


class Post(Base):
    """Instagram post model."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    post_url = Column(String(512), unique=True, nullable=False, index=True)
    published_date = Column(DateTime)
    caption = Column(Text)
    hashtags = Column(JSON)  # List of hashtags
    mentions = Column(JSON)  # List of mentions
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    media_type = Column(String(50))  # image, video, carousel
    views = Column(Integer)
    video_duration = Column(Float)
    thumbnail_url = Column(String(512))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post(url={self.post_url}, likes={self.likes})>"


class Reel(Base):
    """Instagram reel model."""

    __tablename__ = "reels"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    reel_url = Column(String(512), unique=True, nullable=False, index=True)
    published_date = Column(DateTime)
    caption = Column(Text)
    hashtags = Column(JSON)
    mentions = Column(JSON)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    video_duration = Column(Float)
    thumbnail_url = Column(String(512))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="reels")

    def __repr__(self) -> str:
        return f"<Reel(url={self.reel_url}, views={self.views})>"


class Story(Base):
    """Instagram story model (if public)."""

    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    story_id = Column(String(255), unique=True, nullable=False, index=True)
    published_date = Column(DateTime)
    media_type = Column(String(50))
    views = Column(Integer, default=0)
    thumbnail_url = Column(String(512))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    account = relationship("Account", back_populates="stories")

    def __repr__(self) -> str:
        return f"<Story(id={self.story_id}, views={self.views})>"


class AccountHistory(Base):
    """Historical tracking of account changes."""

    __tablename__ = "account_history"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    followers = Column(Integer)
    following = Column(Integer)
    posts_count = Column(Integer)
    follower_change = Column(Integer)
    following_change = Column(Integer)
    posts_change = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    account = relationship("Account", back_populates="history")

    def __repr__(self) -> str:
        return f"<AccountHistory(account_id={self.account_id}, followers_change={self.follower_change})>"


class ReportLog(Base):
    """Tracking of generated reports."""

    __tablename__ = "report_logs"

    id = Column(Integer, primary_key=True)
    report_type = Column(String(50))  # excel, telegram, dashboard, pdf
    report_date = Column(DateTime, nullable=False, index=True)
    file_path = Column(String(512))
    status = Column(String(50))  # success, failed, partial
    error_message = Column(Text)
    accounts_scraped = Column(Integer)
    accounts_failed = Column(Integer)
    execution_time_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ReportLog(type={self.report_type}, date={self.report_date}, status={self.status})>"
