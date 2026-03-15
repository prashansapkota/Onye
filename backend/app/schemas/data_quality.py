from typing import Any
from pydantic import BaseModel


class VitalSigns(BaseModel):
    blood_pressure: str | None = None
    heart_rate: int | None = None
    temperature: float | None = None
    respiratory_rate: int | None = None
    oxygen_saturation: float | None = None


class Demographics(BaseModel):
    name: str | None = None
    dob: str | None = None
    gender: str | None = None


class DataQualityRequest(BaseModel):
    demographics: Demographics
    medications: list[str] = []
    allergies: list[str] = []
    conditions: list[str] = []
    vital_signs: VitalSigns | None = None
    last_updated: str | None = None


class QualityIssue(BaseModel):
    field: str
    issue: str
    severity: str  # "high" | "medium" | "low"


class ScoreBreakdown(BaseModel):
    completeness: int
    accuracy: int
    timeliness: int
    clinical_plausibility: int


class DataQualityResponse(BaseModel):
    overall_score: int
    breakdown: ScoreBreakdown
    issues_detected: list[QualityIssue]
