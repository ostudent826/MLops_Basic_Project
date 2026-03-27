from ai_platform.logger import get_logger

def test_logger():
    logger = get_logger(__name__)
    logger.info("logger is working")
    
    assert logger.name == "test_logger"
    assert len(logger.handlers) == 1