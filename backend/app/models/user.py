
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="user") 
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
