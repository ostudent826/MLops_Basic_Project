"""
Shared Pydantic schemas for the RAG subsystem.

These schemas act as contracts between producers (chunker, evaluation)
and consumers (vector store, evaluation runner). Defining them in a
neutral module keeps both sides loosely coupled.
"""

from pydantic import BaseModel


class ChunkToStore(BaseModel):
    """
    A chunk produced by the chunker, ready to be persisted in the vector store.

    Fields:
        text: The raw chunk content to be embedded and stored.
        source: Human-readable document identifier (e.g. filename stem).
                May repeat across ingestion events of the same logical document.
        doc_id: UUID v4 generated per ingestion event. Unique per call to
                load_docs_rag; used for grouping and safe re-ingestion.
        chunk_index: Zero-based position of this chunk within its document.
                     Combined with doc_id, forms the unique chunk ID.
    """

    text: str
    source: str
    doc_id: str
    chunk_index: int


class TestCase(BaseModel):
    """
    A single RAG evaluation test case.

    Each test case defines a user-style question and the document whose
    chunks should be retrieved when the question is sent through the
    RAG pipeline. The evaluation module uses these to measure retrieval
    accuracy (e.g. recall@N).

    Fields:
        id: Short identifier for logging and reporting (e.g. "q1").
        question: The query to send to the retrieval pipeline.
        expected_source: The `source` metadata value of the chunk that
                         should be retrieved. Must match the stem of a
                         `.md` file in db/doc_storage/.
    """

    id: str
    question: str
    expected_source: str


class FailureDetail(BaseModel):
    """Details of a single test case that failed retrieval."""

    test_id: str
    question: str
    expected_source: str
    retrieved_sources: list[str]


class EvalResult(BaseModel):
    total: int
    passed: int
    failed: int
    recall_at_n: float
    n_results: int
    failures: list[FailureDetail]
