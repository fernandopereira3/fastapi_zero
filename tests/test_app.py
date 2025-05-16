from http import HTTPStatus
from fastapi.testclient import TestClient
from fastapi_zero.app import app


def test_root():
    client = TestClient(app)

    response = client.get('/')
    assert response.json() == {'mensage': 'Hello Word!'}
    assert response.status_code == HTTPStatus.OK

def test_html():
    client = TestClient(app)

    response = client.get('/html')
    assert response.text == '<html>\n      <head>\n       <title>Hello World!</title>\n      </head>\n      <body>\n        <h1> Hello World! </h1>\n      </body>\n    </html>'
    assert response.status_code == HTTPStatus.OK
