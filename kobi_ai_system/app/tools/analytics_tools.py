from sqlalchemy.orm import Session
from langchain_core.tools import tool
from datetime import datetime, timedelta
from typing import Optional

from backend.app.core.database import SessionLocal
from backend.app.models.order import Order
from backend.app.models.product import Product
from backend.app.models.shipment import Shipment

# -----------------------------
# SALES TOOL
# -----------------------------
@tool
def get_daily_sales_summary(date: Optional[str] = None) -> dict:
    """
    Günlük satış özetini getirir (ciro + sipariş + en çok satan ürün).
    """

    db: Session = SessionLocal()

    try:
        if not date or date.lower() == "bugün":
            target_date = datetime.now().date()
        else:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()

        orders = (
            db.query(Order, Product)
            .join(Product, Order.product_id == Product.id)
            .filter(Order.is_deleted == False)
            .filter(Order.created_at >= target_date)
            .filter(Order.created_at < target_date + timedelta(days=1))
            .all()
        )

        total_orders = len(orders)
        total_revenue = 0
        product_count = {}

        for order, product in orders:
            qty = order.quantity or 0
            price = product.price or 0

            revenue = qty * price
            total_revenue += revenue

            name = product.name or "Unknown"
            product_count[name] = product_count.get(name, 0) + qty

        best_product = (
            max(product_count, key=product_count.get)
            if product_count else None
        )

        return {
            "status": "success",
            "tarih": str(target_date),
            "toplam_siparis": total_orders,
            "toplam_ciro_tl": float(total_revenue),
            "en_cok_satan_urun": best_product
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()


# -----------------------------
# SHIPMENT TOOL
# -----------------------------
@tool
def get_delayed_cargos() -> dict:
    """
    Geciken kargoları getirir.
    """

    db: Session = SessionLocal()

    try:
        shipments = (
            db.query(Shipment)
            .filter(Shipment.status.ilike("delayed"))
            .all()
        )

        return {
            "status": "success",
            "geciken_kargo_sayisi": len(shipments),
            "detaylar": [
                {
                    "shipment_id": s.id,
                    "order_id": s.order_id,
                    "durum": s.status,
                    "kargo_firmasi": s.cargo_company,
                    "takip_no": s.tracking_number
                }
                for s in shipments
            ]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

    finally:
        db.close()