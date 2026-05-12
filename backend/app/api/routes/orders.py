from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.order import Order
from backend.app.models.product import Product
from backend.app.models.seller import Seller
from backend.app.services.order_service import OrderService
from backend.app.core.security import get_current_user, require_role

from fastapi.encoders import jsonable_encoder

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload
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
    # Kullanıcı bilgilerini al
    if isinstance(user, dict):
        current_user_id = user.get("user_id") or user.get("id")
        role = user.get("role")
    else:
        current_user_id = user.id
        role = user.role
    
    if role == "seller":
        # Satıcı profilini bul
        seller = db.query(Seller).filter(Seller.user_id == current_user_id).first()
        
        if not seller:
            return {"success": True, "data": [], "message": "Mağaza kaydı bulunamadı."}
        
        # Satıcının ürünlerine gelen siparişleri getir
        orders = db.query(Order).join(Product, Order.product_id == Product.id).filter(
            Product.seller_id == seller.id,
            Order.is_deleted == False
        ).all()
    else:
        # Müşterinin kendi siparişleri
        orders = db.query(Order).filter(
            Order.user_id == current_user_id,
            Order.is_deleted == False
        ).all()
    
    return {
        "success": True, 
        "data": jsonable_encoder(orders)
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
    user=Depends(require_role("seller"))
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