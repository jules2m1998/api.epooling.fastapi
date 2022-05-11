from dotenv import load_dotenv
from fastapi import APIRouter, status, Depends
from controllers import Controllers
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .models import Account
from .utils import get_password_hash, verify_password, create_access_token, Token, Account as AccountSchema
from config import SessionLocal
from sqlalchemy.orm import Session
from datetime import timedelta
from exception import credentials_exception
import os
from pathlib import Path
from os.path import join, dirname


dotenv_path = join(Path(__file__).parent.parent.absolute(), '.env')
load_dotenv(dotenv_path)
ACCESS_TOKEN_EXPIRE_MINUTES =  os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ['ALGORITHM']

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()
controllers = Controllers(Account)

def setter_account(_account: Account, account: OAuth2PasswordRequestForm):
    _account.username = account.username
    _account.hashed_password = get_password_hash(account.password)
    return _account

def create_account(p: OAuth2PasswordRequestForm):
    _p = Account(
        username = p.username,
        hashed_password = get_password_hash(p.password)
    )
    return _p


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=AccountSchema)
async def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return {
        'username': controllers.create(db=db, item = form_data, method=create_account).username,
        'id': controllers.create(db=db, item = form_data, method=create_account).id
    }


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    _account: Account = controllers.retrieveUsername(db, form_data.username)
    if verify_password(form_data.password, _account.hashed_password):
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": _account.username},
            secret_key= SECRET_KEY,
            algorithm= ALGORITHM,
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise credentials_exception
