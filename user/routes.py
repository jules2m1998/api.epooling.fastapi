from fastapi import APIRouter, Depends, Response, status
from config import SessionLocal
from controllers import Controllers
from exception import NotFound404
from .schemas import PersonSchema
from .models import Person
from sqlalchemy.orm import Session
from .controller import UserController


router = APIRouter()
userController = UserController(cls=Person)
controller = Controllers(Person)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def setter_person(p: Person, subperson: PersonSchema):
    p.first_name = subperson.first_name
    p.last_name = subperson.last_name
    p.phone_ex = subperson.phone_ex
    p.phone = subperson.phone
    p.sex = subperson.sex

    return p



@router.post('/person', status_code=status.HTTP_201_CREATED)
async def create_person(request: PersonSchema, response: Response, db: Session = Depends(get_db)):
    try:
        return controller.create(db=db, item = request, method = setter_person)
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {}

@router.get('/person', status_code=status.HTTP_200_OK)
async def get_persons(db: Session = Depends(get_db)):
    return controller.get(db=db)

@router.get('/person/{id}', status_code=status.HTTP_200_OK)
async def get_person(id: int, response: Response, db: Session = Depends(get_db)):
    try:
        _item = controller.retrieve(db=db, id=id)
        return _item
    except NotFound404 as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}

@router.put('/person', status_code=status.HTTP_200_OK)
async def get_persons(request: PersonSchema, response: Response, db: Session = Depends(get_db)):
    try:
        return controller.update(db, id=request.id, item=request, method = setter_person)
    except NotFound404 as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}

@router.delete('/person/{id}', status_code=status.HTTP_200_OK)
async def get_persons(id: int, response: Response, db: Session = Depends(get_db)):
    try:
        return userController.delete(db, id=id)
    except NotFound404 as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {}
