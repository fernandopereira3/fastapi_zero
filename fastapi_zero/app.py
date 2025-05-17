from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

# IMPORTACAO DO SCHEMAS DE SCHEMA.PY
from fastapi_zero.schemas import Message, UserSchema, UserPublic, UserDB

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


@app.get('/exercicio2', response_class=HTMLResponse)
def exercicio2():
    return """<h1>ESTOU VIVO</h1>"""


@app.get('/duno')
async def redirect_typer():
    return RedirectResponse('https://fastapidozero.dunossauro.com/estavel/02/')
