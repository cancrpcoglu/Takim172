import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from kobi_ai_system.app.utils.logger import setup_logger

load_dotenv()
logger = setup_logger("IngestionPipeline")

def create_and_save_index():
    logger.info("Veri yutma (Ingestion) süreci başlatıldı.")
    
    # Gerçek senaryoda bu veriler PDF'den (PyPDFLoader) gelir.
    kobi_bilgileri = [
        Document(page_content="İade Politikası: Satın alınan ürünler teslim tarihinden itibaren 14 gün içerisinde, kullanılmamış olmak şartıyla iade edilebilir."),
        Document(page_content="Çalışma Saatleri: Hafta içi her gün 09:00 - 18:00."),
        Document(page_content="Ödeme Yöntemleri: Kredi kartı ve Havale/EFT kabul edilmektedir.")
    ]
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        vector_store = FAISS.from_documents(kobi_bilgileri, embeddings)
        
        # Klasörü oluştur ve FAISS veritabanını diske kaydet
        os.makedirs("data", exist_ok=True)
        vector_store.save_local("data/faiss_index")
        
        logger.info("Veriler başarıyla vektörleştirildi ve 'data/faiss_index' yoluna kaydedildi.")
    except Exception as e:
        logger.error(f"Vektörleştirme sırasında kritik hata: {e}")

if __name__ == "__main__":
    create_and_save_index()