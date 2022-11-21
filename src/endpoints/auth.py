from fastapi import APIRouter, Depends, HTTPException
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = 'C$N7[L*-VqAWp)dCet[AR]#}kgsZDIjmx;3_[l15(d*A@b*+?-}/C(g`cMf>8Uu['
TOKEN_EXP_DAYS = 0
TOKEN_EXP_MINUTES = 1
TOKEN_EXP_SECONDS = 0


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = SECRET_KEY

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(secret=password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(secret=plain_password, hash=hashed_password)

    def encode_token(self, user_id: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=TOKEN_EXP_DAYS, minutes=TOKEN_EXP_MINUTES, seconds=TOKEN_EXP_SECONDS),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(jwt=token, key=self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)) -> str:
        return self.decode_token(auth.credentials)


class AuthDetails(BaseModel):
    username: str
    password: str


router = APIRouter(
    prefix="/auth",
    tags=["Zadanie 3"]
)


auth_handler = AuthHandler()
users = []
usersHardCoded = \
    [
        {
            'username': 'Kamil',
            'password': auth_handler.get_password_hash('Dupa8')
        }
    ]


@router.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in usersHardCoded:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'Current time': datetime.now().replace(microsecond=0).isoformat()}


@router.get('/protected2')
def protected2(auth_details: AuthDetails):
    user = None
    for x in usersHardCoded:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    Depends(auth_handler.auth_wrapper(token))
