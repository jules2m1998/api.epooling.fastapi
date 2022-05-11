from turtle import st
from pydantic import BaseModel, Field

class Tmp(BaseModel):
    id: int = Field(None)
    user_id: int = Field(None)


class PersonSchema(Tmp):
    first_name: str = Field(None)
    last_name : str = Field(None)
    sex: int = Field(None)

class SocietySchema(Tmp):
    desc: str
    location: str

class UserSchema(BaseModel):
    id: int = Field(None)
    phone: int = Field(None)
    phone_ex: str = Field(None)
    avatar_url: str = Field(None)
    email: str = Field(None)