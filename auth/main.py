from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from config import get_settings, setup_logging

settings = get_settings()

app = FastAPI(
    title="Auth Service",
    description="Authentication and authorization service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging(settings.log_level)
logger = structlog.get_logger()

@app.on_event("startup")
async def startup_event():
    logger.info("Auth service starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Auth service shutting down")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth"} 