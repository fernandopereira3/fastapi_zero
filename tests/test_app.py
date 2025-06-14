from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi_zero.app import app, database


def test_root(client):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/create_users',
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


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Ailton',
            'email': 'ailton@fastapi.com.br',
            'password': '123456',
        },
    )

    if response.status_code == HTTPStatus.NOT_FOUND:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            'username': 'Ailton',
            'email': 'ailton@fastapi.com.br',
            'password': '123456',
            'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não existe'
        )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'jose',
        'email': 'jose@fastapi.com.br',
        'password': '123456',
        'id': 1,
    }