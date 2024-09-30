from .database import client, session

def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json()["message"] == "Hello, Sailor"
    assert res.status_code == 200

