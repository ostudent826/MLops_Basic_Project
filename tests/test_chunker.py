"""
Unit tests for the text chunking utility.
Validates window slicing logic and error handling for invalid configurations.
"""

from ai_platform.rag.chunker import chunk_data
import pytest


def test_chunk_data():
    """Verifies that text is split correctly with the specified overlap."""
    result = chunk_data("abcdefghijklmnopqrst", 10, 2)
    assert result[0] == "abcdefghij"
    assert result[1] == "ijklmnopqr"  # Starts at index 8 due to 2-char overlap
    assert result[2] == "qrst"


def test_chunk_data_input_blank():
    """Ensures empty strings are rejected."""
    with pytest.raises(ValueError):
        chunk_data("")


def test_chunk_data_overlap_size():
    """Ensures overlap cannot be larger than the chunk size itself."""
    with pytest.raises(ValueError):
        chunk_data("Hi just testing overlap", 50, 150)
