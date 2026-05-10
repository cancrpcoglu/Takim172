from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.order import Order

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


# POST /orders
@router.post("/")
def create_order(
    user_id: int,
    product_id: int,
    quantity: int,
):
    db: Session = SessionLocal()

    new_order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        status="pending"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "success": True,
        "data": {
            "id": new_order.id,
            "status": new_order.status
        }
    }


# GET /orders
@router.get("/")
def get_orders():
    db: Session = SessionLocal()

    orders = db.query(Order).all()

    return {
        "success": True,
        "data": orders
    }


# GET /orders/my
@router.get("/my")
def get_my_orders(user_id: int):
    db: Session = SessionLocal()

    orders = db.query(Order).filter(Order.user_id == user_id).all()

    return {
        "success": True,
        "data": orders
    }


# GET /orders/{id}
@router.get("/{id}")
def get_order(id: int):
    db: Session = SessionLocal()

    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    return {
        "success": True,
        "data": order
    }


# PUT /orders/{id}/cancel
@router.put("/{id}/cancel")
def cancel_order(id: int):
    db: Session = SessionLocal()

    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    order.status = "cancelled"

    db.commit()

    return {
        "success": True,
        "message": "Order cancelled"
    }


# PUT /orders/{id}/status
@router.put("/{id}/status")
def update_order_status(id: int, status: str):
    db: Session = SessionLocal()

    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    order.status = status

    db.commit()

    return {
        "success": True,
        "message": "Order status updated"
    }