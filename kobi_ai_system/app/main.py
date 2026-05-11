from fastapi import FastAPI
from kobi_ai_system.app.schemas.requests import ChatRequest
from kobi_ai_system.app.schemas.responses import ChatResponse
from kobi_ai_system.app.agents.orchestrator import process_chat
from kobi_ai_system.app.agents.analytics_agent import process_admin_chat

app = FastAPI(
    title="KOBİ AI System API",
    description="Hackathon için geliştirilen yapay zeka destekli müşteri asistanı.",
    version="1.0.0"
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    print(f"📥 Yeni İstek - Session: {request.session_id} | Mesaj: {request.message}")
    
   
    response = await process_chat(request.message, request.session_id)
    
    print(f"📤 Yanıt: {response.ui_type}")
    return response

@app.post("/api/admin/chat", response_model=ChatResponse)
async def admin_chat_endpoint(request: ChatRequest):
    """
    Yönetici Panelinden gelen soruları alır ve Analytics Agent'a yönlendirir.
    Ciro, sorunlu kargolar gibi yetki gerektiren verileri döner.
    """
    print(f"🔐 Yeni ADMIN İstek - Session: {request.session_id} | Mesaj: {request.message}")
    
    response = await process_admin_chat(request.message, request.session_id)
    
    print(f"📤 ADMIN Yanıtı: {response.ui_type}")
    return response