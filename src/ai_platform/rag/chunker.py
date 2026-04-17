"""
Text chunking utility for RAG processing.
Splits large text inputs into smaller segments with overlapping boundaries
to maintain context between chunks.
"""


def chunk_data(input: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    Divide a string into a list of chunks based on character length.

    Args:
        input (str): The raw text to be split.
        chunk_size (int): The maximum character length of each chunk.
        chunk_overlap (int): The number of characters to repeat from the previous chunk.
    """
    chunk = []

    # Validate that input is not empty
    if len(input) == 0:
        raise ValueError(f"User input is empty string size {input}")

    # Ensure overlap is smaller than the total chunk size to prevent infinite loops
    if chunk_size <= chunk_overlap:
        raise ValueError(
            f"overlap is greater than chunks chunk size {chunk_size} ,overlap size {chunk_overlap}"
        )

    # Use a sliding window approach to create overlapping segments
    for i in range(0, len(input), (chunk_size - chunk_overlap)):
        chunk.append(input[i : i + chunk_size])

    return chunk
