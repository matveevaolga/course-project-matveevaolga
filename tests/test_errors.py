from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_item():
    r = client.get("/features/999")
    assert r.status_code == 404
    body = r.json()
    assert "error" in body and body["error"]["code"] == "not_found"


def test_validation_error():
    r = client.post("/features/", json={"title": "", "desc": "Test"})
    assert r.status_code == 422
