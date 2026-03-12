# Onye EHR Backend (Initial Scaffold)

This is the initial backend scaffold for the take-home:

- FastAPI app
- Required route paths:
  - `POST /api/reconcile/medication`
  - `POST /api/validate/data-quality`
- Google ADK adapter placeholder
- Basic health endpoint
- Docker + docker-compose setup

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Install ADK extras when you start the agent implementation:

```bash
pip install -e ".[adk]"
```

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

## Verify

```bash
pytest
```
