from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.seller_service import SellerService

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



@router.post("/register")
def register_seller(
    user_id: int,
    store_name: str,
    description: str,
    rating: int,
    db: Session = Depends(get_db)
):

    seller = SellerService.register_seller(
        db, user_id, store_name, description, rating
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
def get_my_seller(user_id: int, db: Session = Depends(get_db)):

    seller = SellerService.get_by_user(db, user_id)

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "data": seller
    }



@router.get("/{id}")
def get_seller(id: int, db: Session = Depends(get_db)):

    seller = SellerService.get_by_id(db, id)

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "data": seller
    }



@router.put("/{id}")
def update_seller(
    id: int,
    store_name: str,
    description: str,
    rating: int,
    db: Session = Depends(get_db)
):

    seller = SellerService.update_seller(
        db, id, store_name, description, rating
    )

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "message": "Seller updated"
    }



@router.delete("/{id}")
def delete_seller(id: int, db: Session = Depends(get_db)):

    seller = SellerService.delete_seller(db, id)

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "message": "Seller deleted"
    }