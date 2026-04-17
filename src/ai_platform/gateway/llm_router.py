"""
LLM Routing and Failover Logic.
Implements a hierarchical retry strategy to ensure high availability across multiple AI providers.
"""

from .llm_clients import send_message
from ai_platform.logger import get_logger
from ai_platform.config import get_settings
from fastapi import HTTPException

# Load settings and module-level logger
settings = get_settings()
logger = get_logger(__name__)


def llm_router_send_message(message: str) -> str:
    """
    Primary routing function that manages the provider failover chain.

    The order of attempts is:
    1. Anthropic (Main) -> 2. Gemini (Secondary) -> 3. ChatGPT (Tertiary)
    """
    main_model = settings.anthropic.model
    secondary_model = settings.gemini.model
    third_model = settings.chatgpt.model

    try:
        # First Attempt: Use the primary provider
        response = send_message(main_model, message)
        logger.info(f"successful req with main model {main_model}")
        return response
    except (PermissionError, ConnectionError, RuntimeError) as e:
        try:
            # Second Attempt: Primary failed, fallback to the secondary provider [cite: 13]
            logger.error(
                f"error was made in main llm, moved to secondary llm {secondary_model}"
            )
            response = send_message(secondary_model, message)
            return response
        except (
            PermissionError,
            ConnectionError,
            RuntimeError,
        ) as e:
            try:
                # Third Attempt: Secondary failed, fallback to the tertiary provider [cite: 14]
                logger.error(
                    f"error was made in secondary llm, moved to thrid llm {third_model}"
                )
                response = send_message(third_model, message)
                return response
            except:
                # Critical Failure: All providers in the chain have failed
                logger.error("Couldn't get any of the llm clients")
                raise HTTPException
