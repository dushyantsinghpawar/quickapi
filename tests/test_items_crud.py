from fastapi.testclient import TestClient

from app.main import app

c = TestClient(app)


def _get_token():
    # register once (ignore 400 if already exists), then login
    c.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "Aa1!thisisstrong"},
    )
    r = c.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "Aa1!thisisstrong"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_crud_flow():
    token = _get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # create
    r = c.post("/items", headers=headers, json={"name": "x", "description": "y"})
    assert r.status_code == 201, r.text
    item = r.json()

    # list contains it (public)
    r = c.get("/items")
    assert r.status_code == 200
    assert any(i["id"] == item["id"] for i in r.json())

    # update (protected)
    r = c.put(
        f"/items/{item['id']}",
        headers=headers,
        json={"name": "x2", "description": "y2"},
    )
    assert r.status_code == 200
    assert r.json()["name"] == "x2"

    # delete (protected)
    r = c.delete(f"/items/{item['id']}", headers=headers)
    assert r.status_code == 204
