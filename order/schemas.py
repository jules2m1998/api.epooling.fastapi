from pydantic import BaseModel
from user.schemas import UserSchema
from typing import Optional
from announce.schemas import ItinerarySchema


class AnnounceSchema(BaseModel):
    id: int
    description: str
    image: str
    volume: int
    is_delivery: bool
    user_id: int
    user: Optional[UserSchema]
    itinerary: Optional[ItinerarySchema]

    class Config:
        orm_mode = True


class OrderSchema(BaseModel):
    id: int
    is_accepted: bool = False
    is_denied: bool = False
    is_delivered_agent: bool = False
    is_delivered_client: bool = False
    message: str = None

    user_id: int
    announce_id: int

    user: UserSchema
    announce: AnnounceSchema

    class Config:
        orm_mode = True


class OrderInSchema(BaseModel):
    user_id: int
    announce_id: int
    is_denied: bool = False
    message: str = None


class OrderUpdateSchema(BaseModel):
    id: int
    is_accepted: bool = False
    is_denied: bool = False
    is_delivered_agent: bool = False
    is_delivered_client: bool = False
