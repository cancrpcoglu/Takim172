from sqlalchemy import Column, Boolean, DateTime
from datetime import datetime


class BaseModel:
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    is_deleted = Column(Boolean, default=False)