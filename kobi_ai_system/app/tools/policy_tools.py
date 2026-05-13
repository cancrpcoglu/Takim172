from langchain_core.tools import tool
from kobi_ai_system.app.rag.retriever import SystemRetriever
import asyncio

@tool
async def search_company_policies(query: str) -> str:
    """İade, ödeme ve çalışma saatleri gibi şirket politikalarını sorgular."""
    try:
        retriever = SystemRetriever()
      
        result = retriever.search(query)
        return result if result else "Bu konuda spesifik bir politika bulunamadı."
    except Exception:
        return "Şirket politikası sistemine şu an ulaşılamıyor."