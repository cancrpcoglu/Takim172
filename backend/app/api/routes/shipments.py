from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.services.shipment_service import ShipmentService
from backend.app.core.security import get_current_user, require_role

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

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_shipment(
    order_id: int = Body(...),
    cargo_company: str = Body(...),
    tracking_number: str = Body(None),
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    
    
    shipment = ShipmentService.create_shipment(
        db,
        order_id,
        cargo_company,
        tracking_number
    )

    return {
        "success": True,
        "message": "Shipment created",
        "data": shipment
    }

@router.get("/")
def get_shipments(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    shipments = ShipmentService.get_shipments(db)
    return {
        "success": True,
        "data": shipments
    }

@router.get("/{id}")
def get_shipment(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    shipment = ShipmentService.get_by_id(db, id)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return {
        "success": True,
        "data": shipment
    }

@router.get("/order/{order_id}")
def get_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    shipment = ShipmentService.get_by_order(db, order_id)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found for this order")

    return {
        "success": True,
        "data": shipment
    }

@router.put("/{id}/status")
def update_status(
    id: int,
    status: str = Body(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    ShipmentService.update_status(db, id, status)

    return {
        "success": True,
        "message": f"Shipment status updated to {status}"
    }

@router.put("/{id}/tracking")
def update_tracking(
    id: int,
    tracking_number: str = Body(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    ShipmentService.update_tracking(db, id, tracking_number)

    return {
        "success": True,
        "message": "Tracking number updated"
    }

@router.delete("/{id}")
def delete_shipment(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    ShipmentService.delete_shipment(db, id)

    return {
        "success": True,
        "message": "Shipment deleted"
    }