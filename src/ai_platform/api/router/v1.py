"""
API Router for version 1.
Contains endpoints for standard LLM chat and Retrieval-Augmented Generation (RAG).
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from ..schemas import Chat
from ai_platform.config import get_settings
from ai_platform.security.validation import (
    check_pattern,
    check_token_limit,
    rate_limit_by_ip,
)
from ai_platform.gateway.llm_router import llm_router_send_message
from ai_platform.logger import get_logger
from ai_platform.rag.pipeline import rag_query

# Initialize the logger for monitoring API traffic
logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["api routes"])


@router.get("/health")
def health_check():
    """
    Health check endpoint for monitoring tools.
    """
    return {"status": "Healthy"}


@router.post("/chat")
async def send_message(request: Request, payload: Chat, settings=Depends(get_settings)):
    """
    Standard LLM interaction endpoint.
    Performs security validation before routing the message to the LLM gateway.
    """
    client_host = request.client.host

    # 1. Security & Guardrails
    rate_limit_by_ip(client_host)
    check_token_limit(payload.message)
    check_pattern(payload.message)

    try:
        # 2. Process message through the LLM router (handles provider failover)
        ai_response = llm_router_send_message(payload.message)
        return {"reply": ai_response}
    except Exception as e:
        logger.error(f"Chat Error: {e}")
        raise HTTPException(
            status_code=400,
            detail="We're experiencing technical difficulties. Please try again later.",
        )


@router.post("/query")
async def rag_send_message(
    request: Request, payload: Chat, settings=Depends(get_settings)
):
    """
    RAG-enabled endpoint.
    Retrieves context from the vector database before generating a response.
    """
    client_host = request.client.host

    # 1. Security & Guardrails
    rate_limit_by_ip(client_host)
    check_token_limit(payload.message)
    check_pattern(payload.message)

    try:
        # 2. Process message through the RAG pipeline
        ai_response = rag_query(payload.message)
        return {"reply": ai_response}
    except Exception as e:
        logger.error(f"RAG Error: {e}")
        raise HTTPException(
            status_code=400,
            detail="We're experiencing technical difficulties. Please try again later.",
        )
