from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from conf import ALGORITHM, SECRET_KEY
from auth.utils import Account
from auth.utils import decode_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, secret: str = SECRET_KEY, algorithm: str = ALGORITHM):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.secret = secret
        self.algorithm = algorithm

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")

            body: dict = await request.json()
            account: Account = Account(username=body['account']['username'])
            username = decode_token(credentials.credentials)
            if account.username != username:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = jwt.decode(token=jwtoken, key=self.secret, algorithms=self.algorithm)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
