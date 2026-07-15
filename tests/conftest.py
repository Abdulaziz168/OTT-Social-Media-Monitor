"""Conftest for pytest fixtures."""

import pytest
from pathlib import Path
from instagram_monitor.database import init_database, get_session


@pytest.fixture(scope="session")
def setup_test_db():
    """Setup test database."""
    init_database()
    yield


@pytest.fixture
def db_session(setup_test_db):
    """Get test database session."""
    session = get_session()
    yield session
    session.close()
