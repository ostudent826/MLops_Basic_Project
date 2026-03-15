import requests
import time
from .config import Settings
import logging

logging.basicConfig(filename='newlogfile.log',level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

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

                    logging.info(f'Request Successed')
                    return r.json()
                
                except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError) as e:
                    logging.error(f'Something got Wrong {attempt + 1} {e}')
                    time.sleep(self.backoff ** attempt)
            logging.error(f'All Retries Failed to the {url}')
            raise Exception(f'All retries failed for {url}')

        
if __name__ == "__main__":
    client = httpClient()
    response = client.httpGet("https://httpbin.org/get")
    print(response)