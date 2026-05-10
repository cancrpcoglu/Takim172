from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_order(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):

    order = OrderService.create_order(db, user_id, product_id, quantity)

    return {
        "success": True,
        "message": "Order created",
        "data": order
    }


@router.get("/")
def get_orders(db: Session = Depends(get_db)):

    orders = OrderService.get_orders(db)

    return {
        "success": True,
        "data": orders
    }


@router.get("/my")
def get_my_orders(user_id: int, db: Session = Depends(get_db)):

    orders = OrderService.get_my_orders(db, user_id)

    return {
        "success": True,
        "data": orders
    }


@router.get("/{id}")
def get_order(id: int, db: Session = Depends(get_db)):

    order = OrderService.get_by_id(db, id)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "data": order
    }



@router.put("/{id}/cancel")
def cancel_order(id: int, db: Session = Depends(get_db)):

    order = OrderService.cancel_order(db, id)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "message": "Order cancelled"
    }



@router.put("/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(get_db)):

    order = OrderService.update_status(db, id, status)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "message": "Order status updated"
    }



@router.delete("/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):

    order = OrderService.delete_order(db, id)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "message": "Order deleted"
    }