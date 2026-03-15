from app.agents.google_adk_agent import GoogleADKReconciliationAgent


class ReconciliationService:
    def __init__(self, agent: GoogleADKReconciliationAgent) -> None:
        self.agent = agent

    async def reconcile_medication(self, payload: dict) -> dict:
        return await self.agent.run_async(payload)
