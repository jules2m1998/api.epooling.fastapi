from typing import List
from fastapi import APIRouter, Depends, status
from controllers import Controllers
from user.controller import Controller as UserPersonController
from user.schemas import PersonSchema, SocietySchema, UserSchema, UserPersonSchema, UserSocietySchema
from user.models import Person, Society, User
from sqlalchemy.orm import Session
from user.utils import create_person_method, setter_person_method, setter_user_method, create_society_method, \
    setter_society_method
from utils import get_db
from auth.auth_bearer import JWTBearer
from auth.utils import oauth2_scheme

# Const declaration

router = APIRouter()
controller = Controllers[Person, PersonSchema](Person)
user_controller = Controllers[User, UserSchema](User)
society_controller = Controllers[Society, SocietySchema](Society)


# -------------------------------------------------------


# Simple user APIs

# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
# async def create_user(request: UserSimpleSchema, db: Session = Depends(get_db)):
#     return user_controller.create(db=db, item=request, method=create_user_method)

@router.put(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    dependencies=[Depends(JWTBearer())]
)
async def update_user(
        request: UserSchema,
        db: Session = Depends(get_db)
):
    return user_controller.update(db=db, id=request.id, item=request, method=setter_user_method)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    return user_controller.get(db=db)


@router.get('/one/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    return user_controller.retrieve(db=db, id=id)


@router.get('/account_token', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return UserPersonController.get_user_by_token(token, db)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
    dependencies=[Depends(JWTBearer())]
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_controller.delete(db=db, id=user_id)


## -------------------------------------------------------

# User type APIs

@router.post('/user_person', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user_person(request: UserPersonSchema, db: Session = Depends(get_db)):
    return UserPersonController.create_user_person(request, db)


@router.post('/user_society', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user_society(request: UserSocietySchema, db: Session = Depends(get_db)):
    return UserPersonController.create_user_society(request, db)


## -------------------------------------------------------


# Person APIs

# Create person api
@router.post('/person', status_code=status.HTTP_201_CREATED)
async def create_person(request: PersonSchema, db: Session = Depends(get_db)):
    return controller.create(db=db, item=request, method=create_person_method)


# Get all persons api
@router.get('/person', status_code=status.HTTP_200_OK)
async def get_persons(db: Session = Depends(get_db)):
    return controller.get(db=db)


# Get person api
@router.get('/person/{id}', status_code=status.HTTP_200_OK)
async def get_person(id: int, db: Session = Depends(get_db)):
    _item = controller.retrieve(db=db, id=id)
    return _item


# update person api
@router.put(
    '/person',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTBearer())]
)
async def update_person(request: PersonSchema, db: Session = Depends(get_db)):
    return controller.update(db, id=request.id, item=request, method=setter_person_method)


# Delete person api
# @router.delete('/person/{id}', status_code=status.HTTP_200_OK)
# async def delete(id: int, response: Response, db: Session = Depends(get_db)):
#     return controller.delete(db, id=id)


## -------------------------------------------------------


# Society APIs

# Create society api
@router.post('/society', status_code=status.HTTP_201_CREATED, response_model=SocietySchema)
async def create_society(request: SocietySchema, db: Session = Depends(get_db)):
    return society_controller.create(db=db, item=request, method=create_society_method)


@router.get('/society', status_code=status.HTTP_200_OK, response_model=List[SocietySchema])
async def get_societies(db: Session = Depends(get_db)):
    return society_controller.get(db=db)


@router.get('/society{id}', status_code=status.HTTP_200_OK, response_model=SocietySchema)
async def get_society(id: int, db: Session = Depends(get_db)):
    return society_controller.retrieve(db=db, id=id)


@router.put(
    '/society',
    status_code=status.HTTP_200_OK,
    response_model=SocietySchema,
    dependencies=[Depends(JWTBearer())]
)
async def update_society(request: SocietySchema, db: Session = Depends(get_db)):
    return society_controller.update(db=db, id=request.id, item=request, method=setter_society_method)

# @router.delete('/society/{id}', status_code=status.HTTP_200_OK, response_model=SocietySchema)
# async def delete_society(id: int, db: Session = Depends(get_db)):
#     return society_controller.delete(db=db, id=id)
