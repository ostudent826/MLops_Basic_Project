from ai_platform import platform_token
from types import SimpleNamespace


   
def test_basic_estimator():
    assert platform_token.basicEstimator('thisEqualTo3') == 3

def test_mock_tokens():
    fake_usage = SimpleNamespace(input_tokens=1230, output_tokens=2133)
    fake_response = SimpleNamespace(usage=fake_usage)
    tokencounter = platform_token.tokenCounter(fake_response)
    assert tokencounter == {'input_tokens': 1230,'output_tokens':2133}