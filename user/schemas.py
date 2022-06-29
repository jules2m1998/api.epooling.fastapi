from typing import Any, Optional
from pydantic import BaseModel, Field
from auth.utils import Account
from fastapi import UploadFile


class Tmp(BaseModel):
    id: int = Field(index=True)
    user_id: int = Field(None)

    class Config:
        orm_mode = True


class PersonSchema(Tmp):
    first_name: str = Field(None)
    last_name: str = Field(None)
    sex: int = Field(None)
    user_id: int = Field(default=None, foreign_key="user.id")

    class Config:
        orm_mode = True


class PersonInSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[int] = None


class SocietySchema(Tmp):
    name: str
    desc: str
    location: str
    user_id: int = Field(default=None, foreign_key="user.id")

    class Config:
        orm_mode = True


class SocietyInSchema(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    location: Optional[str] = None


class UserSimpleSchema(BaseModel):
    id: int
    phone: int
    phone_ex: str
    avatar_url: Optional[str]
    email: str
    account_id: int


class UserSchema(UserSimpleSchema):
    class Config:
        orm_mode = True

    account: Optional[Account]
    person: Optional[PersonSchema]
    society: Optional[SocietySchema]


class UserInSchema(BaseModel):
    phone: Optional[int] = None
    phone_ex: Optional[str] = None
    avatar: Optional[UploadFile] = None
    email: Optional[str] = None


class UserPersonSchema(BaseModel):
    first_name: str = Field(None)
    last_name: str = Field(None)
    sex: int = Field(None)
    phone: int = Field(None)
    phone_ex: str = Field(None)
    avatar_url: str = Field(None)
    email: str = Field(None)
    account_id: int = Field(default=None, foreign_key="account.id")

    class Config:
        orm_mode = True


class UserSocietySchema(BaseModel):
    desc: str
    location: str
    name: str
    phone: int
    phone_ex: str
    avatar_url: str
    email: str
    account_id: int

    class Config:
        orm_mode = False
