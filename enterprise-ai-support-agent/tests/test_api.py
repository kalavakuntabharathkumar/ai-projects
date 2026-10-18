from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_triage_endpoint():
    response = client.post("/triage", json={"id":"T-3","subject":"Invoice refund","body":"Please refund this payment."})
    assert response.status_code == 200
    assert response.json()["ticket_id"] == "T-3"

def test_unknown_version():
    response = client.post("/triage?version=v9", json={"id":"T-4","subject":"Help","body":"I need help."})
    assert response.status_code == 400
