from pydantic import BaseModel
from typing import Optional



class SellerCreate(BaseModel):
    user_id: int
    store_name: str
    description: Optional[str] = None


class SellerUpdate(BaseModel):
    store_name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None



class SellerResponse(BaseModel):
    id: int
    user_id: int
    store_name: str
    description: Optional[str]
    rating: float

    class Config:
        from_attributes = True