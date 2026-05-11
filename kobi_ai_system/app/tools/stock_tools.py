import asyncio
from langchain_core.tools import tool

@tool
async def check_stock_and_price(product_name: str) -> dict:
    """
    Kullanıcının sorduğu ürünün stok durumunu, fiyatını ve detaylarını veritabanından sorgular.
    Kullanıcı 'X ürünü var mı?' veya 'Y ne kadar?' dediğinde bu aracı kullan.
    
    Args:
        product_name (str): Aranacak ürünün adı veya kategorisi (örn: 'mavi tişört', 'kahve makinesi').
    """
    # TODO: Backend API'si hazır olduğunda buraya httpx/aiohttp ile gerçek istek (GET /api/products) atılacak.
    
    print(f"[Log] Backend'e istek atılıyor... Aranan ürün: {product_name}")
    
    # Asenkron yapıyı simüle etmek için küçük bir gecikme ekliyoruz
    await asyncio.sleep(1) 
    
    # MOCK (Sahte) VERİ - Backend yokken sistemi test etmek için
    mock_database = {
        "mavi tişört": {"stok": 15, "fiyat": 250.00, "bedenler": ["M", "L", "XL"], "id": "PRD-001"},
        "kahve makinesi": {"stok": 2, "fiyat": 4500.00, "bedenler": None, "id": "PRD-002"}
    }
    
    # Basit bir arama mantığı
    for key, data in mock_database.items():
        if key in product_name.lower():
            return {"status": "success", "data": {"isim": key, **data}}
            
    return {"status": "not_found", "message": f"'{product_name}' isimli ürün stoklarımızda bulunamadı."}