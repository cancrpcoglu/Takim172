from pydantic import BaseModel
from typing import Optional


class ShipmentCreate(BaseModel):
    order_id: int
    cargo_company: Optional[str] = None
    tracking_number: Optional[str] = None
    status: str = "preparing"



class ShipmentUpdate(BaseModel):
    cargo_company: Optional[str] = None
    tracking_number: Optional[str] = None
    status: Optional[str] = None



class ShipmentResponse(BaseModel):
    id: int
    order_id: int
    cargo_company: Optional[str]
    tracking_number: Optional[str]
    status: str

    class Config:
        from_attributes = True