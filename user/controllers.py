from pprint import pprint
from .schemas import UserPersonSchema
from sqlalchemy.orm import Session
from .utils import create_user_method
from .models import Person
from exception import bad_request


class Controller:

    @staticmethod
    def create_user_person(u: UserPersonSchema, db: Session):
        _u = create_user_method(u)
        _p = Person(
            first_name= u.first_name, 
            last_name=  u.last_name, 
            sex=  u.sex
        )

        try:
            db.add(_u)
            db.flush()
            _p.user_id = _u.id
            db.add(_p)
            db.commit()
            db.refresh(_u)
            db.refresh(_p)
        except:
            db.rollback()
            raise bad_request
        return _u