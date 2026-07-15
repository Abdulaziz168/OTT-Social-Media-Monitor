"""Test utilities validator."""

import pytest
from instagram_monitor.utils.validators import validate_username, validate_url


class TestValidators:
    """Test validator functions."""

    def test_validate_username_valid(self):
        """Test valid usernames."""
        valid_usernames = ["itv_uz", "salom.tv", "user123"]
        for username in valid_usernames:
            is_valid, message = validate_username(username)
            assert is_valid, f"Username {username} should be valid: {message}"

    def test_validate_username_invalid(self):
        """Test invalid usernames."""
        invalid_usernames = ["", "a" * 31, "user@name"]
        for username in invalid_usernames:
            is_valid, message = validate_username(username)
            assert not is_valid, f"Username {username} should be invalid"

    def test_validate_url_valid(self):
        """Test valid URLs."""
        valid_urls = [
            "https://www.instagram.com/itv.uz/",
            "https://instagram.com/salom.tv/",
        ]
        for url in valid_urls:
            is_valid, message = validate_url(url)
            assert is_valid, f"URL {url} should be valid"

    def test_validate_url_invalid(self):
        """Test invalid URLs."""
        invalid_urls = ["", "https://facebook.com/user"]
        for url in invalid_urls:
            is_valid, message = validate_url(url)
            assert not is_valid, f"URL {url} should be invalid"
