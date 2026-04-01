from .llm_clients import send_message
from ai_platform.logger import get_logger
from ai_platform.config import get_settings
from fastapi import HTTPException

settings = get_settings()
logger = get_logger(__name__)

def router_send_message(message:str) -> str:
    
    main_model = settings.anthropic.model
    secondary_model = settings.gemini.model
    third_model = settings.chatgpt.model

    try:
        response=send_message(main_model,message)
        logger.info(f"successful req")
        return response
    except (PermissionError,ConnectionError,RuntimeError) as e:
        try:
            logger.error(f"error was made in main llm, moved to secondary llm")
            response=send_message(secondary_model,message)
            return response
        except (PermissionError,ConnectionError,RuntimeError) as e:
            try:
                logger.error(f"error was made in secondary llm, moved to thrid llm")
                response=send_message(third_model,message)
                return response
            except:
                logger.error(f"Couldn't get any of the llm clients")
                raise HTTPException