"""Input validators."""

import re
from typing import Tuple


def validate_username(username: str) -> Tuple[bool, str]:
    """Validate Instagram username."""
    if not username:
        return False, "Username cannot be empty"
    if len(username) < 1 or len(username) > 30:
        return False, "Username must be 1-30 characters"
    if not re.match(r"^[a-zA-Z0-9_.]*$", username):
        return False, "Username contains invalid characters"
    return True, "Valid"


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate Instagram URL."""
    if not url:
        return False, "URL cannot be empty"
    if "instagram.com" not in url:
        return False, "URL must be an Instagram URL"
    return True, "Valid"
