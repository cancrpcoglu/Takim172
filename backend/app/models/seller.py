# app/models/seller.py

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)


    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    store_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rating = Column(Float, default=0.0)
   
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", backref="sellers")