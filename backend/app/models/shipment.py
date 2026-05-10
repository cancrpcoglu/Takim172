from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)

   
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    cargo_company = Column(String(100))
    tracking_number = Column(String(150))
    status = Column(String(50), default="preparing")
    order = relationship("Order", back_populates="shipments")