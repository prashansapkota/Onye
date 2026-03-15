from functools import lru_cache

from fastapi import Header, HTTPException, status

from app.agents.google_adk_agent import GoogleADKReconciliationAgent
from app.core.config import settings
from app.services.data_quality_service import DataQualityService
from app.services.reconciliation_service import ReconciliationService


def verify_api_key(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")


@lru_cache(maxsize=1)
def get_agent() -> GoogleADKReconciliationAgent:
    return GoogleADKReconciliationAgent()


def get_reconciliation_service() -> ReconciliationService:
    return ReconciliationService(agent=get_agent())


def get_data_quality_service() -> DataQualityService:
    return DataQualityService(agent=get_agent())
