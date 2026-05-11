from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Shipment(Base):
    __tablename__ = "shipments"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True, index=True)
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    cargo_company = Column(String(100))
    tracking_number = Column(String(150))
    status = Column(String(50), default="preparing")
 
    order = relationship("Order", back_populates="shipments")
    
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)