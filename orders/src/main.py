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
from shared.events.subscriber import Subscriber
from use_cases.order_event_service import OrderEventService
from repositories.order_repository import OrderRepository
from sqlalchemy.orm import sessionmaker
from utils.admin_auth import get_admin_auth

settings = get_settings()
setup_logging(settings.log_level)

publisher = Publisher(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    username=settings.rabbitmq_user,
    password=settings.rabbitmq_password,
    exchange=settings.rabbitmq_exchange
)

subscriber = Subscriber(
    host=settings.rabbitmq_host,
    port=settings.rabbitmq_port,
    username=settings.rabbitmq_user,
    password=settings.rabbitmq_password,
    exchange=settings.rabbitmq_exchange,
    queue="orders_queue",
    routing_keys=["vehicle_assigned", "no_vehicle_available"]
)

# Create database session and repository
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()
order_repository = OrderRepository(db_session)

order_event_service = OrderEventService(publisher, subscriber, order_repository)

logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.state.publisher = publisher
app.state.subscriber = subscriber
app.state.order_event_service = order_event_service
app.state.order_repository = order_repository

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_router)

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

    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"

def setup_admin(app, engine):
    """Setup admin panel with authentication"""
    admin = Admin(app, engine, authentication_backend=get_admin_auth())
    admin.add_view(OrderAdmin)
    return admin

@app.on_event("startup")
def startup_event():
    logger.info("Orders service starting up")
    create_tables()
    setup_admin(app, engine)
    
    # Start event service
    try:
        order_event_service.start_listening()
        logger.info("Event service started successfully")
    except Exception as e:
        logger.error("Failed to start event service", error=str(e))
    
    logger.info("Database tables created")
    logger.info("Admin panel setup complete")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Orders Service")
    try:
        subscriber.disconnect()
        publisher.disconnect()
        db_session.close()
        logger.info("Event service disconnected")
    except Exception as e:
        logger.error("Error disconnecting event service", error=str(e))


@app.get("/")
async def root():
    return {"message": "Orders Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orders"} 