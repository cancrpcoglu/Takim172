from langchain_core.tools import tool
from app.rag.retriever import SystemRetriever
from app.utils.logger import setup_logger
from app.utils.exceptions import RAGIndexNotFoundError

logger = setup_logger("PolicyTool")

@tool
def search_company_policies(query: str) -> str:
    """
    Kullanıcı iade politikası, çalışma saatleri veya ödeme yöntemleri
    hakkında genel bir soru sorduğunda bu aracı kullan.
    """
    logger.info("Ajan, şirket politikaları aracını (Tool) çağırdı.")
    
    try:
        # Arama motorunu çağırıyoruz
        retriever = SystemRetriever()
        return retriever.search(query)
    
    except RAGIndexNotFoundError as e:
        logger.error(f"Sistem Hatası: {e}")
        return "Şirket kuralları sistemine şu an ulaşılamıyor (Index bulunamadı)."
    except Exception as e:
        logger.error(f"Beklenmeyen Hata: {e}")
        return "Arama sırasında sistemsel bir sorun oluştu."