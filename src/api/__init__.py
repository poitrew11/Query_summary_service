from fastapi import APIRouter
from .routes.health import health_router
from .services.summary import summary_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(summary_router)