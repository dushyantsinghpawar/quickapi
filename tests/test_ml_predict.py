from fastapi.testclient import TestClient

from app.main import app

c = TestClient(app)


def _get_token():
    # register once (ignore if already exists)
    c.post(
        "/auth/register", json={"email": "me@example.com", "password": "Sup3rSaf3!Pass"}
    )
    r = c.post(
        "/auth/login", data={"username": "me@example.com", "password": "Sup3rSaf3!Pass"}
    )
    return r.json()["access_token"]


def test_predict():
    token = _get_token()
    r = c.post(
        "/ml/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert "label" in body and "probabilities" in body
    assert isinstance(body["probabilities"], dict)
