from fastapi import APIRouter, Depends, status
from announce.controller import AnnounceController, CityController
from announce.schemas import AnnounceSchema, CitySchema, AnnounceInSchema, CityInSchema, AnnounceUpdateSchema
from sqlalchemy.orm import Session
from typing import List
from utils import get_db
from auth.auth_bearer import JWTBearer


router = APIRouter()
cityRouter = APIRouter()


@router.get("/{id}", response_model=AnnounceSchema)
def get_announce(id: int, db: Session = Depends(get_db)):
    """
    Get the announce by id
    """
    return AnnounceController.get_by_id(db, id)


@router.get("/", response_model=List[AnnounceSchema])
def get_announces(db: Session = Depends(get_db)):
    """
    Get all announces
    """
    return AnnounceController.get_all(db)


@router.post("/", response_model=AnnounceSchema, status_code=status.HTTP_201_CREATED)
def create_announce(announce: AnnounceInSchema, db: Session = Depends(get_db)):
    """
    Create a new announce
    """
    return AnnounceController.create(db, announce)


@router.put(
    "/",
    response_model=AnnounceSchema,
    dependencies=[Depends(JWTBearer())]
)
def update_announce(announce: AnnounceUpdateSchema, db: Session = Depends(get_db)):
    """
    Update an announce
    """
    return AnnounceController.update(db, announce)


@router.delete(
    "/{id}/{user_id}",
    response_model=AnnounceSchema,
    dependencies=[Depends(JWTBearer())]
)
def delete_announce(id: int, user_id: str, db: Session = Depends(get_db)):
    """
    Delete an announce
    """
    return AnnounceController.delete(db, id)

###############################################################################


@cityRouter.get("/{id}", response_model=List[CitySchema])
def get_city(id: int, db: Session = Depends(get_db)):
    """
    Get all announces by city
    """
    return CityController.get_by_id(db, id)


@cityRouter.get("/", response_model=List[CitySchema])
def get_cities(db: Session = Depends(get_db)):
    """
    Get all announces by city
    """
    return CityController.get_all(db)


@cityRouter.post("/", response_model=CitySchema, status_code=status.HTTP_201_CREATED)
def create_city(city: CityInSchema, db: Session = Depends(get_db)):
    """
    Create a new city
    """
    print(city)
    return CityController.create(db, city)
