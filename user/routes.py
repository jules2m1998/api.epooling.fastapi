from typing import List, Union, Optional
from fastapi import APIRouter, Depends, status, UploadFile, Form, File, HTTPException
from controllers import Controllers
from user.controller import Controller as UserPersonController
from user.schemas import PersonSchema, SocietySchema, UserSchema, UserPersonSchema, UserSocietySchema, UserInSchema, \
    SocietyInSchema, PersonInSchema
from user.models import Person, Society, User
from sqlalchemy.orm import Session
from user.utils import create_person_method, create_society_method
from utils import get_db, get_update_value
from auth.auth_bearer import JWTBearer
from auth.utils import oauth2_scheme, accepted_file_extensions

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
        phone: Optional[int] = Form(None),
        email: Optional[str] = Form(None),
        avatar: Optional[UploadFile] = File(None),
        phone_ex: Optional[str] = Form(None),
        user_id: int = Form(...),
        db: Session = Depends(get_db)
):
    data = {
        'phone': phone,
        'email': email,
        'avatar': avatar,
        'phone_ex': phone_ex,
    }
    data_verify = get_update_value(data)
    user_update = UserInSchema()
    for key, value in data_verify.items():
        if value is not None:
            setattr(user_update, key, value)
    return UserPersonController.update_user(u=user_update, id=user_id, db=db)


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
async def create_user_person(first_name: str = Form(...),
                             last_name: str = Form(...),
                             sex: int = Form(...),
                             phone: int = Form(...),
                             phone_ex: str = Form(...),
                             avatar: Union[UploadFile, None] = File(None),
                             email: str = Form(...), account_id: int = Form(...), db: Session = Depends(get_db)):
    if avatar and avatar.filename.split('.')[-1].lower() not in accepted_file_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong file extension",
            headers={"X-Error": "Wrong file extension"}
        )

    request = UserPersonSchema(first_name=first_name, last_name=last_name, sex=sex, phone=phone, phone_ex=phone_ex,
                               avatar_url='', email=email, account_id=account_id)
    return UserPersonController.create_user_person(request, db, avatar=avatar)


@router.post('/user_society', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user_society(desc: str = Form(...), location: str = Form(...), name: str = Form(...),
                              phone: int = Form(...),
                              phone_ex: str = Form(...),
                              avatar: Union[UploadFile, None] = File(None),
                              email: str = Form(...), account_id: int = Form(...), db: Session = Depends(get_db)):
    if avatar is not None and avatar.filename.split('.')[-1].lower() not in accepted_file_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong file extension",
            headers={"X-Error": "Wrong file extension"}
        )
    request = UserSocietySchema(desc=desc, location=location, name=name, phone=phone, phone_ex=phone_ex,
                                avatar_url='', email=email, account_id=account_id)
    return UserPersonController.create_user_society(request, db, avatar=avatar)


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
    dependencies=[Depends(JWTBearer())],
    response_model=PersonSchema
)
async def update_person(
        user_id: Optional[int] = Form(...),
        id: Optional[int] = Form(...),
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        sex: Optional[int] = Form(None),
        db: Session = Depends(get_db)
):
    data = PersonInSchema(**get_update_value({
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'sex': sex
    }))
    return UserPersonController.update_user_person(id, data, db)


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
async def update_society(
        user_id: int = Form(...),
        id: int = Form(...),
        name: Optional[str] = Form(None),
        desc: Optional[str] = Form(None),
        location: Optional[str] = Form(None),
        db: Session = Depends(get_db)):
    data = {
        'id': id,
        'name': name,
        'desc': desc,
        'location': location
    }
    data_verify = SocietyInSchema(**get_update_value(data))
    return UserPersonController.update_user_society(id, data_verify, db)

# @router.delete('/society/{id}', status_code=status.HTTP_200_OK, response_model=SocietySchema)
# async def delete_society(id: int, db: Session = Depends(get_db)):
#     return society_controller.delete(db=db, id=id)
