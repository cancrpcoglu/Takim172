from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.seller import Seller

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


# POST /sellers/register
@router.post("/register")
def register_seller(
    user_id: int,
    store_name: str,
    description:str,
    rating:int,
    
):
    db: Session = SessionLocal()

    new_seller = Seller(
        user_id=user_id,
        store_name=store_name,
        description=description,
        rating=rating
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    return {
        "success": True,
        "data": new_seller
    }


# GET /sellers
@router.get("/")
def get_sellers():
    db: Session = SessionLocal()

    sellers = db.query(Seller).all()

    return {
        "success": True,
        "data": sellers
    }


# GET /sellers/me
@router.get("/me")
def get_my_seller(user_id: int):
    db: Session = SessionLocal()

    seller = db.query(Seller).filter(
        Seller.user_id == user_id
    ).first()

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "data": seller
    }


# GET /sellers/{id}
@router.get("/{id}")
def get_seller(id: int):
    db: Session = SessionLocal()

    seller = db.query(Seller).filter(
        Seller.id == id
    ).first()

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    return {
        "success": True,
        "data": seller
    }


# PUT /sellers/{id}
@router.put("/{id}")
def update_seller(
    id: int,
    store_name: str,
    description:str,
    rating:int,
):
    db: Session = SessionLocal()

    seller = db.query(Seller).filter(
        Seller.id == id
    ).first()

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    seller.store_name = store_name
    description=description,
    rating=rating

    db.commit()

    return {
        "success": True,
        "message": "Seller updated"
    }


# DELETE /sellers/{id}
@router.delete("/{id}")
def delete_seller(id: int):
    db: Session = SessionLocal()

    seller = db.query(Seller).filter(
        Seller.id == id
    ).first()

    if not seller:
        return {
            "success": False,
            "message": "Seller not found"
        }

    db.delete(seller)
    db.commit()

    return {
        "success": True,
        "message": "Seller deleted"
    }