import chromadb
from ai_platform.config import get_settings
from logging import getLogger
from ai_platform.config import Settings



settings = get_settings()
logger = getLogger(__name__)

class StoreDB():
    def __init__(self,db_path=None):
        path = db_path or settings.db_persistent
        self.chromadb_client = chromadb.PersistentClient(path=path)
        self.chromadb_collection = self.chromadb_client.get_or_create_collection(name=settings.db_store_collection)
        
    def add_data_collection(self,chunks:list):
        if len(chunks) == 0:
            logger.info(f"the chunks is empty {len(chunks)}")
            raise ValueError("Empty Value")
        
        self.chromadb_collection.add(
                ids=[f"chunk_id_{i}" for i in range(len(chunks))],
                documents = chunks
                )

    def query_data_collection(self,query:str,n_results:int = settings.db_query_max_results):
        if len(query) == 0:
            logger.info(f"the query is empty {len(query)}")
            raise ValueError("Query Empty Value")
        
        result = self.chromadb_collection.query(query_texts=[query],n_results=n_results)
        return result