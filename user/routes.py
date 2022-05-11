from typing import List
from fastapi import APIRouter, Depends, Response, status
from config import SessionLocal
from controllers import Controllers
from .schemas import PersonSchema, UserSchema
from .models import Person, User
from sqlalchemy.orm import Session


router = APIRouter()
controller = Controllers[Person, PersonSchema](Person)
user_conttroller = Controllers[User, UserSchema](User)


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
    )
    return _u


def setter_user_method(_u: User, u: UserSchema):
    _u.phone = u.phone
    _u.phone_ex = u.phone_ex
    _u.avatar_url = u.avatar_url
    _u.email = u.email

    return _u


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(request: UserSchema, db: Session = Depends(get_db)):
    return user_conttroller.create(db=db, item=request, method=create_user_method)


@router.put('/', status_code=status.HTTP_200_OK)
async def uppdate_user(request: UserSchema, db: Session = Depends(get_db)):
    return user_conttroller.create(db=db, item=request, method=setter_user_method)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    return user_conttroller.get(db=db)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user_conttroller.retrieve(db=db, id=id)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_user(id: int, db: Session = Depends(get_db)):
    return user_conttroller.delete(db=db, id=id)



@router.post('/person', status_code=status.HTTP_201_CREATED)
async def create_person(request: PersonSchema, response: Response, db: Session = Depends(get_db)):
    try:
        return controller.create(db=db, item = request, method = create_person_method)
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'detail': 'Bad request !'
        }

@router.get('/person', status_code=status.HTTP_200_OK)
async def get_persons(db: Session = Depends(get_db)):
    return controller.get(db=db)

@router.get('/person/{id}', status_code=status.HTTP_200_OK)
async def get_person(id: int, db: Session = Depends(get_db)):
    _item = controller.retrieve(db=db, id=id)
    return _item

@router.put('/person', status_code=status.HTTP_200_OK)
async def get_persons(request: PersonSchema, db: Session = Depends(get_db)):
    return controller.update(db, id=request.id, item=request, method = setter_person_method)

@router.delete('/person/{id}', status_code=status.HTTP_200_OK)
async def get_persons(id: int, response: Response, db: Session = Depends(get_db)):
    return controller.delete(db, id=id)
