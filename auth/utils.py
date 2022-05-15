from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from jose.jwt import JWTError
from fastapi.security import OAuth2PasswordBearer
from exception import credentials_exception
from auth.models import Account as AccountModel
from controllers import Controllers
from sqlalchemy.orm import Session
from conf import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
controller = Controllers(AccountModel)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Account(BaseModel):
    username: str
    id: Optional[int] = None

    class Config:
        orm_mode = True


class AccountInDB(Account):
    hashed_password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = "",
                        algorithm: str = ""):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_current_user(token: str, db: Session):
    try:
        username: str = decode_token(token)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = controller.retrieve_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def decode_token(token: str, secret=SECRET_KEY, algorithm=ALGORITHM):
    payload = jwt.decode(token=token, key=secret, algorithms=algorithm)
    return payload.get("sub")
