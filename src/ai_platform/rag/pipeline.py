from ai_platform.rag.chunker import chunk_data
from ai_platform.rag.rag_db import StoreDB
from ai_platform.gateway.llm_router import llm_router_send_message
from ai_platform.logger import get_logger


logger = get_logger(__name__)
store_client = StoreDB()


def load_docs_rag(doc: str):
    chunk_data_output = chunk_data(doc)
    logger.info(f"chunked document into {len(chunk_data_output)} chunks")
    store_client.add_data_collection(chunk_data_output)
    logger.info("chunks added to store")


def rag_query(message: str) -> str:
    logger.info(f"RAG query received: {message[:50]}...")
    query_result = store_client.query_data_collection(message)
    chunks_text = "\n".join(query_result["documents"][0])
    logger.info(
        f"retrieved {len(query_result['documents'][0])} chunks, distances: {query_result['distances'][0]}"
    )

    new_prompt = f"""Based on the following context, answer the user's question.

Context:
{chunks_text}

Question:
{message}
"""

    llm_result = llm_router_send_message(new_prompt)
    logger.info("LLM response generated")

    return llm_result
