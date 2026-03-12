from pydantic import BaseModel, Field


class DataQualityRequest(BaseModel):
    payload: dict = Field(default_factory=dict)


class DataQualityResponse(BaseModel):
    message: str
    implementation_status: str = "pending"
