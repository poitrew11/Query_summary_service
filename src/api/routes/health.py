import logging

from fastapi import APIRouter
from src.schemas import HealthResponse


logger = logging.getLogger(__name__)
health_router = APIRouter(tags=["healthcheck"])


@health_router.get("/healthcheck",
                   response_model=HealthResponse)
async def healthcheck():
    """Check health status."""
    logger.debug('Health activated')
    return HealthResponse(result=True)
