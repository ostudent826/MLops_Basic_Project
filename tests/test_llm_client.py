from types import SimpleNamespace
from ai_platform.llm.client import AnthropicClient
import anthropic
import pytest

mock_settings = SimpleNamespace(
    anthropic=SimpleNamespace(
        api_key='keytest-1234',
        model="claude-sonnet-4-6",
        max_tokens=6000
    )
)
mock_response = SimpleNamespace(
    content=[SimpleNamespace(text="Hello!")],
    usage=SimpleNamespace(
        input_tokens=1500,
        output_tokens=3000
    )
)

client = AnthropicClient(mock_settings)
client.client.messages.create = lambda **kwargs: mock_response

def test_send_message():
    result = client.send_message("Hello!")
    assert result == "Hello!"
    
def raise_rate_limit(**kwargs):
    mock_http_response = SimpleNamespace(
        request=SimpleNamespace(url="https://api.anthropic.com"),
        status_code=429,
        headers=SimpleNamespace(get=lambda key, default=None: default)
    )
    raise anthropic.RateLimitError("rate limited", response=mock_http_response, body=None)

def test_send_message_rate_limit():
    client.client.messages.create = raise_rate_limit
    with pytest.raises(anthropic.RateLimitError):
        client.send_message("Hello!")