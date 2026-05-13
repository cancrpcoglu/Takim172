from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    price: float
    stock:int
    seller_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    stock:int
    price: float | None = None