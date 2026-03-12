from pydantic import BaseModel, Field


class ReconcileMedicationRequest(BaseModel):
    payload: dict = Field(default_factory=dict)


class ReconcileMedicationResponse(BaseModel):
    message: str
    implementation_status: str = "pending"
