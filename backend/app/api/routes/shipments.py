from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.shipment_service import ShipmentService

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
def create_shipment(
    order_id: int,
    cargo_company: str,
    tracking_number: str = None,
    db: Session = Depends(get_db)
):

    shipment = ShipmentService.create_shipment(
        db, order_id, cargo_company, tracking_number
    )

    return {
        "success": True,
        "message": "Shipment created",
        "data": shipment
    }



@router.get("")
def get_shipments(db: Session = Depends(get_db)):

    shipments = ShipmentService.get_shipments(db)

    return {
        "success": True,
        "data": shipments
    }



@router.get("/{id}")
def get_shipment(id: int, db: Session = Depends(get_db)):

    shipment = ShipmentService.get_by_id(db, id)

    if not shipment:
        return {
            "success": False,
            "message": "Shipment not found"
        }

    return {
        "success": True,
        "data": shipment
    }



@router.get("/order/{order_id}")
def get_by_order(order_id: int, db: Session = Depends(get_db)):

    shipment = ShipmentService.get_by_order(db, order_id)

    if not shipment:
        return {
            "success": False,
            "message": "Shipment not found"
        }

    return {
        "success": True,
        "data": shipment
    }


@router.put("/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):

    shipment = ShipmentService.update_status(db, id, status)

    if not shipment:
        return {
            "success": False,
            "message": "Shipment not found"
        }

    return {
        "success": True,
        "message": "Status updated"
    }


@router.put("/{id}/tracking")
def update_tracking(id: int, tracking_number: str, db: Session = Depends(get_db)):

    shipment = ShipmentService.update_tracking(db, id, tracking_number)

    if not shipment:
        return {
            "success": False,
            "message": "Shipment not found"
        }

    return {
        "success": True,
        "message": "Tracking updated"
    }


@router.delete("/{id}")
def delete_shipment(id: int, db: Session = Depends(get_db)):

    shipment = ShipmentService.delete_shipment(db, id)

    if not shipment:
        return {
            "success": False,
            "message": "Shipment not found"
        }

    return {
        "success": True,
        "message": "Shipment deleted"
    }