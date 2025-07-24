from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from config.settings import get_settings
from config.logging import setup_logging
from config.database import create_tables, engine
import structlog
from controllers.order_controller import router as order_router
from entities.database_models import Order as OrderModel
from shared.events.publisher import Publisher

settings = get_settings()
setup_logging(settings.log_level)

publisher = Publisher(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    username=settings.rabbitmq_user,
    password=settings.rabbitmq_password,
    exchange=settings.rabbitmq_exchange
)

logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.state.publisher = publisher

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router)

admin = Admin(app, engine)

class OrderAdmin(ModelView, model=OrderModel):
    name = "Order"
    name_plural = "Orders"
    icon = "fa-solid fa-box"
    column_list = [OrderModel.id, OrderModel.customer_name, OrderModel.status, OrderModel.created_at]
    column_searchable_list = [OrderModel.customer_name, OrderModel.customer_email]
    column_sortable_list = [OrderModel.id, OrderModel.status, OrderModel.created_at]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

admin.add_view(OrderAdmin)

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