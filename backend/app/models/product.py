from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stock= Column(Integer,nullable=False)
    price = Column(Float, nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
