from email.mime import base
from sqlalchemy import  Column, Integer, String
from config import Base

class User:
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(Integer, nullable=False)
    phone_ex = Column(String, nullable=False)


class Person(User, Base):
    __tablename__ ="person"
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(Integer, nullable = False)

class Society(User, Base):
    __tablename__ ="society"
    desc = Column(String, nullable = False)
    location = Column(String, nullable = False)