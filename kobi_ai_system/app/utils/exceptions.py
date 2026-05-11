class KobiAIException(Exception):
    """Sistemdeki tüm özel hataların temel (base) sınıfı."""
    pass

class ToolExecutionError(KobiAIException):
    """Ajan bir aracı (Tool) çalıştırırken hata aldığında fırlatılır."""
    pass

class RAGIndexNotFoundError(KobiAIException):
    """Vektör veritabanı diskte bulunamadığında fırlatılır."""
    pass