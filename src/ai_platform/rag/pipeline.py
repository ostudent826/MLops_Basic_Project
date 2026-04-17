"""
RAG Pipeline Orchestrator.
Coordinates document ingestion and retrieval-augmented query generation.
"""

from ai_platform.rag.chunker import chunk_data
from ai_platform.rag.rag_db import StoreDB
from ai_platform.gateway.llm_router import llm_router_send_message
from ai_platform.logger import get_logger

# Initialize module logger and the vector store client
logger = get_logger(__name__)
store_client = StoreDB()


def load_docs_rag(doc: str):
    """
    Ingests a document into the system by chunking it and
    storing the segments in the vector database.
    """
    # 1. Break down document into segments
    chunk_data_output = chunk_data(doc)
    logger.info(f"chunked document into {len(chunk_data_output)} chunks")

    # 2. Persist chunks to ChromaDB
    store_client.add_data_collection(chunk_data_output)
    logger.info("chunks added to store")


def rag_query(message: str) -> str:
    """
    Executes the full RAG cycle:
    1. Retrieve relevant text chunks from ChromaDB.
    2. Build an augmented prompt with retrieved context.
    3. Generate a response using the LLM gateway.
    """
    logger.info(f"RAG query received: {message[:50]}...")

    # 1. Retrieve the most relevant information from the database
    query_result = store_client.query_data_collection(message)

    # 2. Combine retrieved chunks into a single context block
    chunks_text = "\n".join(query_result["documents"][0])
    logger.info(
        f"retrieved {len(query_result['documents'][0])} chunks, distances: {query_result['distances'][0]}"
    )

    # 3. Create the prompt containing the retrieved context and user question
    new_prompt = f"""Based on the following context, answer the user's question.
Context:
{chunks_text}

Question:
{message}
"""

    # 4. Route the augmented prompt to the LLM (handles failover)
    llm_result = llm_router_send_message(new_prompt)
    logger.info("LLM response generated")

    return llm_result
