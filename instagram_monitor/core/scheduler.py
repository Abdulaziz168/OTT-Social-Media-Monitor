"""Scheduler module for automated tasks."""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import asyncio

from loguru import logger
from instagram_monitor.core.settings import settings


class TaskScheduler:
    """Scheduler for automated monitoring tasks."""

    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = BackgroundScheduler()

    def schedule_daily_scrape(self, scrape_func, schedule_time: str = None):
        """Schedule daily scraping at specified time."""
        if not schedule_time:
            schedule_time = settings.SCHEDULE_TIME

        hour, minute = map(int, schedule_time.split(":"))

        try:
            trigger = CronTrigger(hour=hour, minute=minute)
            self.scheduler.add_job(
                scrape_func,
                trigger=trigger,
                id="daily_scrape",
                name="Daily Instagram Scrape",
                replace_existing=True,
            )
            logger.info(f"Scheduled daily scrape at {schedule_time}")
        except Exception as e:
            logger.error(f"Error scheduling scrape: {e}")
            raise

    def schedule_hourly_stats(self, stats_func):
        """Schedule hourly statistics update."""
        try:
            trigger = CronTrigger(minute=0)
            self.scheduler.add_job(
                stats_func,
                trigger=trigger,
                id="hourly_stats",
                name="Hourly Statistics Update",
                replace_existing=True,
            )
            logger.info("Scheduled hourly statistics update")
        except Exception as e:
            logger.error(f"Error scheduling stats: {e}")
            raise

    def schedule_weekly_report(self, report_func):
        """Schedule weekly report generation."""
        try:
            trigger = CronTrigger(day_of_week="mon", hour=10, minute=0)
            self.scheduler.add_job(
                report_func,
                trigger=trigger,
                id="weekly_report",
                name="Weekly Report Generation",
                replace_existing=True,
            )
            logger.info("Scheduled weekly report generation")
        except Exception as e:
            logger.error(f"Error scheduling report: {e}")
            raise

    def start(self):
        """Start the scheduler."""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}")
            raise

    def stop(self):
        """Stop the scheduler."""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

    def get_jobs(self):
        """Get all scheduled jobs."""
        return self.scheduler.get_jobs()

    def remove_job(self, job_id: str):
        """Remove a scheduled job."""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job: {job_id}")
        except Exception as e:
            logger.error(f"Error removing job: {e}")
