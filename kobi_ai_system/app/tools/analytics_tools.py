import asyncio
from langchain_core.tools import tool

@tool
async def get_daily_sales_summary(date: str = "bugün") -> dict:
    """
    Satıcının günlük, haftalık veya aylık satış cirosunu ve toplam sipariş sayısını getirir.
    Kullanıcı 'Bugün ne kadar sattık?', 'Ciro nedir?' diye sorduğunda bu aracı kullan.
    """
    print(f"[Log] Satış veritabanı sorgulanıyor... Tarih: {date}")
    await asyncio.sleep(1) # Asenkron gecikme
    
    # MOCK (Sahte) Analitik Verisi
    return {
        "tarih": date,
        "toplam_siparis": 42,
        "toplam_ciro_tl": 18500.00,
        "en_cok_satan_urun": "Kahve Makinesi (3 Adet)"
    }

@tool
async def get_delayed_cargos() -> dict:
    """
    Sistemdeki teslimatı gecikmiş veya sorunlu kargoların listesini getirir.
    Kullanıcı 'Geciken kargo var mı?', 'Kargo problemleri neler?' dediğinde bu aracı kullan.
    """
    print("[Log] Geciken kargolar taranıyor...")
    await asyncio.sleep(1)
    
    # MOCK (Sahte) Sorunlu Kargo Verisi
    return {
        "geciken_kargo_sayisi": 2,
        "detaylar": [
            {"siparis_no": "KRG-999", "durum": "Hasarlı Paket, İade Sürecinde", "musteri": "Ahmet Y."},
            {"siparis_no": "KRG-888", "durum": "Adreste Bulunamadı", "musteri": "Ayşe K."}
        ]
    }