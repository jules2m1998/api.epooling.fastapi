from announce.models import Announce, City
from announce.schemas import AnnounceUpdateSchema, CitySchema, AnnounceInSchema
from sqlalchemy.orm import Session
from exception import not_found_404


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

