"""Configuration loader for accounts."""

import json
from pathlib import Path
from typing import List, Dict, Any

from loguru import logger
from instagram_monitor.core.settings import settings


class ConfigLoader:
    """Load and manage configuration."""

    @staticmethod
    def load_accounts() -> List[Dict[str, Any]]:
        """Load accounts from config file."""
        config_file = settings.CONFIG_DIR / "accounts.json"
        
        if not config_file.exists():
            logger.error(f"Config file not found: {config_file}")
            return []
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                accounts = [a for a in data.get("accounts", []) if a.get("enabled", True)]
                logger.info(f"Loaded {len(accounts)} accounts from config")
                return accounts
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return []

    @staticmethod
    def get_account_by_username(username: str) -> Dict[str, Any]:
        """Get account config by username."""
        accounts = ConfigLoader.load_accounts()
        for account in accounts:
            if account.get("username") == username:
                return account
        return {}
