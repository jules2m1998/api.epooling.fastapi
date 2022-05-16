from user.schemas import UserPersonSchema, UserSocietySchema
from sqlalchemy.orm import Session
from user.utils import create_user_method
from user.models import Person, Society, User
from exception import bad_request
from auth.models import Account
from exception import not_found_404, credentials_exception
from auth.utils import decode_token


class Controller:

    @staticmethod
    def create_user_person(u: UserPersonSchema, db: Session):
        _u = create_user_method(u)
        _p = Person(
            first_name=u.first_name,
            last_name=u.last_name,
            sex=u.sex
        )

        try:
            db.add(_u)
            db.flush()
            _p.user_id = _u.id
            db.add(_p)
            db.commit()
            db.refresh(_u)
            db.refresh(_p)
        except Exception as es:
            db.rollback()
            raise es
        return _u

    @staticmethod
    def create_user_society(u: UserSocietySchema, db: Session):
        _u = create_user_method(u=u)
        _s = Society(
            desc=u.desc,
            location=u.location
        )

        try:
            db.add(_u)
            db.flush()
            _s.user_id = _u.id
            db.add(_s)
            db.commit()
            db.refresh(_u)
            db.refresh(_s)
        except Exception as es:
            print(es)
            db.rollback()
            raise bad_request
        return _u

    @staticmethod
    def get_by_username(username: str, db: Session):
        _u = db.query(User).join(Account).filter(Account.username == username).first()
        if _u is not None:
            return _u
        raise not_found_404

    @staticmethod
    def get_by_id(id: int, db: Session):
        print(db)
        return db.query(User).join(Account).filter(User.id == id).first()

    @staticmethod
    def get_user_by_token(token: str, db: Session):
        print(token)
        try:
            username = decode_token(token)
            return Controller.get_by_username(username, db)
        except:
            raise credentials_exception
