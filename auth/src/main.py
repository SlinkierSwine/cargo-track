from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from config import get_settings, setup_logging
from config.database import create_tables, engine
from controllers import auth_controller, user_controller
from admin import setup_admin

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

app.include_router(auth_controller.router)
app.include_router(user_controller.router)

@app.on_event("startup")
def startup_event():
    logger.info("Auth service starting up")
    create_tables()
    setup_admin(app, engine)
    logger.info("Database tables created")
    logger.info("Admin panel setup complete")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Auth service shutting down")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "auth"} 