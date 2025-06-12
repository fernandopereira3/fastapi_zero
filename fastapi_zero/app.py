from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from fastapi_zero.models import User
from fastapi_zero.database import get_session

# IMPORTACAO DO SCHEMAS DE SCHEMA.PY
from fastapi_zero.schemas import (
    Message,
    UserSchema,
    UserPublic,
    UserList,
    UserDB
)

app = FastAPI()
database = []


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Hello World!'}


@app.post(
    '/create_users', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def create_user(user: UserSchema):
    session = get_session()

    # Verifica se o banco de dados já existe
    email_exists = session.scalar(select(User).where((User.email == user.email) | (User.username == user.username)))
    if email_exists:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou Nome já existe',
        )
    # Cria o usuário com um ID automático
    user_with_id = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(user_with_id)
    session.commit()
    session.refresh(user_with_id)
    return user_with_id



@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    if not database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No users found in database',
        )
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )
    database[user_id - 1] = UserDB(**user.model_dump(), id=user_id)
    return database[user_id - 1]


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )
    return database.pop(user_id - 1)


@app.get('/exercicio2', response_class=HTMLResponse)
def exercicio2():
    return """<h1>ESTOU VIVO</h1>"""


@app.get('/duno')
async def redirect_typer():
    return RedirectResponse('https://fastapidozero.dunossauro.com/estavel/02/')
