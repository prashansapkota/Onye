from fastapi import APIRouter, Depends

from app.api.deps import get_reconciliation_service, verify_api_key
from app.schemas.reconcile import ReconcileMedicationRequest, ReconcileMedicationResponse
from app.services.reconciliation_service import ReconciliationService

router = APIRouter()


@router.post("/medication", response_model=ReconcileMedicationResponse, dependencies=[Depends(verify_api_key)])
async def reconcile_medication(
    request: ReconcileMedicationRequest,
    service: ReconciliationService = Depends(get_reconciliation_service),
) -> ReconcileMedicationResponse:
    result = await service.reconcile_medication(request.model_dump())
    return ReconcileMedicationResponse(**result)
