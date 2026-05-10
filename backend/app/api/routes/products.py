from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):

    new_product = Product(**product.dict())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"success": True, "data": new_product}

@router.get("/")
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    return {"success": True, "data": products}

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"success": True, "data": product}

@router.put("/{product_id}")
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return {"success": True, "data": product}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"success": True, "message": "Product deleted"}

