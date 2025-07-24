from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from config.settings import get_settings
from config.logging import setup_logging
from config.database import create_tables, engine
from controllers.vehicle_controller import router as vehicle_router
from controllers.driver_controller import router as driver_router
from controllers.route_assignment_controller import router as route_assignment_router
from entities.database_models import Vehicle, Driver, RouteAssignment
from shared.events.publisher import Publisher
from shared.events.subscriber import Subscriber
from use_cases.fleet_event_service import FleetEventService
from repositories.driver_repository import DriverRepository
from repositories.vehicle_repository import VehicleRepository
from utils.admin_auth import get_admin_auth
import structlog

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
    queue="fleet_queue",
    routing_keys=["order_created"]
)

logger = structlog.get_logger()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.state.publisher = publisher
app.state.subscriber = subscriber

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(route_assignment_router)

# Setup admin panel with authentication
admin = Admin(app, engine, authentication_backend=get_admin_auth())

# Register admin views
class VehicleAdmin(ModelView, model=Vehicle):
    name = "Vehicle"
    name_plural = "Vehicles"
    icon = "fa-solid fa-truck"
    column_list = [Vehicle.id, Vehicle.license_plate, Vehicle.brand, Vehicle.model, Vehicle.status]
    column_searchable_list = [Vehicle.license_plate, Vehicle.brand, Vehicle.model]
    column_sortable_list = [Vehicle.id, Vehicle.license_plate, Vehicle.brand, Vehicle.model, Vehicle.status]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


class DriverAdmin(ModelView, model=Driver):
    name = "Driver"
    name_plural = "Drivers"
    icon = "fa-solid fa-user"
    column_list = [Driver.id, Driver.first_name, Driver.last_name, Driver.email, Driver.license_number, Driver.status]
    column_searchable_list = [Driver.first_name, Driver.last_name, Driver.email, Driver.license_number]
    column_sortable_list = [Driver.id, Driver.first_name, Driver.last_name, Driver.email, Driver.status]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


class RouteAssignmentAdmin(ModelView, model=RouteAssignment):
    name = "Route Assignment"
    name_plural = "Route Assignments"
    icon = "fa-solid fa-route"
    column_list = [RouteAssignment.id, RouteAssignment.route_id, RouteAssignment.vehicle_id, RouteAssignment.driver_id, RouteAssignment.status]
    column_searchable_list = [RouteAssignment.status]
    column_sortable_list = [RouteAssignment.id, RouteAssignment.status, RouteAssignment.created_at]
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    
    def is_accessible(self, request: Request) -> bool:
        # Проверяем, что пользователь аутентифицирован и имеет роль admin
        user_role = request.session.get("role")
        return user_role == "admin"


admin.add_view(VehicleAdmin)
admin.add_view(DriverAdmin)
admin.add_view(RouteAssignmentAdmin)


@app.on_event("startup")
async def startup_event():
    logger.info("Fleet service starting up")
    create_tables()
    
    # Initialize repositories
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = SessionLocal()
    
    driver_repository = DriverRepository(db_session)
    vehicle_repository = VehicleRepository(db_session)
    
    # Initialize and start event service
    fleet_event_service = FleetEventService(publisher, subscriber, driver_repository, vehicle_repository)
    app.state.fleet_event_service = fleet_event_service
    
    try:
        fleet_event_service.start_listening()
        logger.info("Fleet event service started successfully")
    except Exception as e:
        logger.error("Failed to start fleet event service", error=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Fleet service shutting down")
    try:
        subscriber.disconnect()
        publisher.disconnect()
        logger.info("Fleet event service disconnected")
    except Exception as e:
        logger.error("Error disconnecting fleet event service", error=str(e))


@app.get("/")
async def root():
    return {"message": "Fleet Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fleet"}


@app.get("/admin-login")
async def admin_login_page():
    """Кастомная страница входа в админ-панель"""
    from pathlib import Path
    template_path = Path(__file__).parent / "templates" / "admin_login.html"
    with open(template_path, "r") as f:
        html_content = f.read()
    
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=html_content) 