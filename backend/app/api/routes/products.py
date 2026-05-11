from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone # Modern zaman yönetimi

from app.core.database import SessionLocal
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.product_service import ProductService
from app.core.security import require_role

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))   
):
    
    seller_id = user.get("user_id")

    result = ProductService.create_product(
        db=db,
        seller_id=seller_id,
        data=product.model_dump() # dict() yerine model_dump() (Pydantic v2)
    )

    return {
        "success": True,
        "message": "Product created",
        "data": result
    }

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.is_deleted == False
    ).all()

    return {
        "success": True,
        "data": products
    }

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "success": True,
        "data": product
    }

@router.put("/{product_id}")
def update_product(
    product_id: int,
    updated: ProductUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))  
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

  
    if product.seller_id != user.get("user_id"):
        raise HTTPException(status_code=403, detail="Not your product")

    
    update_data = updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["id", "seller_id"]: # Değişmemesi gereken alanlar
            continue
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {
        "success": True,
        "message": "Product updated",
        "data": product
    }

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_role("seller"))
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_deleted == False
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

   

    
    product.is_deleted = True
    product.updated_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "success": True,
        "message": "Product deleted"
    }