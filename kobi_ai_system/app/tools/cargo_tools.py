import asyncio
from langchain_core.tools import tool

@tool
async def track_cargo(order_id: str) -> dict:
    """
    Müşterinin sipariş veya kargo numarasını kullanarak kargo durumunu sorgular.
    
    ÇOK ÖNEMLİ KURAL: 
    Kullanıcı 'Kargom nerede?', 'Siparişim ne durumda?' diye sorarsa ve bir sipariş numarası VERMEDİYSE, 
    bu aracı KESİNLİKLE ÇALIŞTIRMA. Önce müşteriden nazikçe sipariş numarasını iste.
    Sadece müşteri 'KRG-123 numaralı kargom nerede?' gibi net bir ID verdiğinde bu aracı kullan.
    
    Args:
        order_id (str): Sorgulanacak kargo takip numarası (Örn: 'KRG-123', 'KRG-456').
    """
    print(f"[Log] Kargo sistemine istek atılıyor... Sorgulanan No: {order_id}")
    await asyncio.sleep(1) # Asenkron DB/API gecikmesi simülasyonu
    
    # MOCK (Sahte) Kargo Veritabanı
    mock_cargo_db = {
        "KRG-123": {
            "durum": "Yolda", 
            "sirket": "Yurtiçi Kargo", 
            "tahmini_teslimat": "12 Mayıs 2026", 
            "adimlar": ["Sipariş Alındı", "Kargoya Verildi", "Transfer Merkezinde"]
        },
        "KRG-456": {
            "durum": "Teslim Edildi", 
            "sirket": "Aras Kargo", 
            "tahmini_teslimat": "9 Mayıs 2026", 
            "adimlar": ["Sipariş Alındı", "Kargoya Verildi", "Dağıtıma Çıktı", "Teslim Edildi"]
        }
    }
    
    # Gelen string'i büyük harfe çevirip boşlukları temizleyelim (Kullanıcı 'krg 123' yazabilir)
    clean_id = order_id.upper().replace(" ", "").strip()
    
    if clean_id in mock_cargo_db:
        return {"status": "success", "data": {"siparis_no": clean_id, **mock_cargo_db[clean_id]}}
        
    return {"status": "not_found", "message": f"Sistemimizde {order_id} numaralı aktif bir kargo kaydı bulunamadı."}