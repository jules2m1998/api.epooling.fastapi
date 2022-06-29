from fastapi import APIRouter, Depends, status
from announce.controller import AnnounceController, CityController
from announce.schemas import AnnounceSchema, CitySchema, \
    AnnounceInSchema, CityInSchema, AnnounceUpdateSchema, AnnounceItineraryInSchema, AnnounceItineraryInOptionalSchema, AnnounceOutSchema
from sqlalchemy.orm import Session
from typing import List, Optional
from utils import get_db
from auth.auth_bearer import JWTBearer


router = APIRouter()
cityRouter = APIRouter()


@router.get("/{id}", response_model=AnnounceOutSchema)
def get_announce(id: int, db: Session = Depends(get_db)):
    """
    Get the announce by id
    """
    return AnnounceController.get_by_id(db, id)


@router.get("/user/{user_id}", response_model=List[AnnounceSchema])
def get_announce_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get the announce by id
    """
    return AnnounceController.get_all_by_user_id(db, user_id)


@router.get("/", response_model=List[AnnounceSchema])
def get_announces(
        start: Optional[int] = None,
        end: Optional[int] = None,
        db: Session = Depends(get_db)
):
    """
    Get all announces
    """
    return AnnounceController.get_all(db, start, end)


@router.post("/", response_model=AnnounceSchema, status_code=status.HTTP_201_CREATED)
def create_announce(announce: AnnounceInSchema, db: Session = Depends(get_db)):
    """
    Create a new announce
    """
    return AnnounceController.create(db, announce)


@router.post("/itinerary", response_model=AnnounceSchema, status_code=status.HTTP_201_CREATED)
def create_announce_itinerary(announce: AnnounceItineraryInSchema, db: Session = Depends(get_db)):
    """
    Create a new announce with itinerary
    """
    return AnnounceController.create_with_itinerary(db, announce)


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


@router.put(
    "/itinerary/{announce_id}",
    response_model=AnnounceSchema,
    dependencies=[Depends(JWTBearer())]
)
def update_announce_with_itinerary(announce_id: int, announce: AnnounceItineraryInOptionalSchema, db: Session = Depends(get_db)):
    """
    Update an announce and itinerary
    """
    return AnnounceController.update_with_itinerary(db, announce, announce_id)


@router.delete(
    "/{id}/{user_id}",
    response_model=AnnounceSchema,
    dependencies=[Depends(JWTBearer())]
)
def delete_announce(id: int, user_id: str, db: Session = Depends(get_db)):
    """
    Delete an announce
    """
    print(user_id)
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
