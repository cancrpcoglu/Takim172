from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(String, default="pending")
    shipments = relationship("Shipment", back_populates="order")