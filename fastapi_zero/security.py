from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User

TOKEN_EXPIRE = 30
SECRET_KEY = 'PROVISORIO'
ALGORITHM = 'HS256'

context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password(password: str):
    return context.hash(password)


def send_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    to_encode.update({
        'exp': datetime.now(tz=ZoneInfo('UTC'))
        + timedelta(minutes=TOKEN_EXPIRE)
    })
    encodado_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodado_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Você precisa estar autenticado para acessar este recurso',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_username = payload.get('sub')

        if not subject_username:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.username == subject_username)
    )

    if not user:
        raise credentials_exception

    return user
