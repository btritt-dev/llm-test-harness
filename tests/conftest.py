"""Shared pytest fixtures for the test harness."""

import pytest

from src.client import get_client


@pytest.fixture(scope="session")
def client():
    """Shared Anthropic client for tests that need direct API access.

    Not used by FM-01 (which calls ask(), already wraps client creation) -
    kept here for FM-02/FM-03 tests that may want the raw client object.
    """
    return get_client()
