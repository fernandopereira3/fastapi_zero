from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

TOKEN_EXPIRE = 30
SECRET_KEY = 'PROVISORIO'
ALGORITHM = 'SHA256'

context = PasswordHash.recommended()


def get_password(password: str):
    return context.hash(password)

def set_password(plain_password: str, hashed_password: str):
    return context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    to_encode.update({'exp': datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(minutes=TOKEN_EXPIRE)})
    encodado_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encodado_jwt


