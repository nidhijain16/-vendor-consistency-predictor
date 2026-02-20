"""
Tests for the Vendor Consistency Predictor API.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_prep_time_valid():
    """Test prediction with valid input data."""
    payload = {
        "vendor_id": 12345,
        "order_hour": 19,
        "day_of_week": 4,
        "item_count": 3,
        "is_peak_hour": True,
        "historical_delay_avg": 5.2
    }
    response = client.post("/predict/prep-time", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["vendor_id"] == 12345
    assert isinstance(data["predicted_prep_time"], float)
    assert "feature_importance_top" in data


def test_predict_prep_time_invalid_hour():
    """Test that invalid order_hour is rejected by validation."""
    payload = {
        "vendor_id": 12345,
        "order_hour": 25,  # Invalid: must be 0-23
        "day_of_week": 4,
        "item_count": 3,
        "is_peak_hour": True,
        "historical_delay_avg": 5.2
    }
    response = client.post("/predict/prep-time", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_prep_time_missing_field():
    """Test that missing required fields are rejected."""
    payload = {
        "vendor_id": 12345,
        "order_hour": 19,
        # Missing: day_of_week, item_count, is_peak_hour, historical_delay_avg
    }
    response = client.post("/predict/prep-time", json=payload)
    assert response.status_code == 422
