from fastapi import APIRouter, Depends,HTTPException, Request
from ..schemas import Chat
from ai_platform.config import get_settings
from ai_platform.security.validation import check_pattern,check_token_limit,rate_limit_by_ip
from ai_platform.gateway.router import router_send_message

router = APIRouter(
    prefix="/api/v1",
    tags=["api routes"]
)

@router.get("/health")
def health_check():
    return {"status": "Healthy"}

@router.post("/chat")
async def send_message(request: Request, payload:Chat, settings = Depends(get_settings)):

    client_host = request.client.host
    rate_limit_by_ip(client_host)
    check_token_limit(payload.message)
    check_pattern(payload.message)  
    try:
        ai_response = router_send_message(payload.message)
        return {"reply": ai_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=("We're experiencing technical difficulties. Please try again later."))
