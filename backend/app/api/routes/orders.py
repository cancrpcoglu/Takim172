from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.order import Order
from backend.app.models.product import Product
from backend.app.models.seller import Seller
from backend.app.services.order_service import OrderService
from backend.app.core.security import get_current_user, require_role

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
    current_user_id = user.id if hasattr(user, 'id') else user.get("id")
    
    # Eğer kullanıcı satıcıysa, ona gelen siparişleri getir
    if user.role == "seller":
        # 1. Önce bu kullanıcıya ait satıcı (seller) kaydını bul
        seller = db.query(Seller).filter(Seller.user_id == current_user_id).first()
        if not seller:
            return {"success": True, "data": []}
            
        # 2. Satıcının ürünlerine ait olan siparişleri getir (Join işlemi)
        orders = db.query(Order).join(Product).filter(Product.seller_id == seller.id).all()
    else:
        # Müşteriyse kendi verdiklerini getir
        orders = db.query(Order).filter(Order.user_id == current_user_id).all()
    
    return {"success": True, "data": orders}
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