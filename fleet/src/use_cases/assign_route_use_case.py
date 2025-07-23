from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from entities.route_assignment import RouteAssignment, RouteAssignmentCreate, RouteAssignmentStatus
from repositories.interfaces.vehicle_repository import IVehicleRepository
from repositories.interfaces.driver_repository import IDriverRepository
from repositories.interfaces.route_assignment_repository import IRouteAssignmentRepository


class AssignRouteRequest(BaseModel):
    route_id: UUID
    vehicle_id: UUID
    driver_id: UUID
    estimated_duration_hours: float = Field(..., gt=0)
    notes: Optional[str] = None


class AssignRouteResponse(BaseModel):
    id: str
    route_id: str
    vehicle_id: str
    driver_id: str
    status: str
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration_hours: float
    actual_duration_hours: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AssignRouteUseCase:
    def __init__(self, vehicle_repository: IVehicleRepository, driver_repository: IDriverRepository, route_assignment_repository: IRouteAssignmentRepository):
        self.vehicle_repository = vehicle_repository
        self.driver_repository = driver_repository
        self.route_assignment_repository = route_assignment_repository
    
    def execute(self, request: AssignRouteRequest) -> AssignRouteResponse:
        # Check if vehicle exists and is available
        vehicle = self.vehicle_repository.get_by_id(request.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        
        if vehicle.status != "active":
            raise ValueError("Vehicle is not available for assignment")
        
        # Check if driver exists and is available
        driver = self.driver_repository.get_by_id(request.driver_id)
        if not driver:
            raise ValueError("Driver not found")
        
        if driver.status != "active":
            raise ValueError("Driver is not available for assignment")
        
        # Check if driver's license and medical certificate are valid
        current_time = datetime.now()
        if driver.license_expiry <= current_time:
            raise ValueError("Driver's license has expired")
        
        if driver.medical_certificate_expiry <= current_time:
            raise ValueError("Driver's medical certificate has expired")
        
        # Validate estimated duration
        if request.estimated_duration_hours <= 0:
            raise ValueError("Estimated duration must be positive")
        
        # Create route assignment
        assignment_data = RouteAssignmentCreate(
            route_id=request.route_id,
            vehicle_id=request.vehicle_id,
            driver_id=request.driver_id,
            estimated_duration_hours=request.estimated_duration_hours,
            notes=request.notes
        )
        
        # Create route assignment
        assignment = self.route_assignment_repository.create(assignment_data)
        
        return AssignRouteResponse(
            id=str(assignment.id),
            route_id=str(assignment.route_id),
            vehicle_id=str(assignment.vehicle_id),
            driver_id=str(assignment.driver_id),
            status=assignment.status,
            assigned_at=assignment.assigned_at,
            started_at=assignment.started_at,
            completed_at=assignment.completed_at,
            estimated_duration_hours=assignment.estimated_duration_hours,
            actual_duration_hours=assignment.actual_duration_hours,
            notes=assignment.notes,
            created_at=assignment.created_at,
            updated_at=assignment.updated_at
        ) 