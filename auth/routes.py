from fastapi import APIRouter, status, Depends
from controllers import Controllers
from fastapi.security import OAuth2PasswordRequestForm
from auth.models import Account
from auth.utils import get_password_hash, verify_password, create_access_token, Token, Account as AccountSchema, \
    oauth2_scheme, get_current_user
from config import SessionLocal
from sqlalchemy.orm import Session
from datetime import timedelta
from exception import credentials_exception
from conf import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM


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
        username=p.username,
        hashed_password=get_password_hash(p.password)
    )
    return _p


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=AccountSchema)
async def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    _u = controllers.create(db=db, item=form_data, method=create_account)
    return {
        'username': _u.username,
        'id': _u.id
    }


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    _account: Account = controllers.retrieve_username(db, form_data.username)
    if verify_password(form_data.password, _account.hashed_password):
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": _account.username},
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise credentials_exception


@router.get("/me", status_code=status.HTTP_200_OK, response_model=AccountSchema)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return await get_current_user(token, db=db)
