from user.schemas import UserPersonSchema, UserSocietySchema, UserSchema, UserInSchema, SocietyInSchema, PersonInSchema
from sqlalchemy.orm import Session
from user.utils import create_user_method
from user.models import Person, Society, User
from auth.models import Account
from exception import not_found_404, credentials_exception
from auth.utils import decode_token
from fastapi import UploadFile
from typing import Union
import uuid
import os
from os.path import join, exists
from pathlib import Path
from utils import copy_value


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
    def create_file(old_file_name: Union[str, None] = None, file_location: Union[str, int] = '', file: UploadFile = ''):
        if old_file_name is not None:
            file_path = join(Path(__file__).parent.parent.absolute(), old_file_name)
            if exists(file_path):
                os.remove(file_path)
        file_location = f"static/{file_location}_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return file_location

    @staticmethod
    def create_user_person(u: UserPersonSchema, db: Session, avatar: UploadFile = None):
        if avatar is not None:
            file_location = Controller.create_file(
                file_location=u.account_id,
                file=avatar
            )
        else:
            file_location = None

        u.avatar_url = file_location
        _u = create_user_method(u=UserSchema(**u.dict(), id=0))
        _p = Person(
            first_name=u.first_name,
            last_name=u.last_name,
            sex=u.sex
        )
        return Controller.save(db, _u, _p)

    @staticmethod
    def create_user_society(u: UserSocietySchema, db: Session, avatar: UploadFile = None):
        if avatar is not None:
            file_location = Controller.create_file(
                file_location=u.account_id,
                file=avatar
            )
        else:
            file_location = None

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
        if _u.avatar_url and u.avatar:
            _u.avatar_url = Controller.create_file(old_file_name=_u.avatar_url, file_location=str(_u.id), file=u.avatar)
        elif u.avatar:
            _u.avatar_url = Controller.create_file(old_file_name=None, file_location=str(_u.id), file=u.avatar)
        copy_value(_u, u, ['avatar'])
        db.commit()
        return _u

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


