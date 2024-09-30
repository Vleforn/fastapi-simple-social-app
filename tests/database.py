from app.config import settings
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient 
import pytest


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

def test_root(client):
    res = client.get("/")
    res.json().get('message') == "Hello, Sailor"
