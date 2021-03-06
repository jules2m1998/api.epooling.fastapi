from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from config import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(Integer, nullable=False, unique=True)
    phone_ex = Column(String, nullable=False)
    avatar_url = Column(Text)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    account_id = Column(Integer, ForeignKey('account.id'))

    person = relationship("Person", back_populates='user', uselist=False, cascade="all, delete", lazy='joined')
    society = relationship("Society", back_populates='user', uselist=False, cascade="all, delete", lazy='joined')
    account = relationship("Account")

    def __repr__(self):
        return "<User %r>" % self.id


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates='person', uselist=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return "<Person %r>" % self.id


class Society(Base):
    __tablename__ = "society"
    id = Column(Integer, primary_key=True, index=True)
    desc = Column(String, nullable=False)
    location = Column(String, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates='society', uselist=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return "<Society %r>" % self.id
