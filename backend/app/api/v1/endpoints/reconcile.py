from fastapi import APIRouter

from app.schemas.reconcile import (
    ReconcileMedicationRequest,
    ReconcileMedicationResponse,
)
from app.services.reconciliation_service import ReconciliationService

router = APIRouter()


@router.post("/medication", response_model=ReconcileMedicationResponse)
def reconcile_medication(
    request: ReconcileMedicationRequest,
) -> ReconcileMedicationResponse:
    service = ReconciliationService()
    result = service.reconcile_medication(request.payload)
    return ReconcileMedicationResponse(**result)
