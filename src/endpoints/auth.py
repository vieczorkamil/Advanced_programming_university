from fastapi import APIRouter, Depends, HTTPException
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

SECRET_KEY = 'SECRET'  # TODO:


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
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
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


@router.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append(
        {
            'username': auth_details.username,
            'password': hashed_password
        }
    )
    return


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


@router.get('/unprotected')
def unprotected():
    """
    Helper function to check list of registered users

    Parameters: 
        None
    Returns: 
        None
    """
    for x in usersHardCoded:
        print(x)
    return {'hello': usersHardCoded}
    # return {'hello': 'world'}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    print(username)  # DEBUG:
    return {'Current time': datetime.now().replace(microsecond=0).isoformat()}
