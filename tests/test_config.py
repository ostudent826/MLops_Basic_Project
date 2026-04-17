"""
Unit tests for application configuration.
Verifies default settings and data types for environment variables.
"""

from ai_platform import config

setting = config.Settings()


def test_log_level_default():
    """Ensures the default log level is set correctly."""
    assert setting.log_level == "INFO"


def test_api_timeout_is_integer():
    """Validates that timeout settings are numeric."""
    assert isinstance(setting.api_timeout, int)


def test_api_url_is_valid():
    """Checks if the API URL matches the expected endpoint."""
    assert setting.api_url == "https://httpbin.org/get"
