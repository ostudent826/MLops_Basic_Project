"""
Token estimation and counting utilities.
Helps predict costs before sending requests and parses usage from LLM responses.
"""

import math


def basicEstimator(text):
    """
    Simple heuristic to estimate token count based on character length.
    Standard approximation: 1 token ≈ 4 characters.
    """
    return math.ceil(len(text) / 4)


def tokenCounter(response):
    """
    Extracts structured token usage data from a LiteLLM/provider response object.
    """
    return {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }
