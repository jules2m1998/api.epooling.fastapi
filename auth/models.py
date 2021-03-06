from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config import Base


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return "<Account %r>" % self.username
