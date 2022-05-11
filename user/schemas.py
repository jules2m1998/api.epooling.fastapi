from typing import Any
from pydantic import BaseModel, Field
from auth.utils import Account

class Tmp(BaseModel):
    id: int = Field(index=True)
    user_id: int = Field(None)

    class Config:
        orm_mode = True


class PersonSchema(Tmp):
    first_name: str = Field(None)
    last_name : str = Field(None)
    sex: int = Field(None)

    class Config:
        orm_mode = True

class SocietySchema(Tmp):
    desc: str
    location: str

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    class Config:
        orm_mode = True
    
    id: int
    phone: int
    phone_ex: str
    avatar_url: str
    email: str 
    account_id: int
    account: Account
    person: PersonSchema


class UserPersonSchema(BaseModel):
    first_name: str = Field(None)
    last_name : str = Field(None)
    sex: int = Field(None)
    phone: int = Field(None)
    phone_ex: str = Field(None)
    avatar_url: str = Field(None)
    email: str = Field(None)
    account_id: int = Field(default=None, foreign_key="account.id")

    class Config:
        orm_mode = True
