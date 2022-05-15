from utils import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from config import Base


class Announce(BaseModel, Base):
    __tablename__ = "announce"

    description = Column(String, nullable=False)
    image = Column(String, nullable=True)
    volume = Column(Integer, nullable=False)
    is_delivery = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', uselist=False, lazy='joined', single_parent=True)
    itinerary = relationship(
        'Itinerary',
        back_populates='announce',
        uselist=False,
        cascade="all,  delete-orphan, save-update",
        lazy='joined'
    )

    def __repr__(self):
        return "<Announce %r>" % self.id


class City(BaseModel, Base):
    __tablename__ = "city"
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<City %r>" % self.id
