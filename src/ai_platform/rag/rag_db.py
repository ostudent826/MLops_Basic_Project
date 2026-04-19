"""
Vector database management using ChromaDB.
Handles persistent storage of text chunks and performs similarity searches.
"""

import chromadb
from ai_platform.config import get_settings
from logging import getLogger
from .schemas import ChunkToStore

# Load project-wide settings and initialize logger
settings = get_settings()
logger = getLogger(__name__)


class StoreDB:
    """
    Wrapper for ChromaDB operations, including collection management
    and document querying.
    """

    def __init__(self, db_path=None):
        """
        Initializes the persistent ChromaDB client using the path
        defined in settings.
        """
        path = db_path or settings.db_persistent
        self.chromadb_client = chromadb.PersistentClient(path=path)

        # Get an existing collection or create a new one for document storage
        self.chromadb_collection = self.chromadb_client.get_or_create_collection(
            name=settings.db_store_collection
        )

    def add_data_collection(self, chunks: list[ChunkToStore]):
        """
        Adds a list of text chunks to the vector database collection.
        Automatically generates IDs for each segment.
        """
        if len(chunks) == 0:
            logger.info(f"the chunks is empty {len(chunks)}")
            raise ValueError("Empty Value")

        # Add documents with unique identifiers (ids)
        self.chromadb_collection.add(
            ids=[f"{chunk.doc_id}:{chunk.chunk_index}" for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "source": chunk.source,
                    "chunk_index": chunk.chunk_index,
                    "doc_id": chunk.doc_id,
                }
                for chunk in chunks
            ],
        )

    def query_data_collection(
        self, query: str, n_results: int = settings.db_query_max_results
    ):
        """
        Performs a similarity search in the database based on a user query string.

        Returns:
            dict: The search results including documents and distances.
        """
        if len(query) == 0:
            logger.info(f"the query is empty {len(query)}")
            raise ValueError("Query Empty Value")

        # Search for the most relevant n_results chunks
        result = self.chromadb_collection.query(
            query_texts=[query], n_results=n_results
        )
        return result
