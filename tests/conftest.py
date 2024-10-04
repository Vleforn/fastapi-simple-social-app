from app.config import settings
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient 
import pytest
from app.oauth2 import create_access_token
from app import models

engine = create_engine(settings.sqlalchemy_database_url + '_test')


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    # as far as I remember client is the fixture that deletes database and created whenever it passed to test_function
    user_data = {"email": "test_user@gmail.com", "password": "12345678"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "34d content",
        "user_id": test_user['id']
    }]
    posts = list(map(lambda a: models.Posts(**a), posts_data))
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Posts).all()
    return posts
