"""Main CLI application."""

import asyncio
from pathlib import Path
from datetime import datetime

import typer
from rich.console import Console
from rich.table import Table
from loguru import logger

from instagram_monitor.core import settings
from instagram_monitor.database import init_database, get_session
from instagram_monitor.utils import ConfigLoader
from instagram_monitor.scrapers import InstagramScraper
from instagram_monitor.reports import ExcelReportGenerator, TelegramReportGenerator
from instagram_monitor.telegram import TelegramBot
from instagram_monitor.analytics import AnalyticsCalculator

app = typer.Typer(
    name="OTT Instagram Monitor",
    help="Monitor OTT social media accounts in Uzbekistan",
)
console = Console()


@app.command()
def scrape(
    username: str = typer.Option(None, help="Specific username to scrape"),
    posts: bool = typer.Option(True, help="Scrape posts"),
    reels: bool = typer.Option(True, help="Scrape reels"),
) -> None:
    """Scrape Instagram accounts."""
    console.print("[bold blue]Starting Instagram scrape...[/bold blue]")
    init_database()
    
    config_loader = ConfigLoader()
    accounts = config_loader.load_accounts()
    
    if username:
        accounts = [a for a in accounts if a.get("username") == username]
    
    if not accounts:
        console.print("[bold red]No accounts to scrape[/bold red]")
        return
    
    console.print(f"[green]Found {len(accounts)} account(s) to scrape[/green]")


@app.command()
def report(
    excel: bool = typer.Option(True, help="Generate Excel report"),
    telegram_msg: bool = typer.Option(True, help="Generate Telegram report"),
) -> None:
    """Generate reports."""
    console.print("[bold blue]Generating reports...[/bold blue]")
    init_database()
    
    if excel:
        excel_gen = ExcelReportGenerator()
        report_path = excel_gen.generate_report([], [])
        console.print(f"[green]✓ Excel report saved to {report_path}[/green]")
    
    if telegram_msg:
        tg_gen = TelegramReportGenerator()
        content = tg_gen.generate_report([])
        report_path = tg_gen.save_report(content)
        console.print(f"[green]✓ Telegram report saved to {report_path}[/green]")


@app.command()
async def telegram() -> None:
    """Send report to Telegram."""
    console.print("[bold blue]Sending Telegram report...[/bold blue]")
    init_database()
    
    bot = TelegramBot()
    tg_gen = TelegramReportGenerator()
    
    content = tg_gen.generate_report([])
    success = await bot.send_message(content)
    
    if success:
        console.print("[green]✓ Report sent to Telegram[/green]")
    else:
        console.print("[red]✗ Failed to send Telegram report[/red]")


@app.command()
def stats() -> None:
    """Show statistics."""
    console.print("[bold blue]Loading statistics...[/bold blue]")
    init_database()
    
    session = get_session()
    calc = AnalyticsCalculator(session)
    summary = calc.get_summary_stats()
    
    table = Table(title="Summary Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    
    for key, value in summary.items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)
    session.close()


@app.command()
def schedule() -> None:
    """Start scheduler for automated scraping."""
    console.print("[bold blue]Starting scheduler...[/bold blue]")
    console.print(f"Scheduled time: {settings.SCHEDULE_TIME}")
    console.print("[yellow]Press Ctrl+C to stop[/yellow]")
    
    try:
        while True:
            asyncio.run(asyncio.sleep(1))
    except KeyboardInterrupt:
        console.print("\n[yellow]Scheduler stopped[/yellow]")


@app.command()
def init() -> None:
    """Initialize database."""
    console.print("[bold blue]Initializing database...[/bold blue]")
    init_database()
    console.print("[green]✓ Database initialized[/green]")


@app.command()
def config_show() -> None:
    """Show loaded configuration."""
    console.print("[bold blue]OTT Instagram Monitor Configuration[/bold blue]")
    
    config_loader = ConfigLoader()
    accounts = config_loader.load_accounts()
    
    table = Table(title=f"Loaded Accounts ({len(accounts)})")
    table.add_column("Username", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Enabled", style="yellow")
    
    for account in accounts:
        table.add_row(
            account.get("username", "N/A"),
            account.get("name", "N/A"),
            account.get("category", "N/A"),
            "✓" if account.get("enabled", True) else "✗",
        )
    
    console.print(table)


if __name__ == "__main__":
    app()
