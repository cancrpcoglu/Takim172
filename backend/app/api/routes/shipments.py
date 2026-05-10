from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.shipment import Shipment

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("")
def create_shipment(order_id: int, cargo_company: str, tracking_number: str = None):
    db: Session = SessionLocal()

    shipment = Shipment(
        order_id=order_id,
        cargo_company=cargo_company,
        tracking_number=tracking_number,
        status="preparing"
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return {
        "success": True,
        "data": shipment
    }



@router.get("")
def get_shipments():
    db: Session = SessionLocal()

    shipments = db.query(Shipment).all()

    return {
        "success": True,
        "data": shipments
    }



@router.get("/{id}")
def get_shipment(id: int):
    db: Session = SessionLocal()

    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        return {"success": False, "message": "Shipment not found"}

    return {
        "success": True,
        "data": shipment
    }



@router.get("/order/{order_id}")
def get_by_order(order_id: int):
    db: Session = SessionLocal()

    shipment = db.query(Shipment).filter(
        Shipment.order_id == order_id
    ).first()

    if not shipment:
        return {"success": False, "message": "Shipment not found"}

    return {
        "success": True,
        "data": shipment
    }



@router.put("/{id}/status")
def update_status(id: int, status: str):
    db: Session = SessionLocal()

    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        return {"success": False, "message": "Shipment not found"}

    shipment.status = status
    db.commit()

    return {
        "success": True,
        "message": "Status updated"
    }



@router.put("/{id}/tracking")
def update_tracking(id: int, tracking_number: str):
    db: Session = SessionLocal()

    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        return {"success": False, "message": "Shipment not found"}

    shipment.tracking_number = tracking_number
    db.commit()

    return {
        "success": True,
        "message": "Tracking updated"
    }



@router.delete("/{id}")
def delete_shipment(id: int):
    db: Session = SessionLocal()

    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        return {"success": False, "message": "Shipment not found"}

    db.delete(shipment)
    db.commit()

    return {
        "success": True,
        "message": "Shipment deleted"
    }