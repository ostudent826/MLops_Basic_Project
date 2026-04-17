"""
Unit tests for token estimation and counting.
Verifies the math behind character-based estimation and response parsing.
"""

from ai_platform import platform_token
from types import SimpleNamespace


def test_basic_estimator():
    """Tests character-to-token ratio (4:1) estimation."""
    assert platform_token.basicEstimator("thisEqualTo3") == 3


def test_mock_tokens():
    """Verifies parsing of usage stats from an LLM response object."""
    fake_usage = SimpleNamespace(input_tokens=1230, output_tokens=2133)
    fake_response = SimpleNamespace(usage=fake_usage)
    tokencounter = platform_token.tokenCounter(fake_response)
    assert tokencounter == {"input_tokens": 1230, "output_tokens": 2133}
