from user.schemas import UserPersonSchema, UserSocietySchema, UserSchema, UserInSchema, SocietyInSchema, PersonInSchema
from sqlalchemy.orm import Session
from user.utils import create_user_method
from user.models import Person, Society, User
from auth.models import Account
from exception import not_found_404, credentials_exception
from auth.utils import decode_token
from fastapi import UploadFile, HTTPException, status
from typing import Union
from utils import copy_value
from utils import create_file


class Controller:

    @staticmethod
    def save(db: Session, _i: User, _h: Union[Person, Society]):
        try:
            db.add(_i)
            db.flush()
            _h.user_id = _i.id
            db.add(_h)
            db.commit()
            db.refresh(_i)
            db.refresh(_h)
        except Exception as es:
            db.rollback()
            raise es
        return _i

    @staticmethod
    def phone_number_exist(phone: int, db: Session):
        user_phone: User = db.query(User).filter(User.phone == phone).first()
        if user_phone is not None:
            return True
        return False

    @staticmethod
    def create_user_person(u: UserPersonSchema, db: Session, avatar: UploadFile = None):
        if not Controller.phone_number_exist(u.phone, db):
            if avatar is not None:
                file_location = create_file(
                    file_location=u.account_id,
                    file=avatar,
                    file_dir='user'
                )
            else:
                file_location = 'static/default-user.webp'

            u.avatar_url = file_location
            _u = create_user_method(u=UserSchema(**u.dict(), id=0))
            _p = Person(
                first_name=u.first_name,
                last_name=u.last_name,
                sex=u.sex
            )
            return Controller.save(db, _u, _p)
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        'message': 'Le numeros de telephone est deja utilise',
                        'field': 'phone'
                    }
                ]
            )

    @staticmethod
    def create_user_society(u: UserSocietySchema, db: Session, avatar: UploadFile = None):
        if avatar is not None:
            file_location = create_file(
                file_location=u.account_id,
                file=avatar,
                file_dir='user'
            )

        else:
            file_location = 'static/default-society.png'

        u.avatar_url = file_location
        _u = create_user_method(u=UserSchema(**u.dict(), id=0))
        _s = Society(
            desc=u.desc,
            location=u.location,
            name=u.name
        )

        return Controller.save(db, _u, _s)

    @staticmethod
    def get_by_username(username: str, db: Session):
        _u = db.query(User).join(Account).filter(Account.username == username).first()
        if _u is not None:
            return _u
        raise not_found_404

    @staticmethod
    def get_by_id(id: int, db: Session):
        _u = db.query(User).filter(User.id == id).first()
        if _u is not None:
            return _u
        raise not_found_404

    @staticmethod
    def get_society_by_id(id: int, db: Session):
        _s = db.query(Society).filter(Society.id == id).first()
        if _s is not None:
            return _s
        raise not_found_404

    @staticmethod
    def get_person_by_id(id: int, db: Session) -> Person:
        _s: Person = db.query(Person).filter(Society.id == id).first()
        if _s is not None:
            return _s
        raise not_found_404

    @staticmethod
    def get_user_by_token(token: str, db: Session):
        try:
            username = decode_token(token)
            return Controller.get_by_username(username, db)
        except Exception as e:
            print(e)
            raise credentials_exception

    @staticmethod
    def update_user(id: int, u: UserInSchema, db: Session):
        _u: User = Controller.get_by_id(id, db)
        print(u.avatar)
        if not Controller.phone_number_exist(u.phone, db):
            if _u.avatar_url and u.avatar:
                _u.avatar_url = create_file(
                    old_file_name=_u.avatar_url,
                    file_location=str(_u.id),
                    file=u.avatar, file_dir='user'
                )
            elif u.avatar:
                _u.avatar_url = create_file(
                    old_file_name=None,
                    file_location=str(_u.id),
                    file=u.avatar,
                    file_dir='user'
                )
            copy_value(_u, u, ['avatar'])
            db.commit()
            db.refresh(_u)
            return _u
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        'message': 'Le numeros de telephone est deja utilise',
                        'field': 'phone'
                    }
                ]
            )

    @staticmethod
    def update_user_society(id: int, s: SocietyInSchema, db: Session):
        _s = Controller.get_society_by_id(id, db)
        copy_value(_s, s)
        db.commit()
        return _s

    @staticmethod
    def update_user_person(id: int, p: PersonInSchema, db: Session) -> Person:
        _p: Person = Controller.get_person_by_id(id, db)
        copy_value(_p, p)
        db.commit()
        return _p
