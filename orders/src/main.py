from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from config.settings import get_settings
from config.logging import setup_logging
from config.database import create_tables, engine
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

# Setup admin panel with authentication
admin = Admin(app, engine)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Orders Service")
    create_tables()
    logger.info("Database tables created")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Orders Service")


@app.get("/")
async def root():
    return {"message": "Orders Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orders"} 