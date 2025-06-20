from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_zero.models import User
from fastapi_zero.database import get_session
from fastapi_zero.security import (
    get_password,
    send_password,
    create_access_token,
    get_current_user,
)
from fastapi.security import OAuth2PasswordRequestForm
from jwt import encode, decode

# IMPORTACAO DO SCHEMAS DE SCHEMA.PY
from fastapi_zero.schemas import (
    Message,
    UserSchema,
    UserPublic,
    UserList,
    Token,
)

app = FastAPI()
database = []


# ROTA INICIAL
@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Hello World!'}


# CRIAR USUARIOS
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


# PEGAR TODOS USUARIOS
@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def get_users( session: Session = Depends(get_session)):
    limit: int = 10
    offset: int = 0
    users = session.scalars(select(User).limit(limit).offset(offset))
    if not users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No users found',
        )
    return {'users': users}


# ATUALIZAR USUARIOS
@app.put(
    '/update_user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Voce nao tem permissao para atualizar este usuario',
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = user.password
        current_user.commit()
        current_user.refresh(current_user)

    except:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Erro ao atualizar usuario',
        )

    return current_user

# SELECIONA UM USUARIO PELO ID
@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def get_single_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    return db_user


# DELETA USUARIOS
@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def delete_user(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user),):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Voce nao tem permissao para deletar este usuario',
        )
    else:
        session.delete(current_user)
        session.commit()
        return {'message': 'Usuario deletado com sucesso'}

    return delete_user


# CRIACAO DE TOKENS
@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
