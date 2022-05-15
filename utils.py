from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config import SessionLocal


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()