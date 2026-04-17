"""
Logging configuration for the AI Platform.
Provides a standardized logging format (JSON-style) and environment-based log routing.
"""

import logging
from ai_platform.config import get_settings


def get_logger(name: str):
    """
    Initializes and returns a logger instance with a standardized format.

    Args:
        name (str): The name of the module requesting the logger (typically __name__).
    """
    settings = get_settings()
    logger = logging.getLogger(name)

    # Set the threshold for what messages to capture (e.g., 'info', 'debug') [cite: 24]
    logger.setLevel(settings.log_level)

    # Standardized format to make logs easier to parse for MLOps/monitoring tools [cite: 24]
    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}'
    )

    # Prevent adding multiple handlers if the logger is requested more than once [cite: 24]
    if not logger.handlers:
        # Standard output handler (for console/terminal)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        # File output handler (for persistent storage)
        fileHandler = logging.FileHandler("logfile.log")
        fileHandler.setFormatter(formatter)

        # Environment-based routing:
        # 'prod' usually logs to stdout (stream) for cloud container capture (like GKE or Cloud Run)
        # 'dev' logs to a local file for easier offline inspection [cite: 25]
        if settings.environment == "prod":
            logger.addHandler(streamHandler)
        else:
            logger.addHandler(fileHandler)

    return logger
