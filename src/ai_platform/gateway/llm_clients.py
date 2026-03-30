import litellm
from ai_platform.logger import get_logger


logger = get_logger(__name__)


def send_message(model:str, message:str) -> str:
    message_input = [{"role": "user", "content": message}]
    
    try:
        response = litellm.completion(model=model,messages=message_input)
        return response.choices[0].message.content
    except litellm.AuthenticationError as e:
        logger.warning(f"Bad API key: {e}")
        raise PermissionError(f"LLM authentication failed: {e}")
    except litellm.RateLimitError as e:
        logger.warning(f"Rate limited: {e}")
        raise ConnectionError(f"LLM Ratelimit error: {e}")
    except litellm.APIError as e:
        logger.error(f"API error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")
