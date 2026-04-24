"""
One-off ingestion utility.

Reads every .md file under db/doc_storage/ and pushes it through the
RAG ingestion pipeline. The filename (without extension) becomes the
`source` metadata attached to every chunk from that file.

Intended for bulk-populating the vector store during development or
after wiping ChromaDB. Not part of the application runtime — this is
operational tooling, separate from the importable package.

Usage:
    uv run python scripts/ingest_corpus.py
"""

from pathlib import Path
from ai_platform.rag.pipeline import load_docs_rag, store_client


def ingest_corpus():
    """Ingest every .md file in db/doc_storage/ into the vector store."""
    files = list(Path("db/doc_storage").glob("*.md"))
    count = store_client.chromadb_collection.count()

    if count > 0:
        print(
            f"ChromaDB already has {count} chunks. Wipe with 'rm -rf db/chromaDB' first."
        )
        return
    for file in files:
        text = file.read_text()
        source = file.stem
        load_docs_rag(text, source)
        print(f"ingested: {source} ({len(text)} chars)")


if __name__ == "__main__":
    ingest_corpus()
