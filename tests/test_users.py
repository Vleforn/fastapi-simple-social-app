import pytest
from app import schemas
from jose import jwt
from app.config import settings

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
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong_email@gmail.com', '12345678', 403),
    ('test_user@gmail.com', 'wrong_password', 403),
    ('wrong_email@gmail.com', 'wrong_password', 403),
    (None, '12345678', 422),
    ('test_user@gmail.com', None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post('/login', data={'username': email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'


def test_get_users(client):
    pass

def test_delete_user(client):
    pass
