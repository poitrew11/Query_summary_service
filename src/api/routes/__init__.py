from fastapi import APIRouter
from .health import health_router


router = APIRouter()
router.include_router(health_router)
