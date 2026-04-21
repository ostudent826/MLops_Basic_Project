from ai_platform.rag.pipeline import load_docs_rag
from pathlib import Path


def ingest_corpus():
    file_path = list(Path("db/doc_storage").glob("*.md"))
    for i in file_path:
        file_output = i.read_text()
        file_src = i.stem
        load_docs_rag(file_output, file_src)


if __name__ == "__main__":
    ingest_corpus()
