from announce.models import Announce, City
from itinerary.models import Itinerary, ItineraryCity
from announce.schemas import AnnounceUpdateSchema, CitySchema, AnnounceInSchema, \
    AnnounceItineraryInSchema, AnnounceItineraryInOptionalSchema, AnnounceInOptionalSchema, ItineraryCitiesInSchema
from sqlalchemy.orm import Session
from exception import not_found_404
import base64
from utils import create_file_with_bytes, file_base64_regex, copy_value
import re
import imghdr
from datetime import datetime


class AnnounceController:
    @staticmethod
    def create(db: Session, announce: AnnounceInSchema):
        _announce = Announce(
            **announce.dict()
        )
        db.add(_announce)
        db.commit()
        db.refresh(_announce)
        return _announce

    @staticmethod
    def create_itinerary_cities(db: Session, itinerary: ItineraryCitiesInSchema, announce_id: int):
        _itinerary = Itinerary(
            start_date=itinerary.start_date,
            end_date=itinerary.end_date,
            announce_id=announce_id,
            name=itinerary.name
        )
        db.add(_itinerary)
        db.flush()
        _id = 0
        for city in itinerary.cities:
            _city = ItineraryCity(
                city_id=city.id,
                itinerary_id=_itinerary.id,
                order=_id,
                price=city.price,
                date=city.date
            )
            db.add(_city)
            _id += 1

    @staticmethod
    def create_with_itinerary(db: Session, announce: AnnounceItineraryInSchema) -> AnnounceInSchema:
        image_data = base64.b64decode(re.sub(file_base64_regex, '', announce.image))
        ext = imghdr.what('', image_data)

        try:
            _announce = Announce(
                description=announce.description,
                image=create_file_with_bytes(
                    bytes_file=image_data,
                    file_location=f'announce/{announce.user_id}',
                    file_ext=ext
                ),
                volume=announce.volume,
                user_id=announce.user_id
            )
            db.add(_announce)
            db.flush()
            _itinerary = Itinerary(
                start_date=announce.itinerary.start_date,
                end_date=announce.itinerary.end_date,
                announce_id=_announce.id,
                name=announce.itinerary.name
            )
            db.add(_itinerary)
            db.flush()
            _id = 0
            for city in announce.itinerary.cities:
                _city = ItineraryCity(
                    city_id=city.id,
                    itinerary_id=_itinerary.id,
                    order=_id,
                    price=city.price,
                    date=city.date
                )
                db.add(_city)
                _id += 1
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return _announce

    @staticmethod
    def get_all(db: Session, start: int, end: int) -> [Announce]:
        if all(v is not None for v in [start, end]):
            first_list = db.query(Announce).join(Itinerary).join(ItineraryCity).join(City).filter(City.id == start).all()
            second_list = db.query(Announce).join(Itinerary).join(ItineraryCity).join(City).filter(City.id == end).all()
            intersect: [Announce] = list(set(first_list) & set(second_list))
            result = []
            for it in intersect:
                itinerary_city = it.itinerary.itinerary_city
                start_it = end_it = None
                for itc in itinerary_city:
                    print(itc.date > datetime.now())
                    if itc.city_id == start:
                        print(itc.city_id, 'start')
                        start_it = itc
                    elif itc.city_id == end:
                        print(itc.city_id, 'end')
                        end_it = itc
                if all(v is not None for v in [start_it, end_it]):
                    if start_it.order < end_it.order and start_it.date > datetime.now():
                        result.append(it)
            return result
        return db.query(Announce).order_by(Announce.created_at.desc()).all()

    @staticmethod
    def get_all_by_user_id(db: Session, user_id: int):
        print(user_id)
        return db.query(
            Announce
        ).filter(
            Announce.user_id == user_id
        ).order_by(Announce.created_at.desc()).all()

    @staticmethod
    def get_by_id(db: Session, id: int):
        _announce = db.query(Announce).filter(Announce.id == id).first()
        if _announce:
            return _announce
        raise not_found_404

    @staticmethod
    def update(db: Session, announce: AnnounceUpdateSchema):
        _announce = AnnounceController.get_by_id(db, announce.id)
        _announce.description = announce.description
        _announce.image = announce.image
        _announce.volume = announce.volume
        _announce.is_delivery = announce.is_delivery
        db.commit()
        return _announce

    @staticmethod
    def update_with_itinerary(db: Session, announce: AnnounceItineraryInOptionalSchema, _id: int):
        _announce: Announce = AnnounceController.get_by_id(db, _id)
        announce_schema = AnnounceInOptionalSchema(**announce.dict())
        try:
            copy_value(_announce, announce_schema)
            if announce.itinerary:
                it = db.query(Itinerary).filter(Itinerary.announce_id == _announce.id).first()
                db.delete(it)
                AnnounceController.create_itinerary_cities(db, announce.itinerary, _announce.id)
            db.commit()
            return _announce
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(db: Session, id: int):
        print(id)
        _announce = AnnounceController.get_by_id(db, id)
        db.delete(_announce)
        db.commit()
        return _announce


class CityController:
    @staticmethod
    def get_all(db: Session):
        return db.query(City).all()

    @staticmethod
    def get_by_id(db: Session, city_id: int):
        _city = db.query(City).filter(City.id == city_id).first()
        if _city:
            return _city
        raise not_found_404

    @staticmethod
    def create(db: Session, city: CitySchema):
        _city = City(**city.dict())
        db.add(_city)
        db.commit()
        db.refresh(_city)
        return _city
