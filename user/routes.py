from typing import List
from fastapi import APIRouter, Depends, Response, status
from controllers import Controllers
from .controllers import Controller as UserPersonController
from .schemas import PersonSchema, SocietySchema, UserSchema, UserPersonSchema, UserSimpleSchema, UserSocietySchema
from .models import Person, Society, User
from sqlalchemy.orm import Session
from .utils import create_person_method, create_user_method, get_db, setter_person_method, setter_user_method, create_society_method, setter_society_method

# Const declaration

router = APIRouter()
controller = Controllers[Person, PersonSchema](Person)
user_conttroller = Controllers[User, UserSchema](User)
society_controller = Controllers[Society, SocietySchema](Society)

# -------------------------------------------------------


# Simple user APIs

# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
# async def create_user(request: UserSimpleSchema, db: Session = Depends(get_db)):
#     return user_conttroller.create(db=db, item=request, method=create_user_method)


@router.put('/', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def uppdate_user(request: UserSchema, db: Session = Depends(get_db)):
    return user_conttroller.update(db=db, id=request.id, item=request, method=setter_user_method)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    return user_conttroller.get(db=db)


@router.get('/one/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    u = user_conttroller.retrieve(db=db, id=id)
    return user_conttroller.retrieve(db=db, id=id)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def delete_user(id: int, db: Session = Depends(get_db)):
    return user_conttroller.delete(db=db, id=id)

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
async def create_person(request: PersonSchema, response: Response, db: Session = Depends(get_db)):
    try:
        return controller.create(db=db, item = request, method = create_person_method)
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'detail': 'Bad request !'
        }

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
@router.put('/person', status_code=status.HTTP_200_OK)
async def update_person(request: PersonSchema, db: Session = Depends(get_db)):
    return controller.update(db, id=request.id, item=request, method = setter_person_method)

# Delete person api
@router.delete('/person/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int, response: Response, db: Session = Depends(get_db)):
    return controller.delete(db, id=id)

## -------------------------------------------------------


# Society APIs

# Create society api
@router.post('/society', status_code=status.HTTP_201_CREATED, response_model=SocietySchema)
async def create_society(request: SocietySchema, db: Session = Depends(get_db)):
    return society_controller.create(db=db, item=request, method=create_society_method)


@router.get('/society', status_code=status.HTTP_200_OK, response_model=List[SocietySchema])
async def get_societies(db: Session = Depends(get_db)):
    print('sdfsdfhjgsdjhkgfjhsgdfhj')
    return society_controller.get(db=db)


@router.get('/society{id}', status_code=status.HTTP_200_OK, response_model=SocietySchema)
async def get_society(id: int, db: Session = Depends(get_db)):
    return society_controller.retrieve(db=db, id=id)


@router.put('/society', status_code=status.HTTP_200_OK, response_model=SocietySchema)
async def update_society(request: SocietySchema, db: Session = Depends(get_db)):
    return society_controller.update(db=db, id=request.id, item=request, method=setter_society_method)


@router.delete('/society/{id}', status_code=status.HTTP_200_OK, response_model=SocietySchema)
async def delete_society(id: int, db: Session = Depends(get_db)):
    return society_controller.delete(db=db, id=id)
