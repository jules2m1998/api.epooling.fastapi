from typing import Generic, List, TypeVar
from unittest.mock import call
from config import Base
from sqlalchemy.orm import Session
from pydantic import BaseModel
from exception import not_found_404


T = TypeVar('T', bound=Base)
TS = TypeVar('TS', bound=BaseModel)


class Controllers(Generic[T, TS]):

    def __init__(self, cls: T) -> None:
        self.cls = cls

    def create(self, db: Session, item: TS, method: callable) -> T:
        _item = self.cls()
        db.add(method(_item, item))
        db.commit()
        db.refresh(_item)
        return _item

    def get(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        return db.query(self.cls).offset(skip).limit(limit).all()
    
    def retrieve(self,db: Session, id: int = 0,) -> T:
        _item = db.query(self.cls).filter(self.cls.id == id).first()
        if _item:
            return _item
        else:
            raise not_found_404
    
    
    def retrieveUsername(self,db: Session, username: str = 0,) -> T:
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
            print(_item.__dict__)
            return _item
        else:
            raise not_found_404

    def delete(self, db: Session, id: int = 0) -> T:
        _item = self.retrieve(db=db, id=id)
        if _item:
            db.delete(_item)
            db.commit()
            return _item
        else:
            raise not_found_404