import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """Modüller için standartlaştırılmış logger oluşturur."""
    logger = logging.getLogger(name)
    
    # Logger daha önce ayarlanmışsa tekrar ekleme yapmamak için kontrol
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Log Formatı: [Tarih] | [Seviye] | [Modül] | Mesaj
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # 1. Terminale (Console) Yazdır
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 2. Dosyaya (system.log) Kaydet
        file_handler = logging.FileHandler("system.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger