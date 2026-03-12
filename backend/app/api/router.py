from fastapi import APIRouter

from app.api.v1.endpoints import data_quality, health, reconcile

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(reconcile.router, prefix="/reconcile", tags=["reconcile"])
api_router.include_router(
    data_quality.router, prefix="/validate", tags=["data-quality"]
)
