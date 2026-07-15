"""Test configuration loader."""

import pytest
from instagram_monitor.utils import ConfigLoader


class TestConfigLoader:
    """Test configuration loader."""

    def test_load_accounts(self):
        """Test loading accounts from config."""
        accounts = ConfigLoader.load_accounts()
        assert isinstance(accounts, list)
        assert len(accounts) > 0

    def test_get_account_by_username(self):
        """Test getting account by username."""
        account = ConfigLoader.get_account_by_username("itv.uz")
        assert account is not None
        assert account.get("username") == "itv.uz"

    def test_get_account_by_username_not_found(self):
        """Test getting non-existent account."""
        account = ConfigLoader.get_account_by_username("nonexistent_account")
        assert account == {}
