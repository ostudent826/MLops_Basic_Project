import logging
from ai_platform.config import get_settings

def get_logger(name: str):
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)
    formatter = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(name)s", "message": "%(message)s"}')



    if not logger.handlers:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        
        fileHandler = logging.FileHandler("logfile.log")
        fileHandler.setFormatter(formatter) 
    
        if settings.environment == "prod":
            
            logger.addHandler(streamHandler)
        else:
    
            logger.addHandler(fileHandler)
        
    
    return logger