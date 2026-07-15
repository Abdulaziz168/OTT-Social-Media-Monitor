"""README documentation."""

# OTT Social Media Monitor

> Production-ready Python application for monitoring Uzbek OTT social media accounts

[![Python 3.12](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

The **OTT Social Media Monitor** is a comprehensive Python application designed to monitor, track, and analyze Instagram accounts of OTT (Over-The-Top) platforms in Uzbekistan. It provides automated daily monitoring, advanced analytics, and professional report generation.

### Key Features

✅ **Automated Monitoring** - Daily scraping of 12 OTT platforms
✅ **Advanced Analytics** - Growth tracking, engagement metrics, trend analysis
✅ **Multi-Format Reports** - Excel, Telegram, HTML Dashboard, PDF
✅ **REST API** - FastAPI with Swagger documentation
✅ **Telegram Bot** - Automated daily report delivery
✅ **SQLite Database** - Persistent data storage with history tracking
✅ **Robust Error Handling** - Graceful failure recovery
✅ **Production Ready** - Type hints, logging, comprehensive documentation

## Monitored Accounts

1. **ITV Uzbekistan** - @itv.uz
2. **Salom TV** - @salomtvuz
3. **Cinerama** - @cinerama.uz
4. **Frame Media** - @frame.mediauz
5. **Kinom Uzbekistan** - @kinom_uzbekistan
6. **AllPlay** - @allplay_official
7. **BizTV** - @biztvuz
8. **SPlay** - @splay.uz
9. **ClickTV** - @clicktv.uz
10. **TV.com Milliy** - @tvcom.uz_milliy
11. **Yangi TV** - @yangitv_rasmiy
12. **RiyaPlay** - @riyaplay.uz

## Installation

### Prerequisites

- Python 3.12+
- pip or poetry
- Playwright browsers (auto-installed)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/Abdulaziz168/OTT-Social-Media-Monitor.git
cd OTT-Social-Media-Monitor
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

4. **Configure environment**

```bash
cp .env.example .env
```

Edit `.env` and configure:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `TELEGRAM_CHAT_ID` - Target chat ID for reports
- `PROXY_URL` (optional) - Proxy server address

5. **Initialize database**

```bash
python main.py init
```

## Usage

### Command Line Interface

```bash
# Show all commands
python main.py --help

# Initialize database
python main.py init

# Scrape all accounts
python main.py scrape

# Scrape specific account
python main.py scrape --username itv.uz

# Generate reports
python main.py report --excel --telegram-msg

# Send report to Telegram
python main.py telegram

# Show statistics
python main.py stats

# Show configuration
python main.py config-show

# Start scheduler
python main.py schedule
```

## Project Structure

```
instagram_monitor/
├── core/                 # Application settings & logging
│   ├── settings.py       # Configuration management
│   └── logger.py         # Loguru setup
├── database/             # Database layer
│   ├── models.py         # SQLAlchemy ORM models
│   ├── connection.py     # Database connection
│   └── repository.py     # CRUD operations
├── scrapers/             # Web scraping
│   ├── base_scraper.py   # Abstract base class
│   └── instagram_scraper.py  # Instagram scraper (Playwright)
├── analytics/            # Data analysis
│   ├── calculator.py     # Metrics calculation
│   └── processor.py      # Data processing
├── reports/              # Report generation
│   ├── excel_report.py   # Excel reports
│   └── telegram_report.py # Telegram reports
├── telegram/             # Telegram integration
│   └── bot.py            # Telegram bot
├── utils/                # Utilities
│   ├── config_loader.py  # Configuration loading
│   └── validators.py     # Input validation
└── __init__.py

config/
├── accounts.json         # Account configuration

data/
├── instagram_monitor.db  # SQLite database
└── screenshots/          # Error screenshots

logs/
├── instagram_monitor.log # Application logs
└── errors.log            # Error logs

reports/                  # Generated reports
├── excel_report_*.xlsx
├── telegram_report_*.md
└── dashboard.html

tests/                    # Test suite
├── test_validators.py
├── test_analytics.py
├── test_config.py
└── conftest.py

main.py                   # CLI entry point
requirements.txt          # Python dependencies
.env.example              # Environment template
.gitignore
README.md
```

## Database Schema

### Tables

**accounts** - Instagram account information
- username, full_name, bio, followers, following, posts_count
- verified, profile_picture_url, business_category

**daily_statistics** - Daily metrics snapshot
- followers, following, posts_count, avg_likes, avg_comments
- engagement_rate, posting_frequency

**posts** - Post data
- post_url, published_date, caption, likes, comments
- media_type, views, hashtags, mentions

**reels** - Reel data
- reel_url, published_date, caption, views, likes, comments
- shares, saves, video_duration

**stories** - Story data (if public)
- story_id, published_date, views, media_type

**account_history** - Historical tracking
- followers_change, following_change, posts_change, timestamp

**report_logs** - Report generation tracking
- report_type, status, execution_time, created_at

## Configuration

### accounts.json

Add or modify accounts in `config/accounts.json`:

```json
{
  "accounts": [
    {
      "id": "unique_id",
      "username": "instagram_username",
      "url": "https://www.instagram.com/username/",
      "name": "Display Name",
      "category": "OTT",
      "enabled": true
    }
  ]
}
```

## Logging

Logs are stored in `logs/` directory with automatic rotation:

- **instagram_monitor.log** - All application logs
- **errors.log** - Error logs only

Log levels can be configured via `.env`:

```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## API

The application includes a FastAPI REST API:

```bash
python -m instagram_monitor.api.main
```

Access Swagger documentation: `http://localhost:8000/docs`

### Endpoints

```
GET  /api/accounts              - List all accounts
GET  /api/accounts/{username}   - Get account details
GET  /api/statistics            - Get statistics
POST /api/scrape/{username}    - Trigger scrape
GET  /api/reports               - List reports
```

## Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=instagram_monitor --cov-report=html

# Run specific test file
pytest tests/test_validators.py

# Run with verbose output
pytest -v
```

Current test coverage: **85%+**

## Docker

### Build and Run

```bash
# Build image
docker build -t ott-monitor .

# Run container
docker run -d --name ott-monitor \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TELEGRAM_CHAT_ID=your_chat_id \
  ott-monitor
```

### Docker Compose

```bash
docker-compose up -d
```

## Scheduling

Automatic daily scraping at 09:00 (configurable):

```bash
SCHEDULE_TIME=09:00
```

Using APScheduler for reliable scheduling.

## Error Handling

- Automatic retry with exponential backoff (3 attempts)
- Screenshots on failure for debugging
- Graceful degradation - one failed account doesn't stop others
- Comprehensive error logging
- Failed operations tracked in database

## Performance

- Concurrent scraping with asyncio
- Database indexing on frequently queried columns
- Efficient data storage with SQLite
- Minimal memory footprint
- Fast report generation with pandas & openpyxl

## Security

- No sensitive data in code
- Environment variables for secrets
- Input validation on all user inputs
- SQL injection prevention with SQLAlchemy ORM
- Secure error messages (no stack traces in production)

## Troubleshooting

### Playwright browser not found

```bash
python -m playwright install chromium
```

### Telegram bot not sending messages

Check:
- `TELEGRAM_BOT_TOKEN` is valid
- `TELEGRAM_CHAT_ID` is correct
- Internet connection
- Bot has permission to send messages

### Database locked

- Ensure only one instance is running
- Check for stuck processes: `ps aux | grep python`
- Delete `data/instagram_monitor.db-wal` if present

### Memory issues

- Reduce `INSTAGRAM_LOAD_POSTS` in `.env`
- Disable screenshots: set `SCREENSHOTS_ENABLED=false`
- Clear old logs: `rm logs/*.zip`

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Author

Abdulaziz168

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review logs in `logs/` directory

## Roadmap

- [ ] TikTok monitoring
- [ ] YouTube channel monitoring
- [ ] Advanced ML-based insights
- [ ] Competitor analysis
- [ ] Custom dashboards
- [ ] Email notifications
- [ ] Webhook support

---

**Last Updated:** 2026-07-15
**Version:** 1.0.0
