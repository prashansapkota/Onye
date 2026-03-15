# Claude Rules for Onye

## Project Context
FastAPI EHR backend for medication reconciliation + data quality validation. Google ADK integration is the core pending work.

## Efficiency Rules

### Reading Code
- Read only the files directly relevant to the task. Do NOT read all files speculatively.
- Key files by area:
  - Agent logic: `backend/app/agents/google_adk_agent.py`
  - Reconciliation: `backend/app/services/reconciliation_service.py`, `backend/app/schemas/reconcile.py`
  - Data quality: `backend/app/services/data_quality_service.py`, `backend/app/schemas/data_quality.py`
  - Routing: `backend/app/api/router.py`, `backend/app/api/v1/endpoints/`
  - Config: `backend/app/core/config.py`

### Making Changes
- Edit the minimal set of files needed. Do not refactor surrounding code unless asked.
- Do not add logging, error handling, or docstrings unless explicitly requested.
- Both reconciliation and data quality services return mock responses — replace only when asked to implement.

### Testing
- Tests live in `backend/tests/`. Only `test_health.py` exists currently.
- Run tests with: `cd backend && pytest`

### Google ADK
- Install with: `pip install -e ".[adk]"` from `backend/`
- API key goes in `.env` as `GOOGLE_API_KEY`

## What NOT to do
- Do not use the Explore agent for simple, targeted lookups — use Grep/Glob/Read directly.
- Do not create new files unless the task requires a new module (e.g., new endpoint, new schema).
- Do not speculatively implement features not requested.
