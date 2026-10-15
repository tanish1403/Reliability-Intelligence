from fastapi.testclient import TestClient

from reliability_agent.main import app

client = TestClient(app)


def test_health_endpoint_returns_expected_payload() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "reliability-data-analysis-agent",
        "version": "0.1.0",
    }


def test_root_points_to_docs() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"



def test_analytics_demo_endpoint() -> None:
    response = client.get("/analytics/demo")
    assert response.status_code == 200
    data = response.json()
    assert data["sample_size"] == 8
    assert "mean_ttf_hours" in data
    assert "weibull_shape_beta" in data
    assert "weibull_scale_eta" in data

