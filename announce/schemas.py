import datetime

from pydantic import BaseModel
from user.schemas import UserSchema
from typing import List, Optional


class CitySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CityInSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ItineraryCitySchema(BaseModel):
    id: int
    city: CitySchema
    itinerary_id: int
    price: int
    order: int

    class Config:
        orm_mode = True


class ItinerarySchema(BaseModel):
    id: int
    name: str
    announce_id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    itinerary_city: List[ItineraryCitySchema]

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    id: int
    is_accepted: bool = False
    is_delivered_agent: bool = False
    is_delivered_client: bool = False

    user_id: int
    announce_id: int

    user: UserSchema

    class Config:
        orm_mode = True


class AnnounceSchema(BaseModel):
    id: int
    description: str
    image: str
    volume: int
    is_delivery: bool
    user_id: int
    user: Optional[UserSchema]
    itinerary: Optional[ItinerarySchema]
    orders: Optional[List[OrderSchema]]

    class Config:
        orm_mode = True


class AnnounceSimpleSchema(BaseModel):
    description: str
    image: str
    volume: int
    is_delivery: bool
    user_id: int
    itinerary: ItinerarySchema

    class Config:
        orm_mode = True


class ItineraryInCitySchema(BaseModel):
    itinerary_id: int
    city_id: int
    price: int
    order: int

    class Config:
        orm_mode = True


class ItineraryInSchema(BaseModel):
    name: str
    announce_id: int
    start_date: str
    end_date: str
    cities: List[ItineraryInCitySchema]


class AnnounceInSchema(BaseModel):
    description: str
    image: str
    volume: int
    user_id: int
    is_delivery: bool = False

    class Config:
        orm_mode = True


class AnnounceUpdateSchema(BaseModel):
    id: int
    description: str
    image: str
    volume: int
    user_id: int
    is_delivery: bool = False

    class Config:
        orm_mode = True
