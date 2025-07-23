from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import structlog

from config import get_settings, setup_logging
from config.database import create_tables, engine
from controllers import warehouse_controller, cargo_controller, compatibility_controller
from admin import setup_admin

settings = get_settings()

app = FastAPI(
    title="Warehouse Service",
    description="Warehouse and cargo management service",
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

app.include_router(warehouse_controller.router)
app.include_router(cargo_controller.router)
app.include_router(compatibility_controller.router)

@app.on_event("startup")
def startup_event():
    logger.info("Warehouse service starting up")
    create_tables()
    setup_admin(app, engine)
    logger.info("Database tables created")
    logger.info("Admin panel setup complete")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Warehouse service shutting down")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "warehouse"}

@app.get("/admin-login")
async def admin_login_page():
    """Кастомная страница входа в админ-панель"""
    from pathlib import Path
    template_path = Path(__file__).parent / "templates" / "admin_login.html"
    with open(template_path, "r") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content) 