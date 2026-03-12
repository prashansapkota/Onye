from app.agents.google_adk_agent import GoogleADKReconciliationAgent


class ReconciliationService:
    def __init__(self, agent: GoogleADKReconciliationAgent | None = None) -> None:
        self.agent = agent or GoogleADKReconciliationAgent()

    def reconcile_medication(self, payload: dict) -> dict:
        return self.agent.run(payload)
