from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_zero.schemas import UserSchema

from fastapi_zero.schemas import message

app = FastAPI()


@app.get('/', 
        status_code=HTTPStatus.OK,
        response_model=message,
        )
def read_root():
    return {'message': 'Hello World!'}

@app.post('/users',  status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    return user

@app.get('/html', response_class=HTMLResponse)
def exercicio_aula_02():
    return """
    <html>
      <head>
        <title>Hello World!</title>
      </head>
      <body>
        <h1> Hello World! </h1>
      </body>
    </html>"""

@app.get('/exercicio2', response_class=HTMLResponse)
def exercicio2():
    return """<h1>ESTOU VIVO</h1>"""

@app.get("/duno")
async def redirect_typer():
    return RedirectResponse("https://fastapidozero.dunossauro.com/estavel/02/")