from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi_zero.app import app, database
from fastapi_zero.schemas import UserPublic


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


def test_get_users(client, user):
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


def test_get_users_com_users(client, user):
    response = client.get('/users')
    user_public = UserPublic.model_validate(user).model_dump()
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_public]
    }


def test_update_user(client):
    # Primeiro cria o usuário
    create_response = client.post('/create_users', json={
        'username': 'jose',
        'email': 'jose@fastapi.com.br', 
        'password': '123456',
    })
    assert create_response.status_code == HTTPStatus.CREATED
    # Tenta atualizar
    response = client.put('/update_user/1', json={
        'username': 'Ailton',
        'email': 'ailton@fastapi.com.br',
        'password': '123456',
    })
    assert response.json() == {
        'username': 'Ailton',
        'email': 'ailton@fastapi.com.br',
        'password': '123456',
        'id': 1
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    
 