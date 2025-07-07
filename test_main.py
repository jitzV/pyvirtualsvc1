import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def reset_service_data():
    # Reset the service data before each test
    client.post("/reset")

def test_get_hits_initial(reset_service_data):
    # Test the initial state of the /hits endpoint
    response = client.get("/hits")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["total_avg_response_time"] == "0.00 ms"
    for service in data["services"].values():
        assert service["hits"] == 0
        assert service["last_access_time"] == "N/A"
        assert service["avg_response_time"] == "0.00 ms"
        assert service["status"] == "Inactive"

def test_post_hits_and_get(reset_service_data):
    # Simulate a hit to a service with a valid JSON payload
    response = client.post("/stub/service1", json={"session": "test_session", "flag": True})
    assert response.status_code == 200

    # Check the /hits endpoint after the hit
    response = client.get("/hits")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["services"]["service1"]["hits"] == 1
    assert data["services"]["service1"]["last_access_time"] != "N/A"
    assert data["services"]["service1"]["avg_response_time"] != "0.00 ms"
    assert data["services"]["service1"]["status"] == "Active"

def test_reset_hits(reset_service_data):
    # Simulate a hit to a service with a valid JSON payload
    client.post("/stub/service1", json={"session": "test_session", "flag": True})

    # Reset the hit counters
    response = client.post("/reset")
    assert response.status_code == 200
    assert response.json() == {"message": "Hit counters reset successfully"}

    # Check the /hits endpoint after reset
    response = client.get("/hits")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    for service in data["services"].values():
        assert service["hits"] == 0
        assert service["last_access_time"] == "N/A"
        assert service["avg_response_time"] == "0.00 ms"
        assert service["status"] == "Inactive"