from fastapi import APIRouter
from .routes import router as routes_router
from .services.summary import summary_router as summary_router

api_router = APIRouter()
api_router.include_router(routes_router)
api_router.include_router(summary_router)