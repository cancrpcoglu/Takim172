from sqlalchemy import Column, Integer, String, Float, Boolean,DateTime
from backend.app.core.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer)

    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  