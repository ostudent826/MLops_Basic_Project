import pytest
from fastapi import HTTPException
from ai_platform.security.validation import check_token_limit

def test_token_limit_allows_short_message():
    check_token_limit("Hello world")

def test_token_limit_blocks_long_message():
    long_message = "x" * 50000
    with pytest.raises(HTTPException) as exc:
        check_token_limit(long_message)
    assert exc.value.status_code == 400