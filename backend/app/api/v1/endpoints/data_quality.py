from fastapi import APIRouter

from app.schemas.data_quality import DataQualityRequest, DataQualityResponse
from app.services.data_quality_service import DataQualityService

router = APIRouter()


@router.post("/data-quality", response_model=DataQualityResponse)
def validate_data_quality(request: DataQualityRequest) -> DataQualityResponse:
    service = DataQualityService()
    result = service.validate(request.payload)
    return DataQualityResponse(**result)
