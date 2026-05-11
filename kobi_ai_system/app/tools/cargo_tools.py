import asyncio
from langchain_core.tools import tool
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal
from backend.app.models.shipment import Shipment

@tool
async def track_cargo(order_id: str) -> dict:
    """Kargo takip numarası (tracking_number) ile kargo durumunu sorgular."""
    db: Session = SessionLocal()
    try:
       
        clean_id = order_id.upper().replace(" ", "").strip()

        shipment = (
            db.query(Shipment)
            .filter(Shipment.tracking_number == clean_id)
            .filter(Shipment.is_deleted == False)
            .first()
        )

        if not shipment:
            return {"status": "not_found", "message": f"{order_id} numaralı kargo bulunamadı."}

       
        status_map = {"preparing": "Hazırlanıyor", "shipped": "Kargoya Verildi", "delivered": "Teslim Edildi"}
        current_status = status_map.get(shipment.status, shipment.status)

        return {
            "status": "success",
            "data": {
                "takip_no": shipment.tracking_number,
                "durum": current_status,
                "kargo_firmasi": shipment.cargo_company,
                "guncelleme": shipment.updated_at.strftime("%d/%m/%Y %H:%M")
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()