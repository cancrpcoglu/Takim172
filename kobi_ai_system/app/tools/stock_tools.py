import asyncio
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.models.product import Product

@tool
async def check_stock_and_price(product_name: str) -> dict:
    """Ürün stok durumunu ve fiyatını veritabanından sorgular."""
    db: Session = SessionLocal()
    try:
       
        product = (
            db.query(Product)
            .filter(Product.is_deleted == False)
            .filter(Product.name.ilike(f"%{product_name}%"))
            .first()
        )

        if not product:
            return {"status": "not_found", "message": f"'{product_name}' ürünü bulunamadı."}

        return {
            "status": "success",
            "data": {
                "id": product.id,
                "isim": product.name,
                "stok": product.stock,
                "fiyat": product.price,
                "birim": "TL"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()