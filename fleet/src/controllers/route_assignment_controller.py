from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from config.database import get_db
from entities.route_assignment import RouteAssignment, RouteAssignmentCreate, RouteAssignmentUpdate
from use_cases.assign_route_use_case import AssignRouteUseCase, AssignRouteRequest
from repositories.route_assignment_repository import RouteAssignmentRepository
from repositories.vehicle_repository import VehicleRepository
from repositories.driver_repository import DriverRepository
from utils.auth_utils import get_current_user, require_any_role


router = APIRouter(prefix="/route-assignments", tags=["route-assignments"])


def get_route_assignment_repository(db: Session = Depends(get_db)) -> RouteAssignmentRepository:
    return RouteAssignmentRepository(db)


def get_vehicle_repository(db: Session = Depends(get_db)) -> VehicleRepository:
    return VehicleRepository(db)


def get_driver_repository(db: Session = Depends(get_db)) -> DriverRepository:
    return DriverRepository(db)


def get_assign_route_use_case(
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    driver_repository: DriverRepository = Depends(get_driver_repository),
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository)
) -> AssignRouteUseCase:
    return AssignRouteUseCase(vehicle_repository, driver_repository, route_assignment_repository)


@router.post("/", response_model=RouteAssignment, status_code=status.HTTP_201_CREATED)
async def assign_route(
    assignment_data: RouteAssignmentCreate,
    use_case: AssignRouteUseCase = Depends(get_assign_route_use_case),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        request = AssignRouteRequest(
            route_id=assignment_data.route_id,
            vehicle_id=assignment_data.vehicle_id,
            driver_id=assignment_data.driver_id,
            estimated_duration_hours=assignment_data.estimated_duration_hours,
            notes=assignment_data.notes
        )
        result = use_case.execute(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[RouteAssignment])
async def get_all_route_assignments(
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository),
    current_user: dict = Depends(get_current_user)
):
    try:
        return route_assignment_repository.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{assignment_id}", response_model=RouteAssignment)
async def get_route_assignment_by_id(
    assignment_id: UUID,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository),
    current_user: dict = Depends(get_current_user)
):
    try:
        assignment = route_assignment_repository.get_by_id(assignment_id)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route assignment not found")
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{assignment_id}", response_model=RouteAssignment)
async def update_route_assignment(
    assignment_id: UUID,
    assignment_data: RouteAssignmentUpdate,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        assignment = route_assignment_repository.update(assignment_id, assignment_data)
        if not assignment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route assignment not found")
        return assignment
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route_assignment(
    assignment_id: UUID,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository),
    current_user: dict = Depends(require_any_role(["admin"]))
):
    try:
        success = route_assignment_repository.delete(assignment_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route assignment not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/route/{route_id}", response_model=List[RouteAssignment])
async def get_route_assignments_by_route_id(
    route_id: UUID,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository)
):
    try:
        return route_assignment_repository.get_by_route_id(route_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/vehicle/{vehicle_id}", response_model=List[RouteAssignment])
async def get_route_assignments_by_vehicle_id(
    vehicle_id: UUID,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository)
):
    try:
        return route_assignment_repository.get_by_vehicle_id(vehicle_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/driver/{driver_id}", response_model=List[RouteAssignment])
async def get_route_assignments_by_driver_id(
    driver_id: UUID,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository)
):
    try:
        return route_assignment_repository.get_by_driver_id(driver_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/status/{status}", response_model=List[RouteAssignment])
async def get_route_assignments_by_status(
    status: str,
    route_assignment_repository: RouteAssignmentRepository = Depends(get_route_assignment_repository)
):
    try:
        return route_assignment_repository.get_by_status(status)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 