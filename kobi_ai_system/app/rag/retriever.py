import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from app.utils.logger import setup_logger
from app.utils.exceptions import RAGIndexNotFoundError

logger = setup_logger("Retriever")

class SystemRetriever:
    def __init__(self):
        self.index_path = "data/faiss_index"
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_store = self._load_index()

    def _load_index(self):
        if not os.path.exists(self.index_path):
            raise RAGIndexNotFoundError("FAISS index bulunamadı! Önce ingestion.py çalıştırılmalı.")
        
        # Diskteki veritabanını hafızaya alıyoruz
        return FAISS.load_local(
            self.index_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )

    def search(self, query: str, k: int = 2) -> str:
        logger.info(f"Vektör araması tetiklendi. Sorgu: '{query}'")
        docs = self.vector_store.similarity_search(query, k=k)
        
        if docs:
            return "\n".join([doc.page_content for doc in docs])
        return "Bu konu hakkında kurumsal bilgi bulunamadı."