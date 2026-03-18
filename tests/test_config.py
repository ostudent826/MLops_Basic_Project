from ai_platform import config, http_client

setting = config.Settings()

def test_log_level_default():
    assert setting.log_level == 'INFO'

def test_api_timeout_is_integer():
    assert isinstance(setting.api_timeout, int)
    
def test_api_url_is_valid():
    assert setting.api_url == 'https://httpbin.org/get'#'https://api.anthropic.com'

def test_httpClient():
            client = http_client.httpClient()
            response = client.httpGet("https://httpbin.org/get")
            assert 'url' in response 
