"""Tests for X-API-Key authentication on protected endpoints."""
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_data_quality_service, get_reconciliation_service
from app.main import app
from app.services.data_quality_service import DataQualityService
from app.services.reconciliation_service import ReconciliationService

client = TestClient(app)

VALID_KEY = "dev-key"
INVALID_KEY = "wrong-key"

RECONCILE_URL = "/api/reconcile/medication"
DATA_QUALITY_URL = "/api/validate/data-quality"

RECONCILE_PAYLOAD = {
    "patient_context": {"age": 67, "conditions": ["Type 2 Diabetes"], "recent_labs": {"eGFR": 45}},
    "sources": [{"system": "Primary Care", "medication": "Metformin 500mg", "source_reliability": "high"}],
}

DATA_QUALITY_PAYLOAD = {
    "demographics": {"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
    "medications": ["Metformin 500mg"],
    "allergies": [],
    "conditions": ["Type 2 Diabetes"],
    "vital_signs": {"blood_pressure": "120/80", "heart_rate": 72},
    "last_updated": "2024-06-15",
}


@pytest.mark.parametrize("url,payload", [
    (RECONCILE_URL, RECONCILE_PAYLOAD),
    (DATA_QUALITY_URL, DATA_QUALITY_PAYLOAD),
])
def test_missing_api_key_returns_422(url, payload):
    response = client.post(url, json=payload)
    assert response.status_code == 422  # Header(...) missing → FastAPI validation error


@pytest.mark.parametrize("url,payload", [
    (RECONCILE_URL, RECONCILE_PAYLOAD),
    (DATA_QUALITY_URL, DATA_QUALITY_PAYLOAD),
])
def test_invalid_api_key_returns_401(url, payload):
    response = client.post(url, json=payload, headers={"X-API-Key": INVALID_KEY})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


@pytest.mark.parametrize("url,payload,mock_response", [
    (
        RECONCILE_URL,
        RECONCILE_PAYLOAD,
        {
            "reconciled_medication": "Metformin 500mg twice daily",
            "confidence_score": 0.88,
            "reasoning": "Primary care record is most recent.",
            "recommended_actions": ["Update Hospital EHR"],
            "clinical_safety_check": "PASSED",
        },
    ),
    (
        DATA_QUALITY_URL,
        DATA_QUALITY_PAYLOAD,
        {
            "overall_score": 85,
            "breakdown": {"completeness": 90, "accuracy": 85, "timeliness": 80, "clinical_plausibility": 85},
            "issues_detected": [],
        },
    ),
])
def test_valid_api_key_passes_auth(url, payload, mock_response):
    mock_agent = MagicMock()
    mock_agent.run_async = AsyncMock(return_value=mock_response)

    app.dependency_overrides[get_reconciliation_service] = lambda: ReconciliationService(agent=mock_agent)
    app.dependency_overrides[get_data_quality_service] = lambda: DataQualityService(agent=mock_agent)

    try:
        response = client.post(url, json=payload, headers={"X-API-Key": VALID_KEY})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
