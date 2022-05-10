from typing import Any
from sqlalchemy import  Column, Integer, String
from config import Base

class Account(Base):
    __tablename__ ="account"
    id = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, nullable=False)
    hashed_password: str = Column(String, nullable=False)