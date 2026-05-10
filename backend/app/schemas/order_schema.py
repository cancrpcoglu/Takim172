from pydantic import BaseModel
from typing import Optional


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class OrderUpdateStatus(BaseModel):
    status: str



class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    status: str

    class Config:
        from_attributes = True