import litellm
from ai_platform.logger import get_logger
from ai_platform.cost import add_cost,check_budget_exceeded
from ai_platform.config import get_settings

settings = get_settings()
logger = get_logger(__name__)

def send_message(model:str, message:str) -> str:
    message_input = [{"role": "user", "content": message}]
    check_budget_exceeded(settings.max_cost)
    
    try:
        response = litellm.completion(model=model,messages=message_input,max_tokens=settings.max_tokens)
        req_cost = litellm.completion_cost(completion_response=response)
        add_cost(req_cost)
        return response.choices[0].message.content
    except litellm.exceptions.AuthenticationError as e:
        logger.warning(f"Bad API key: {e}")
        raise PermissionError(f"LLM authentication failed: {e}")
    except litellm.exceptions.RateLimitError as e:
        logger.warning(f"Rate limited: {e}")
        raise ConnectionError(f"LLM Ratelimit error: {e}")
    except litellm.exceptions.APIError as e:
        logger.error(f"API error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")
    except litellm.exceptions.BadRequestError as e:
        logger.error(f"API Bad Request error: {e}")
        raise RuntimeError(f"LLM API failed: {e}")