import datetime
from typing import List

from itinerary.models import Itinerary, ItineraryCity
from announce.schemas import ItineraryInSchema, ItinerarySchema, ItineraryInCitySchema
from sqlalchemy.orm import Session
from exception import not_found_404


class ItineraryController:
    @staticmethod
    def create(db: Session, itinerary: ItineraryInSchema):
        _i = Itinerary(
            name=itinerary.name, announce_id=itinerary.announce_id, start_date="2020-04-08T13:09:39.067190", end_date="2020-04-08T13:09:39.067190")
        db.add(_i)
        db.commit()
        db.refresh(_i)
        for city in itinerary.cities:
            city.itinerary_id = _i.id
            _ic = ItineraryCityController.create(db, city)
            db.add(_ic)
        return _i

    @staticmethod
    def create_city(db: Session, id: int, city: ItineraryInCitySchema):
        _i = ItineraryController.get_by_id(db, id)
        city.itinerary_id = _i.id
        _ic = ItineraryCityController.create(db, city)
        db.add(_ic)
        db.commit()
        return _ic

    @staticmethod
    def get_all(db: Session) -> List[ItinerarySchema]:
        return db.query(Itinerary).all()

    @staticmethod
    def get_by_id(db: Session, id: int) -> ItinerarySchema:
        _i = db.query(Itinerary).filter(Itinerary.id == id).first()
        if _i is None:
            raise not_found_404
        return _i

    @staticmethod
    def update(db: Session, id: int, itinerary: ItinerarySchema):
        _i = ItineraryController.get_by_id(db, id)
        _i.name = itinerary.name
        _i.announce_id = itinerary.announce_id
        _i.start_date = itinerary.start_date
        _i.end_date = itinerary.end_date
        db.commit()
        return _i

    @staticmethod
    def delete(db: Session, id: int) ->  ItinerarySchema:
        _i = ItineraryController.get_by_id(db, id)
        db.delete(_i)
        db.commit()
        return _i


class ItineraryCityController:
    @staticmethod
    def create(db: Session, itinerary_city: ItineraryInCitySchema):
        _i = ItineraryCity(**itinerary_city.dict())
        db.add(_i)
        db.commit()
        db.refresh(_i)
        return _i


