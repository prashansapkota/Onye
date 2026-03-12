from app.core.config import settings


class GoogleADKReconciliationAgent:
    """
    Thin adapter placeholder for Google ADK integration.
    This remains intentionally minimal for the initial scaffolding step.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.google_api_key

    def verify_readiness(self) -> bool:
        return bool(self.api_key)

    def run(self, payload: dict) -> dict:
        return {
            "message": "Google ADK agent scaffold is ready.",
            "implementation_status": "pending",
            "received_keys": sorted(payload.keys()),
        }
