from http import HTTPStatus
from fastapi.testclient import TestClient
from fastapi_zero.app import app


def test_root():
    client = TestClient(app)

    response = client.get('/')
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_html():
    client = TestClient(app)

    response = client.get('/exercicio2')
    assert response.text == '<h1>ESTOU VIVO</h1>'
    assert response.status_code == HTTPStatus.OK


def test_create_user():
    client = TestClient(app)
    response = client.post(
        '/users',
        json={
            'username': 'jose',
            'email': 'jose@fastapi.com.br',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'jose',
        'email': 'jose@fastapi.com.br',
        'password': '123456',
        'id': 1,
    }
