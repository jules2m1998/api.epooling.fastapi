from utils import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from config import Base


class ItineraryCity(BaseModel, Base):
    __tablename__ = 'itinerary_city'

    itinerary_id = Column(Integer, ForeignKey('itinerary.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
    price = Column(Integer)
    order = Column(Integer)
    itinerary = relationship('Itinerary', back_populates='itinerary_city', uselist=False, single_parent=True)
    date = Column(DateTime, nullable=False)
    city = relationship('City')


class Itinerary(BaseModel, Base):
    __tablename__ = "itinerary"

    name = Column(String, nullable=False)
    announce_id = Column(Integer, ForeignKey('announce.id'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    announce = relationship(
        'Announce',
        uselist=False,
        back_populates='itinerary',
        lazy='joined',
        single_parent=True
    )

    itinerary_city = relationship(
        'ItineraryCity',
        back_populates='itinerary',
        cascade="all, delete-orphan, save-update",
    )

    def __repr__(self):
        return "<Itinerary %r>" % self.id