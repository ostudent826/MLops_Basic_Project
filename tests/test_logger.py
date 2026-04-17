"""
Unit tests for the logging system.
Checks logger naming and handler initialization.
"""

from ai_platform.logger import get_logger


def test_logger():
    """Verifies logger name and ensures handlers are correctly attached."""
    logger = get_logger(__name__)
    logger.info("logger is working")

    # Logger name should match the module name provided
    assert logger.name == "test_logger"
    # Ensure at least one handler (Stream or File) is active
    assert len(logger.handlers) == 1
