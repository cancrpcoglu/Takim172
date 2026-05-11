from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.order_service import OrderService
from app.core.security import get_current_user, require_role

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


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    # Body kullanarak Swagger'da kutucukların çıkmasını sağlıyoruz
    product_id: int = Body(...),
    quantity: int = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
   
    current_user_id = user.get("user_id")
    
    order = OrderService.create_order(
        db,
        current_user_id,
        product_id,
        quantity
    )

    return {
        "success": True,
        "message": "Order created",
        "data": order
    }


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    orders = OrderService.get_orders(db)
    return {
        "success": True,
        "data": orders
    }


@router.get("/my")
def get_my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    current_user_id = user.get("user_id")
    orders = OrderService.get_my_orders(db, current_user_id)
    return {
        "success": True,
        "data": orders
    }


@router.get("/{id}")
def get_order(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = OrderService.get_by_id(db, id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    
    if order.user_id != user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not your order")

    return {
        "success": True,
        "data": order
    }


@router.put("/{id}/cancel")
def cancel_order(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    order = OrderService.get_by_id(db, id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not your order")

    OrderService.cancel_order(db, id)

    return {
        "success": True,
        "message": "Order cancelled"
    }


@router.put("/{id}/status")
def update_status(
    id: int,
    # Status'u Query yerine Body olarak almak Swagger'da daha temiz durur
    status: str = Body(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    OrderService.update_status(db, id, status)
    return {
        "success": True,
        "message": "Order status updated"
    }


@router.delete("/{id}")
def delete_order(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    OrderService.delete_order(db, id)
    return {
        "success": True,
        "message": "Order deleted"
    }