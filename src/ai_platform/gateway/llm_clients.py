"""
Unified LLM client gateway.
Utilizes LiteLLM to interface with various AI providers while enforcing budget guardrails.
"""

import litellm
from ai_platform.logger import get_logger
from ai_platform.cost import add_cost, check_budget_exceeded
from ai_platform.config import get_settings

# Initialize settings and logger for gateway operations
settings = get_settings()
logger = get_logger(__name__)


def send_message(model: str, message: str) -> str:
    """
    Sends a prompt to the specified model and handles the response lifecycle.

    Includes pre-flight budget checks, unified completion calls,
    and detailed error handling for various provider failure modes.
    """
    message_input = [{"role": "user", "content": message}]

    # Pre-flight check: Verify that the global spend has not exceeded the max_cost limit
    check_budget_exceeded(settings.max_cost)

    try:
        # Unified call to the LLM provider (Anthropic, Gemini, or OpenAI)
        response = litellm.completion(
            model=model, messages=message_input, max_tokens=settings.max_tokens
        )

        # Calculate the cost of the specific request using provider-specific pricing
        req_cost = litellm.completion_cost(completion_response=response)

        # Update the global cost tracker [cite: 11]
        add_cost(req_cost)

        # Return the raw text content of the AI's response
        return response.choices[0].message.content

    except litellm.exceptions.AuthenticationError as e:
        # Handle invalid API keys or expired credentials [cite: 11]
        logger.warning(f"Bad API key: {e}")
        raise PermissionError(f"LLM authentication failed: {e}")

    except litellm.exceptions.RateLimitError as e:
        # Handle provider-side throttling [cite: 11]
        logger.warning(f"Rate limited: {e}")
        raise ConnectionError(f"LLM Ratelimit error: {e}")

    except litellm.exceptions.APIError as e:
        # Handle general provider-side infrastructure failures [cite: 11]
        logger.error(f"API error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")

    except litellm.exceptions.BadRequestError as e:
        # Handle malformed requests or unsupported parameters [cite: 12]
        logger.error(f"API Bad Request error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")

    except litellm.exceptions.ServiceUnavailableError as e:
        # Handle malformed requests or unsupported parameters [cite: 12]
        logger.error(f"API Bad Request error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")
