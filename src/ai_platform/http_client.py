import requests
import time
from .config import Settings
from ai_platform.logger import get_logger

logger = get_logger(__name__)
settings = Settings()

class httpClient:

        def __init__(self, timeout=settings.api_timeout, retries=settings.max_retries, backoff=settings.backoff_multiplier):
            self.timeout = timeout
            self.retries = retries
            self.backoff = backoff
        
        def httpGet(self,url):
            for attempt in range(self.retries):
                try:
                    r = requests.get(url=url,timeout=self.timeout)
                    r.raise_for_status()

                    logger.info(f'Request Successed')
                    return r.json()
                
                except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError) as e:
                    logger.error(f'Something got Wrong {attempt + 1} {e}')
                    time.sleep(self.backoff ** attempt)
            logger.error(f'All Retries Failed to the {url}')
            raise Exception(f'All retries failed for {url}')

        
if __name__ == "__main__":
    client = httpClient()
    response = client.httpGet("https://httpbin.org/get")
    print(response)