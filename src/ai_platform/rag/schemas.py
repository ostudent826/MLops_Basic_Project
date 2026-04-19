from pydantic import BaseModel


class ChunkToStore(BaseModel):
    text: str
    source: str
    doc_id: str
    chunk_index: int
