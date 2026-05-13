import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

# Hafıza modülümüzü içeri aktarıyoruz
from langgraph.checkpoint.memory import MemorySaver

from kobi_ai_system.app.tools.stock_tools import check_stock_and_price
from kobi_ai_system.app.tools.cargo_tools import track_cargo
from kobi_ai_system.app.tools.policy_tools import search_company_policies
from kobi_ai_system.app.schemas.responses import ChatResponse

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.1
)

tools = [check_stock_and_price, track_cargo, search_company_policies]

system_prompt = """Sen KOBİ'ler ve kooperatifler için çalışan uzman bir asistan ajansın.

KURALLAR:
1. Ürün fiyatı/stoku sorulursa 'check_stock_and_price' aracını kullan.
2. Kargo nerede diye sorulursa 'track_cargo' aracını kullan (sipariş numarası yoksa önce numarayı iste).
3. İade, ödeme, çalışma saatleri gibi şirket kuralları sorulursa 'search_company_policies' aracını kullan.
4. Son yanıtını KESİNLİKLE aşağıdaki JSON formatında ver. Düz metin kullanma.

JSON ŞABLONU:
{
  "message": "Müşteriye söyleyeceğin doğal dildeki yanıt",
  "ui_type": "Stok için 'product_card', Kargo için 'cargo_timeline', RAG ve diğer yanıtlar için 'text' yaz",
  "ui_data": {} 
}"""

# 1. Hafıza Nesnesini Yaratıyoruz
memory = MemorySaver()

# 2. Ajanı kurarken hafızayı (checkpointer) ona bağlıyoruz
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory
)

# 3. Fonksiyona session_id parametresini ekledik
async def process_chat(user_message: str, session_id: str) -> ChatResponse:
    """FastAPI tarafından çağrılacak ana fonksiyon."""
    
    inputs = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
    }
    
    # 4. LangGraph'a bu sohbetin kimliğini (thread_id) söylüyoruz
    config = {"configurable": {"thread_id": session_id}}
    
    final_response = ChatResponse(
        message="Sistemsel bir hata oluştu, lütfen tekrar deneyin.",
        ui_type="text",
        ui_data=None
    )
    
    # 5. config parametresini astream fonksiyonuna gönderiyoruz
    async for event in agent_executor.astream(inputs, config=config, stream_mode="values"):
        message = event["messages"][-1]
        
        if message.type == "ai" and not message.tool_calls:
            if isinstance(message.content, list):
                raw_text = "".join(item.get("text", "") if isinstance(item, dict) else str(item) for item in message.content).strip()
            else:
                raw_text = str(message.content).strip()
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            
            try:
                final_response = ChatResponse.model_validate_json(clean_json)
            except Exception as e:
                print(f"JSON Parse Hatası: {e}")
                final_response = ChatResponse(message=raw_text, ui_type="text", ui_data=None)
                
    return final_response