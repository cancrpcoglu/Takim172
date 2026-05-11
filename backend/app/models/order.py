
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from backend.app.core.database import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(String, default="pending")

    shipments = relationship("Shipment", back_populates="order", cascade="all, delete-orphan")

    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
   
    product = relationship("Product")