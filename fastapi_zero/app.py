from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

# IMPORTACAO DO SCHEMAS DE SCHEMA.PY
from fastapi_zero.schemas import (
    Message,
    UserSchema,
    UserPublic,
    UserDB,
    UserList,
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


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1,
    )
    database.append(user_with_id)
    return user_with_id


@app.post(
    '/create_users', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def create_user(user: UserSchema):
    user_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_id)
    return user_id


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
