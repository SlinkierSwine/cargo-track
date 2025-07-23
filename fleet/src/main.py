from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from config.logging import setup_logging
import structlog

settings = get_settings()
setup_logging(settings.log_level)

logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Fleet service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Fleet service shutting down")


@app.get("/")
async def root():
    return {"message": "Fleet Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fleet"} 