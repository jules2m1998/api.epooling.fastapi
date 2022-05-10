from typing import List
from fastapi import APIRouter, Depends, Response, status
from config import SessionLocal
from controllers import Controllers
from .schemas import PersonSchema
from .models import Person
from sqlalchemy.orm import Session


router = APIRouter()
controller = Controllers[Person, PersonSchema](Person)

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
        return {
            'detail': 'Badd request !'
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
    return controller.update(db, id=request.id, item=request, method = setter_person)

@router.delete('/person/{id}', status_code=status.HTTP_200_OK)
async def get_persons(id: int, response: Response, db: Session = Depends(get_db)):
    return controller.delete(db, id=id)
