from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from conf import ALGORITHM, SECRET_KEY
from auth.utils import Account
from user.models import User
from auth.utils import decode_token
from user.controller import Controller
from config import SessionLocal


class JWTBearer(HTTPBearer):
    def __init__(
            self,
            auto_error: bool = True,
            secret: str = SECRET_KEY,
            algorithm: str = ALGORITHM
    ):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.secret = secret
        self.algorithm = algorithm
        self.db = SessionLocal()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            username = decode_token(credentials.credentials)
            if request.method != 'DELETE':
                body = await request.json()
            else:
                body = {'user_id': request.path_params['user_id']}
            if body.get('account') is not None:
                account: Account = Account(username=body['account']['username'])
                if account.username != username:
                    raise HTTPException(status_code=403, detail="Invalid authorization code.")
                return credentials.credentials
            elif body['user_id'] is not None:
                try:
                    user_id: int = body['user_id']
                    user: User = Controller.get_by_username(db=self.db, username=username)
                    if user is not None:
                        if user.id != int(user_id):
                            raise HTTPException(status_code=403, detail="Invalid authorization code.")
                        return credentials.credentials
                    else:
                        raise HTTPException(status_code=403, detail="Invalid authorization code.")
                except Exception as ex:
                    raise HTTPException(status_code=403, detail="Invalid authorization code.")
        else:
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")

    def verify_jwt(self, jw_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = jwt.decode(token=jw_token, key=self.secret, algorithms=self.algorithm)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
