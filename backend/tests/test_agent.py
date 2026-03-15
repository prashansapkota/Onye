"""Tests for GoogleADKReconciliationAgent — no real API calls made."""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.google_adk_agent import (
    GoogleADKReconciliationAgent,
    analyze_medication_sources,
    validate_patient_record,
)
from app.services.data_quality_service import DataQualityService
from app.services.reconciliation_service import ReconciliationService

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

MOCK_RECONCILE_RESPONSE = {
    "reconciled_medication": "Metformin 500mg twice daily",
    "confidence_score": 0.88,
    "reasoning": "Most recent clinical record from primary care.",
    "recommended_actions": ["Update Hospital EHR"],
    "clinical_safety_check": "PASSED",
}

MOCK_QUALITY_RESPONSE = {
    "overall_score": 62,
    "breakdown": {
        "completeness": 60,
        "accuracy": 50,
        "timeliness": 70,
        "clinical_plausibility": 40,
    },
    "issues_detected": [
        {
            "field": "vital_signs.blood_pressure",
            "issue": "Implausible value 340/180",
            "severity": "high",
        }
    ],
}


def _make_mock_runner(response_dict: dict) -> MagicMock:
    part = MagicMock()
    part.text = json.dumps(response_dict)

    event = MagicMock()
    event.is_final_response.return_value = True
    event.content.parts = [part]

    async def fake_run_async(**kwargs):
        yield event

    runner = MagicMock()
    runner.run_async = fake_run_async
    return runner


# ---------------------------------------------------------------------------
# Tool tests
# ---------------------------------------------------------------------------

def test_analyze_medication_sources_parses_inputs():
    sources = [{"system": "Hospital EHR", "medication": "Metformin 500mg", "source_reliability": "high"}]
    context = {"age": 67, "conditions": ["Type 2 Diabetes"], "recent_labs": {"eGFR": 45}}

    result = analyze_medication_sources(
        sources_json=json.dumps(sources),
        patient_context_json=json.dumps(context),
    )

    assert result["sources"] == sources
    assert result["patient_context"] == context


def test_validate_patient_record_parses_input():
    record = {
        "demographics": {"name": "John Doe", "dob": "1955-03-15", "gender": "M"},
        "medications": ["Metformin 500mg"],
        "allergies": [],
        "conditions": ["Type 2 Diabetes"],
        "vital_signs": {"blood_pressure": "340/180", "heart_rate": 72},
        "last_updated": "2024-06-15",
    }

    result = validate_patient_record(record_json=json.dumps(record))

    assert result["record"] == record


def test_analyze_medication_sources_raises_on_invalid_json():
    with pytest.raises(json.JSONDecodeError):
        analyze_medication_sources(sources_json="not-json", patient_context_json="{}")


# ---------------------------------------------------------------------------
# Agent tests
# ---------------------------------------------------------------------------

@patch("app.agents.google_adk_agent._build_agent", return_value=MagicMock())
@patch("app.agents.google_adk_agent.InMemoryRunner")
def test_run_async_returns_reconciliation_result(mock_runner_cls, _mock_build):
    mock_runner_cls.return_value = _make_mock_runner(MOCK_RECONCILE_RESPONSE)

    agent = GoogleADKReconciliationAgent()
    result = asyncio.run(agent.run_async({
        "patient_context": {"age": 67, "conditions": ["Type 2 Diabetes"], "recent_labs": {"eGFR": 45}},
        "sources": [{"system": "Primary Care", "medication": "Metformin 500mg twice daily", "source_reliability": "high"}],
    }))

    assert result["reconciled_medication"] == "Metformin 500mg twice daily"
    assert result["confidence_score"] == 0.88
    assert result["clinical_safety_check"] == "PASSED"


@patch("app.agents.google_adk_agent._build_agent", return_value=MagicMock())
@patch("app.agents.google_adk_agent.InMemoryRunner")
def test_run_async_returns_data_quality_result(mock_runner_cls, _mock_build):
    mock_runner_cls.return_value = _make_mock_runner(MOCK_QUALITY_RESPONSE)

    agent = GoogleADKReconciliationAgent()
    result = asyncio.run(agent.run_async({
        "demographics": {"name": "John Doe"},
        "vital_signs": {"blood_pressure": "340/180"},
    }))

    assert result["overall_score"] == 62
    assert result["breakdown"]["clinical_plausibility"] == 40
    assert any(i["severity"] == "high" for i in result["issues_detected"])


@patch("app.agents.google_adk_agent._build_agent", return_value=MagicMock())
@patch("app.agents.google_adk_agent.InMemoryRunner")
def test_verify_readiness_true_when_key_set(mock_runner_cls, _mock_build, monkeypatch):
    mock_runner_cls.return_value = MagicMock()
    monkeypatch.setattr("app.agents.google_adk_agent.settings.anthropic_api_key", "sk-test")

    assert GoogleADKReconciliationAgent().verify_readiness() is True


@patch("app.agents.google_adk_agent._build_agent", return_value=MagicMock())
@patch("app.agents.google_adk_agent.InMemoryRunner")
def test_verify_readiness_false_when_no_key(mock_runner_cls, _mock_build, monkeypatch):
    mock_runner_cls.return_value = MagicMock()
    monkeypatch.setattr("app.agents.google_adk_agent.settings.anthropic_api_key", "")

    assert GoogleADKReconciliationAgent().verify_readiness() is False


# ---------------------------------------------------------------------------
# Service tests
# ---------------------------------------------------------------------------

def test_reconciliation_service_calls_agent():
    mock_agent = MagicMock()
    mock_agent.run_async = AsyncMock(return_value=MOCK_RECONCILE_RESPONSE)

    result = asyncio.run(ReconciliationService(agent=mock_agent).reconcile_medication({"sources": []}))

    mock_agent.run_async.assert_awaited_once()
    assert result == MOCK_RECONCILE_RESPONSE


def test_data_quality_service_calls_agent():
    mock_agent = MagicMock()
    mock_agent.run_async = AsyncMock(return_value=MOCK_QUALITY_RESPONSE)

    result = asyncio.run(DataQualityService(agent=mock_agent).validate({"demographics": {}}))

    mock_agent.run_async.assert_awaited_once()
    assert result == MOCK_QUALITY_RESPONSE
