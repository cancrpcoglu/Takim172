import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from kobi_ai_system.app.tools.analytics_tools import get_daily_sales_summary, get_delayed_cargos
from kobi_ai_system.app.schemas.responses import ChatResponse

load_dotenv()

# Analitik ajanımızda da aynı modeli kullanabiliriz
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0 # Analitik konularda sıfır halüsinasyon isteriz
)

tools = [get_daily_sales_summary, get_delayed_cargos]

system_prompt = """Sen bir KOBİ yöneticisinin (mağaza sahibinin) kişisel veri analisti ajansın.
Amacın yöneticinin mağaza durumu, satışlar, ciro ve kargo problemleri hakkındaki sorularını yanıtlamaktır.

KURALLAR:
1. Satış ve ciro için 'get_daily_sales_summary' aracını kullan.
2. Sorunlu kargolar için 'get_delayed_cargos' aracını kullan.
3. Yöneticiye hitap ederken profesyonel ve net ol. Rakamları vurgula.
4. Son yanıtını KESİNLİKLE aşağıdaki JSON formatında ver. Düz metin kullanma.

JSON ŞABLONU:
{
  "message": "Yöneticiye vereceğin özet rapor metni",
  "ui_type": "Satış verisi için 'sales_dashboard', Kargo verisi için 'alert_list', diğerleri için 'text' yaz",
  "ui_data": {} // Araçtan gelen JSON verisi
}"""

memory = MemorySaver()

agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory
)

async def process_admin_chat(user_message: str, session_id: str) -> ChatResponse:
    inputs = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
    }
    
    config = {"configurable": {"thread_id": f"admin_{session_id}"}}
    
    final_response = ChatResponse(
        message="Sistemsel bir hata oluştu.",
        ui_type="text",
        ui_data=None
    )
    
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