from typing import Generic, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from config import Base
from typing import TypeVar

from user.models import Person
from user.schemas import PersonSchema

T = TypeVar('T', bound=Base)

class UserController():
    def __init__(self, cls: T) -> None:
        self.cls = cls

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Person]:
        return db.query(self.cls).offset(skip).limit(limit).all()

    def get_by_id(self,db: Session, id: int = 0,) -> Person:
        return db.query(Person).filter(Person.id == id).first()

    def create(self, db: Session, item: PersonSchema) -> Person:
        _item = Person(first_name = item.first_name, last_name = item.last_name, sex=item.sex, phone = item.phone, phone_ex = item.phone_ex)
        db.add(_item)
        db.commit()
        db.refresh(_item)
        return _item

    def update(self, db: Session, id: int, item: PersonSchema) -> Person:
        _item = self.get_by_id(db=db, id=id)

        for attr, _ in _item.__dict__.iteritems():
            _item[attr] = item[attr]
        
        db.commit()
        db.refresh(_item)
        return _item


    def delete(self, db: Session, id: int = 0) -> Person:
        _item = self.get_by_id(db=db, id=id)
        db.delete(_item)
        db.commit()
        return _item