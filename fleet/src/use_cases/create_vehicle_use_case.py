from typing import Optional
from pydantic import BaseModel
from entities.vehicle import Vehicle, VehicleCreate, VehicleResponse
from repositories.interfaces.vehicle_repository import IVehicleRepository


class CreateVehicleRequest(BaseModel):
    license_plate: str
    vehicle_type: str
    brand: str
    model: str
    year: int
    capacity_weight: float
    capacity_volume: float
    fuel_type: str
    fuel_efficiency: float
    insurance_expiry: str
    registration_expiry: str


class CreateVehicleResponse(BaseModel):
    id: str
    license_plate: str
    vehicle_type: str
    brand: str
    model: str
    year: int
    capacity_weight: float
    capacity_volume: float
    fuel_type: str
    fuel_efficiency: float
    status: str
    insurance_expiry: str
    registration_expiry: str


class CreateVehicleUseCase:
    def __init__(self, vehicle_repository: IVehicleRepository):
        self.vehicle_repository = vehicle_repository
    
    def execute(self, request: CreateVehicleRequest) -> CreateVehicleResponse:
        existing_vehicle = self.vehicle_repository.get_by_license_plate(request.license_plate)
        if existing_vehicle:
            raise ValueError("Vehicle with this license plate already exists")
        
        vehicle_data = VehicleCreate(
            license_plate=request.license_plate,
            vehicle_type=request.vehicle_type,
            brand=request.brand,
            model=request.model,
            year=request.year,
            capacity_weight=request.capacity_weight,
            capacity_volume=request.capacity_volume,
            fuel_type=request.fuel_type,
            fuel_efficiency=request.fuel_efficiency,
            insurance_expiry=request.insurance_expiry,
            registration_expiry=request.registration_expiry
        )
        
        vehicle = self.vehicle_repository.create(vehicle_data)
        
        return CreateVehicleResponse(
            id=str(vehicle.id),
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            capacity_weight=vehicle.capacity_weight,
            capacity_volume=vehicle.capacity_volume,
            fuel_type=vehicle.fuel_type,
            fuel_efficiency=vehicle.fuel_efficiency,
            status=vehicle.status,
            insurance_expiry=str(vehicle.insurance_expiry),
            registration_expiry=str(vehicle.registration_expiry)
        ) 