
from config import SessionLocal
from .schemas import PersonSchema, UserSchema
from .models import Person, User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_person_method(p: PersonSchema):
    _p = Person(
        first_name=p.first_name, 
        last_name=p.last_name, 
        sex=p.sex, 
        user_id=p.user_id
    )
    return _p


def setter_person_method(p: Person, subperson: PersonSchema):
    p.first_name = subperson.first_name
    p.last_name = subperson.last_name
    p.user_id = subperson.phone_ex
    p.sex = subperson.sex

    return p


def create_user_method(u: UserSchema):
    _u = User(
        phone = u.phone,
        phone_ex = u.phone_ex,
        avatar_url = u.avatar_url,
        email = u.email,
        account_id = u.account_id
    )
    return _u


def setter_user_method(_u: User, u: UserSchema):
    _u.phone = u.phone
    _u.phone_ex = u.phone_ex
    _u.avatar_url = u.avatar_url
    _u.email = u.email

    return _u
