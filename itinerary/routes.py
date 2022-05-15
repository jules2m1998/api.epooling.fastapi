from fastapi import APIRouter, Depends, status
from itinerary.models import Itinerary
from announce.schemas import ItinerarySchema, ItineraryInSchema
from itinerary.controller import ItineraryController
from sqlalchemy.orm import Session
from typing import List
from utils import get_db


router = APIRouter()


@router.get("/", response_model=List[ItinerarySchema])
async def get_itineraries(
    db: Session = Depends(get_db)
):
    """
    Get all itineraries
    """
    return ItineraryController.get_all(db)


@router.get("/{id}", response_model=ItinerarySchema)
async def get_itinerary(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Get itinerary by id
    """
    return ItineraryController.get_by_id(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ItinerarySchema)
async def create_itinerary(
    itinerary: ItineraryInSchema,
    db: Session = Depends(get_db)
):
    """
    Create itinerary
    """
    return ItineraryController.create(db, itinerary)


@router.put("/{id}", response_model=ItinerarySchema)
async def update_itinerary(
    id: int,
    itinerary: ItinerarySchema,
    db: Session = Depends(get_db)
):
    """
    Update itinerary
    """
    return ItineraryController.update(db, id, itinerary)


@router.delete("/{id}", response_model=ItinerarySchema)
async def delete_itinerary(
    id: int,
    db: Session = Depends(get_db)
):
    """
    Delete itinerary
    """
    return ItineraryController.delete(db, id)
