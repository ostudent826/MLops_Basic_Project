from ai_platform import platform_token 
from ai_platform.logger import get_logger
from ai_platform.config import get_settings
import time 
from fastapi import HTTPException
from ai_platform.platform_token import basicEstimator



logger = get_logger(__name__)
settings = get_settings()

request_tracker_by_ip = {}

def rate_limit_by_ip(ip: str):
    now = time.time()
    timestamps = request_tracker_by_ip.get(ip,[])
    recent = [t for t in timestamps if now - t < 300]    
       
    if len(recent) >= 5:
        logger.warning(f"Rate limit exceeded for IP: {ip}")
        raise HTTPException(429,detail="You have made to many requests, try again in few mins")

    recent.append(now)
    request_tracker_by_ip[ip] = recent 
    logger.info(f"Request allowed for IP: {ip}")

def check_token_limit(message: str):
    estimated_token = basicEstimator(message)
    if estimated_token > settings.max_user_token:

        logger.warning(f"Message too long: {estimated_token} tokens")
        raise HTTPException(400,detail="Your message is too long")