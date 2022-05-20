from announce.models import Announce, City
from itinerary.models import Itinerary, ItineraryCity
from announce.schemas import AnnounceUpdateSchema, CitySchema, AnnounceInSchema, AnnounceItineraryInSchema
from sqlalchemy.orm import Session
from exception import not_found_404
import base64
from utils import create_file_with_bytes, file_base64_regex
import re
import imghdr


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
            print(announce.itinerary.cities)
            _id = 0
            for city in announce.itinerary.cities:
                _city = ItineraryCity(
                    city_id=city.id,
                    itinerary_id=_itinerary.id,
                    order=_id,
                    price=city.price
                )
                db.add(_city)
                _id += 1
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return _announce

    @staticmethod
    def get_all(db: Session):
        return db.query(Announce).all()

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
    def delete(db: Session, id: int):
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
