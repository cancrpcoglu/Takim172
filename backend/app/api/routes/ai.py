from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.app.core.security import get_current_user
# Import yollarını projenin ana dizinine göre standardize etmen gerekebilir
from kobi_ai_system.app.agents.analytics_agent import process_admin_chat
from kobi_ai_system.app.agents.orchestrator import process_chat  # Yeni eklediğimiz ana ajan

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    message: str
    

@router.post("/seller-chat")
async def seller_chat(
    request: ChatRequest,
    user=Depends(get_current_user)
):
    """
    Satıcı paneli için analiz yapan ajan (Satış raporları, geciken kargolar vb.)
    """
    return await process_admin_chat(
        user_message=request.message,
        session_id=f"seller_{user['user_id']}"
    )

@router.post("/customer-chat")
async def customer_chat(
    request: ChatRequest,
    user=Depends(get_current_user)
):
    """
    Müşteri asistanı ajanı (Stok sorgulama, kargo takibi, şirket politikaları)
    """
   
    session_id =  f"customer_{user['user_id']}"
    
    return await process_chat(
        user_message=request.message,
        session_id=session_id
    )