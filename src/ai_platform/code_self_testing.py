import requests
import logging

logging.basicConfig(filename='deftest.log',level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def httpClientGet():
    r = requests.get(url="https://httpbin.org/get")
    return r.text

print(httpClientGet())
logging.debug('log test-debug' )
