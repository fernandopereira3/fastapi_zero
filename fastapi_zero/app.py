from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
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
def create_user(user: UserSchema, session=Depends(get_session)):
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
def get_users(session: Session = Depends(get_session)):
    limit: int = 3
    offset: int = 0
    users = session.scalars(select(User).limit(limit).offset(offset))
    if not users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No users found',
        )
    return {'users': users}




@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    return db_user



@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )
    return database.pop(user_id - 1)
