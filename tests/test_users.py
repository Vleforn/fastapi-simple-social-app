import pytest
from .database import client, session
from app import schemas
from jose import jwt
from app.config import settings

@pytest.fixture
def test_user(client):
    # as far as I remember client is the fixture that deletes database and created whenever it passed to test_function
    user_data = {"email": "test_user@gmail.com", "password": "12345678"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_create_user(client):
    res = client.post("/users/", json={"email": "new_user@gmail.com", "password": "12345678"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "new_user@gmail.com"
    assert res.status_code == 201

def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}") 
    user = schemas.UserOut(**res.json())
    assert user.email == test_user["email"]
    assert user.id == test_user["id"]
    assert res.status_code == 200

def test_login(client, test_user):
    res = client.post('/login', data={'username': test_user["email"], "password": test_user["password"]})
    token = schemas.Token(**res.json())
    assert token.token_type == 'bearer'
    assert jwt.decode(token.access_token, settings.secret_key, algorithms=settings.algorithm)['user_id'] == test_user['id']
    # print(jwt.decode(token.access_token, settings.secret_key, algorithms=settings.algorithm)['user_id'])
    # print(test_user['id'])
    assert res.status_code == 200


def test_get_users(client):
    pass

def test_delete_user(client):
    pass
