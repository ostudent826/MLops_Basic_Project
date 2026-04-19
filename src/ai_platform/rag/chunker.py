"""
Text chunking utility for RAG processing.

Splits a document into overlapping chunks and wraps each in a ChunkToStore
model with its source and position. The resulting list is ready to be
ingested into the vector store.
"""

from .schemas import ChunkToStore
from ai_platform.config import get_settings


def chunk_data(
    input: str,
    source: str,
    doc_id: str,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[ChunkToStore]:
    """
    Split a document into overlapping chunks for RAG ingestion.

    Args:
        input: The raw text of the document to split.
        source: Identifier of the document (used as metadata on every chunk).
        doc_id: Unique identifier for this document ingestion (UUID). Used for deduplication and chunk grouping.
        chunk_size: Max characters per chunk. Falls back to settings if None.
        chunk_overlap: Characters shared between neighboring chunks. Falls back to settings if None.
    Returns:
        A list of ChunkToStore objects, each carrying its text, source, doc_id, and chunk_index.
    Raises:
        ValueError: If input is empty or overlap is not smaller than chunk size.
    """
    settings = get_settings()

    # Resolve defaults from settings when caller did not pass values
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if chunk_overlap is None:
        chunk_overlap = settings.chunk_overlap

    # Guard: reject empty input — nothing to chunk
    if len(input) == 0:
        raise ValueError("Cannot chunk empty input")

    # Guard: overlap must be strictly smaller than chunk size,
    # otherwise the sliding window never advances and loops forever
    if chunk_size <= chunk_overlap:
        raise ValueError(
            f"chunk_overlap ({chunk_overlap}) must be less than chunk_size ({chunk_size})"
        )

    chunks: list[ChunkToStore] = []
    chunk_index = 0

    # Sliding window: step forward by (chunk_size - chunk_overlap) each iteration
    # so neighboring chunks share `chunk_overlap` characters at their boundary.
    for i in range(0, len(input), chunk_size - chunk_overlap):
        chunks.append(
            ChunkToStore(
                text=input[i : i + chunk_size],
                source=source,
                doc_id=doc_id,
                chunk_index=chunk_index,
            )
        )
        chunk_index += 1

    return chunks
