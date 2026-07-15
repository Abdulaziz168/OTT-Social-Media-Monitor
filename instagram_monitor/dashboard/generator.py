"""HTML dashboard generator."""

from pathlib import Path
from datetime import datetime
from typing import List, Optional
import json

from jinja2 import Template
from loguru import logger
from instagram_monitor.core.settings import settings
from instagram_monitor.database import Account, DailyStatistics


class DashboardGenerator:
    """Generate HTML dashboard."""

    HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTT Instagram Monitor Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            line-height: 1.6;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .timestamp {
            opacity: 0.9;
            font-size: 0.9em;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #1a1a1a;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            transition: transform 0.3s ease;
        }
        .stat-card:hover {
            transform: translateY(-5px);
        }
        .stat-label {
            color: #999;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #fff;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #1a1a1a;
            border-radius: 8px;
            overflow: hidden;
        }
        th {
            background: #222;
            padding: 15px;
            text-align: left;
            color: #667eea;
            font-weight: 600;
        }
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #2a2a2a;
        }
        tr:hover {
            background: #2a2a2a;
        }
        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 OTT Instagram Monitor</h1>
            <div class="timestamp">Generated: {{ generated_at }}</div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Accounts</div>
                <div class="stat-value">{{ total_accounts }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Followers</div>
                <div class="stat-value">{{ total_followers | format_number }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Posts</div>
                <div class="stat-value">{{ total_posts | format_number }}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Followers</div>
                <div class="stat-value">{{ avg_followers | format_number }}</div>
            </div>
        </div>

        <h2 style="margin: 30px 0 20px 0; font-size: 1.5em;">Top Accounts by Followers</h2>
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Followers</th>
                    <th>Following</th>
                    <th>Posts</th>
                    <th>Verified</th>
                </tr>
            </thead>
            <tbody>
                {% for account in top_accounts %}
                <tr>
                    <td><strong>{{ account.username }}</strong></td>
                    <td>{{ account.followers | format_number }}</td>
                    <td>{{ account.following | format_number }}</td>
                    <td>{{ account.posts_count | format_number }}</td>
                    <td>{% if account.verified %}✓{% else %}✗{% endif %}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            <p>&copy; 2026 OTT Instagram Monitor - Production Ready</p>
        </div>
    </div>
</body>
</html>
    """

    def __init__(self):
        """Initialize dashboard generator."""
        self.reports_dir = settings.REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

    def generate_dashboard(
        self,
        accounts: List[Account],
        statistics: Optional[List[DailyStatistics]] = None,
        filename: Optional[str] = None,
    ) -> Path:
        """Generate HTML dashboard."""
        if not filename:
            filename = f"dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        dashboard_path = self.reports_dir / filename

        try:
            # Calculate statistics
            total_accounts = len(accounts)
            total_followers = sum(a.followers or 0 for a in accounts)
            total_posts = sum(a.posts_count or 0 for a in accounts)
            avg_followers = (
                total_followers // total_accounts if total_accounts > 0 else 0
            )

            # Sort accounts by followers
            top_accounts = sorted(
                accounts, key=lambda x: x.followers or 0, reverse=True
            )[:10]

            # Create Jinja2 template
            template = Template(self.HTML_TEMPLATE)

            # Add custom filters
            template.globals["format_number"] = lambda x: f"{x:,}" if x else "0"

            # Render template
            html_content = template.render(
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_accounts=total_accounts,
                total_followers=total_followers,
                total_posts=total_posts,
                avg_followers=avg_followers,
                top_accounts=top_accounts,
            )

            # Write to file
            dashboard_path.write_text(html_content, encoding="utf-8")
            logger.info(f"Dashboard saved to {dashboard_path}")
            return dashboard_path

        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
            raise
