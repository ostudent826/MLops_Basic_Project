from ai_platform import config, http_client


def test_log_level_default():
    assert config.LOG_LEVEL == 'INFO'

def test_api_timeout_is_integer():
    assert isinstance(config.API_TIMEOUT, int)
    
def test_api_url_is_valid():
    assert config.API_URL == 'https://httpbin.org/get'#'https://api.anthropic.com'

def test_httpClient():
            client = http_client.httpClient()
            response = client.httpGet("https://httpbin.org/get")
            assert 'url' in response 