import uvicorn
import logging
from fastapi import FastAPI
from src.api import api_router
from src.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chat Summarize",
    description="Сервис для суммаризации чатов",
    version="0.1.0"
)

app.include_router(api_router)

if __name__ == "__main__":
    logger.info(f"Starting Chat Summarize with {settings.llm.model_name} model")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3000,
        log_level="info"
    )