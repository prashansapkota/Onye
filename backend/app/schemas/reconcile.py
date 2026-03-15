from typing import Any
from pydantic import BaseModel


class MedicationSource(BaseModel):
    system: str
    medication: str
    source_reliability: str  # "high" | "medium" | "low"
    last_updated: str | None = None
    last_filled: str | None = None


class PatientContext(BaseModel):
    age: int | None = None
    conditions: list[str] = []
    recent_labs: dict[str, Any] = {}


class ReconcileMedicationRequest(BaseModel):
    patient_context: PatientContext
    sources: list[MedicationSource]


class ReconcileMedicationResponse(BaseModel):
    reconciled_medication: str
    confidence_score: float
    reasoning: str
    recommended_actions: list[str]
    clinical_safety_check: str
