from http import HTTPStatus
from fastapi.testclient import TestClient
from fastapi_zero.app import app


def test_root(client):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_html(client):
    response = client.get('/exercicio2')
    assert response.text == '<h1>ESTOU VIVO</h1>'
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
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

def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'jose',
            'email': 'jose@fastapi.com.br',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'jose',
        'email': 'jose@fastapi.com.br',
        'password': '123456',
        'id': 1,
    }

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'jose',
                'email': 'jose@fastapi.com.br',
                'password': '123456',
                'id': 1,
            }
        ]
    }

def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'jose',
        'email': 'jose@fastapi.com.br',
        'password': '123456',
        'id': 1,
    }

def test_duno(client):
    response = client.get('/duno')
    assert response.url == 'https://fastapidozero.dunossauro.com/estavel/02/'


