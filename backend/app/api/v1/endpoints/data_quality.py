from fastapi import APIRouter, Depends

from app.api.deps import get_data_quality_service, verify_api_key
from app.schemas.data_quality import DataQualityRequest, DataQualityResponse
from app.services.data_quality_service import DataQualityService

router = APIRouter()


@router.post("/data-quality", response_model=DataQualityResponse, dependencies=[Depends(verify_api_key)])
async def validate_data_quality(
    request: DataQualityRequest,
    service: DataQualityService = Depends(get_data_quality_service),
) -> DataQualityResponse:
    result = await service.validate(request.model_dump())
    return DataQualityResponse(**result)
