from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_event():
    response = client.post("/api/event/")
    assert response.status_code == 200
    assert response.json() == {"result": "success"}