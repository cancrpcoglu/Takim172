from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Shipment(Base):
    __tablename__ = "shipments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    # unique=True: Aynı order_id ikinci kez bu tabloya giremez!
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    cargo_company = Column(String(100))
    tracking_number = Column(String(150), unique=True) # Takip numarası da benzersiz olmalı
    status = Column(String(50), default="preparing")

    order = relationship("Order", back_populates="shipment") # "shipments" yerine "shipment" (tekil)
    
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)