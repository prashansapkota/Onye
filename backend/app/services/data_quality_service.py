from app.agents.google_adk_agent import GoogleADKReconciliationAgent


class DataQualityService:
    def __init__(self, agent: GoogleADKReconciliationAgent) -> None:
        self.agent = agent

    async def validate(self, payload: dict) -> dict:
        return await self.agent.run_async(payload)
