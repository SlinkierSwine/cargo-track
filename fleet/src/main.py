from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from config.settings import get_settings
from config.logging import setup_logging
from config.database import create_tables, engine
from controllers.vehicle_controller import router as vehicle_router
from controllers.driver_controller import router as driver_router
from controllers.route_assignment_controller import router as route_assignment_router
from entities.database_models import Vehicle, Driver, RouteAssignment
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

# Include routers
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(route_assignment_router)

# Setup admin panel
admin = Admin(app, engine)

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


admin.add_view(VehicleAdmin)
admin.add_view(DriverAdmin)
admin.add_view(RouteAssignmentAdmin)


@app.on_event("startup")
async def startup_event():
    logger.info("Fleet service starting up")
    create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Fleet service shutting down")


@app.get("/")
async def root():
    return {"message": "Fleet Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fleet"} 