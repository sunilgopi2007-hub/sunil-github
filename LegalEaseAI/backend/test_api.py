from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_generate_route_returns_document():
    response = client.post(
        "/generate",
        json={
            "document_type": "Service Agreement",
            "parties": "Alpha Ltd. and Beta LLC",
            "terms": "Payment within 30 days; confidentiality; project completion by 15 November 2026",
            "effective_date": "1 October 2026",
            "jurisdiction": "New York, USA"
        }
    )
    assert response.status_code == 200
    payload = response.json()
    assert "document" in payload
    assert isinstance(payload["document"], str)
    assert len(payload["document"]) > 0
