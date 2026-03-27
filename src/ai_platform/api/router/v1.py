from fastapi import APIRouter, Depends,HTTPException
from ..schemas import Chat
from ai_platform.llm.client import AnthropicClient
from ai_platform.config import get_settings
router = APIRouter(
    prefix="/api/v1",
    tags=["api routes"]
)

@router.get("/health")
def health_check():
    return {"status": "Healthy"}

@router.post("/chat")
async def send_message(payload:Chat, settings = Depends(get_settings)):
    client = AnthropicClient(settings)
    try:
        ai_response = client.send_message(payload.message)
        return {"reply": ai_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=("We're experiencing technical difficulties. Please try again later."))
