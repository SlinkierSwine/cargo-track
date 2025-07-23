from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from config.database import get_db
from entities.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from use_cases.create_vehicle_use_case import CreateVehicleUseCase
from repositories.vehicle_repository import VehicleRepository
from utils.auth_utils import get_current_user, require_any_role


router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def get_vehicle_repository(db: Session = Depends(get_db)) -> VehicleRepository:
    return VehicleRepository(db)


def get_create_vehicle_use_case(vehicle_repository: VehicleRepository = Depends(get_vehicle_repository)) -> CreateVehicleUseCase:
    return CreateVehicleUseCase(vehicle_repository)


@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    use_case: CreateVehicleUseCase = Depends(get_create_vehicle_use_case),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        result = use_case.execute(vehicle_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[Vehicle])
async def get_all_vehicles(
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(get_current_user())
):
    try:
        return vehicle_repository.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{vehicle_id}", response_model=Vehicle)
async def get_vehicle_by_id(
    vehicle_id: UUID,
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(get_current_user())
):
    try:
        vehicle = vehicle_repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{vehicle_id}", response_model=Vehicle)
async def update_vehicle(
    vehicle_id: UUID,
    vehicle_data: VehicleUpdate,
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        vehicle = vehicle_repository.update(vehicle_id, vehicle_data)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: UUID,
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(require_any_role(["admin"]))
):
    try:
        success = vehicle_repository.delete(vehicle_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/by-license/{license_plate}", response_model=Vehicle)
async def get_vehicle_by_license_plate(
    license_plate: str,
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(get_current_user())
):
    try:
        vehicle = vehicle_repository.get_by_license_plate(license_plate)
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
        return vehicle
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/status/{status}", response_model=List[Vehicle])
async def get_vehicles_by_status(
    status: str,
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
    current_user: dict = Depends(get_current_user())
):
    try:
        return vehicle_repository.get_by_status(status)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 