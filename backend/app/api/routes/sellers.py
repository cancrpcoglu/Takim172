from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.seller_service import SellerService
from app.core.security import get_current_user, require_role

router = APIRouter(
    prefix="/sellers",
    tags=["Sellers"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_seller(
   
    store_name: str = Body(...),
    description: str = Body(...),
    rating: int = Body(0), # Varsayılan değer 0
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
   
    current_user_id = user.get("user_id")

    seller = SellerService.register_seller(
        db,
        current_user_id,   
        store_name,
        description,
        rating
    )

    return {
        "success": True,
        "message": "Seller created",
        "data": seller
    }

@router.get("/")
def get_sellers(db: Session = Depends(get_db)):
    sellers = SellerService.get_sellers(db)
    return {
        "success": True,
        "data": sellers
    }

@router.get("/me")
def get_my_seller(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    current_user_id = user.get("user_id")
    seller = SellerService.get_by_user(db, current_user_id)

    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")

    return {
        "success": True,
        "data": seller
    }

@router.get("/{id}")
def get_seller(id: int, db: Session = Depends(get_db)):
    seller = SellerService.get_by_id(db, id)

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    return {
        "success": True,
        "data": seller
    }

@router.put("/{id}")
def update_seller(
    id: int,
    store_name: str = Body(...),
    description: str = Body(...),
    rating: int = Body(...),
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    seller = SellerService.get_by_id(db, id)

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    
    if seller.user_id != user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not your seller profile")

    updated_seller = SellerService.update_seller(
        db, id, store_name, description, rating
    )

    return {
        "success": True,
        "message": "Seller updated",
        "data": updated_seller
    }

@router.delete("/{id}")
def delete_seller(
    id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    seller = SellerService.get_by_id(db, id)

    if not seller:
        raise HTTPException(status_code=404, detail="Seller not found")

    if seller.user_id != user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not your seller profile")

    SellerService.delete_seller(db, id)

    return {
        "success": True,
        "message": "Seller deleted"
    }