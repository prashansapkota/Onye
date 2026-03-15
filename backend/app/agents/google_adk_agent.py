import asyncio
import json
import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import InMemoryRunner
from google.genai import types

from app.core.config import settings


def analyze_medication_sources(
    sources_json: str,
    patient_context_json: str,
) -> dict:
    """Analyze conflicting medication records from multiple EHR sources.

    Args:
        sources_json: JSON array of source records. Each has: system,
            medication, source_reliability, last_updated, last_filled.
        patient_context_json: JSON object with patient age, conditions,
            and recent_labs (e.g. eGFR).

    Returns:
        Parsed sources and patient context for the agent to reason over.
        Produce a JSON response with: reconciled_medication, confidence_score
        (0.0-1.0), reasoning, recommended_actions, clinical_safety_check.
    """
    return {
        "sources": json.loads(sources_json),
        "patient_context": json.loads(patient_context_json),
    }


def validate_patient_record(record_json: str) -> dict:
    """Validate a patient EHR record for data quality issues.

    Args:
        record_json: JSON object with: demographics, medications, allergies,
            conditions, vital_signs, last_updated.

    Returns:
        Parsed record for the agent to score. Produce a JSON response with:
        overall_score (0-100), breakdown (completeness, accuracy, timeliness,
        clinical_plausibility), issues_detected (field, issue, severity).
    """
    return {"record": json.loads(record_json)}


def _build_agent() -> LlmAgent:
    os.environ.setdefault("ANTHROPIC_API_KEY", settings.anthropic_api_key)

    return LlmAgent(
        model=LiteLlm(model="anthropic/claude-opus-4-6"),
        name="ehr_reconciliation_agent",
        description=(
            "Clinical EHR agent that reconciles conflicting medication records "
            "and validates patient data quality."
        ),
        instruction=(
            "You are an expert clinical pharmacist and EHR data quality analyst. "
            "When reconciling medications, call analyze_medication_sources with "
            "the provided data and return ONLY a JSON object with keys: "
            "reconciled_medication, confidence_score, reasoning, "
            "recommended_actions, clinical_safety_check. "
            "When validating a patient record, call validate_patient_record and "
            "return ONLY a JSON object with keys: overall_score, breakdown, "
            "issues_detected. Never include markdown or prose in your response."
        ),
        tools=[analyze_medication_sources, validate_patient_record],
    )


class GoogleADKReconciliationAgent:
    def __init__(self) -> None:
        self._agent = _build_agent()
        self._runner = InMemoryRunner(agent=self._agent, app_name="onye-ehr")

    def verify_readiness(self) -> bool:
        return bool(settings.anthropic_api_key)

    def run(self, payload: dict) -> dict:
        return asyncio.run(self.run_async(payload))

    async def run_async(self, payload: dict) -> dict:
        final_text = ""
        async for event in self._runner.run_async(
            user_id="api",
            session_id=f"session-{id(payload)}",
            new_message=types.UserContent(parts=[types.Part(text=json.dumps(payload))]),
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text

        return json.loads(final_text)
