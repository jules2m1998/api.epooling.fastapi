from typing import Generic, List, TypeVar
from config import Base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from exception import not_found_404, bad_request

T = TypeVar('T', bound=Base)
TS = TypeVar('TS', bound=BaseModel)


class Controllers(Generic[T, TS]):

    def __init__(self, cls: T) -> None:
        self.cls = cls

    @staticmethod
    def create(db: Session, item: TS, method: callable) -> T:
        _item = method(item)
        try:
            db.add(_item)
            db.commit()
            db.refresh(_item)
        except IntegrityError as ie:
            raise bad_request
        return _item

    def get(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        try:
            return db.query(self.cls).offset(skip).limit(limit).all()
        except Exception as es:
            print(es)
            raise es

    def retrieve(self, db: Session, id: int = 0, ) -> T:
        _item = db.query(self.cls).filter(self.cls.id == id).first()
        if _item:
            return _item
        else:
            raise not_found_404

    def retrieve_username(self, db: Session, username: str = 0, ) -> T:
        _item = db.query(self.cls).filter(self.cls.username == username).first()
        if _item:
            return _item
        else:
            raise not_found_404

    def update(self, db: Session, id: int, item: TS, method: callable) -> TS:
        _item = self.retrieve(db=db, id=id)
        if _item:
            _item = method(_item, item)
            db.commit()
            db.refresh(_item)
            return _item
        else:
            raise not_found_404

    def delete(self, db: Session, id: int = 0) -> T:
        _item = self.retrieve(db=db, id=id)
        print(_item)
        if _item:
            db.delete(_item)
            db.commit()
            return _item
        else:
            raise not_found_404
