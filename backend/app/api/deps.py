from functools import lru_cache

from app.agents.google_adk_agent import GoogleADKReconciliationAgent
from app.services.data_quality_service import DataQualityService
from app.services.reconciliation_service import ReconciliationService


@lru_cache(maxsize=1)
def get_agent() -> GoogleADKReconciliationAgent:
    return GoogleADKReconciliationAgent()


def get_reconciliation_service() -> ReconciliationService:
    return ReconciliationService(agent=get_agent())


def get_data_quality_service() -> DataQualityService:
    return DataQualityService(agent=get_agent())
