from typing import Optional, List
from sqlalchemy.orm import Session
from entities.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from entities.database_models import Vehicle as VehicleModel
from repositories.interfaces.vehicle_repository import IVehicleRepository


class VehicleRepository(IVehicleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, vehicle: VehicleCreate) -> Vehicle:
        db_vehicle = VehicleModel(
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            brand=vehicle.brand,
            model=vehicle.model,
            year=vehicle.year,
            capacity_weight=vehicle.capacity_weight,
            capacity_volume=vehicle.capacity_volume,
            fuel_type=vehicle.fuel_type,
            fuel_efficiency=vehicle.fuel_efficiency,
            insurance_expiry=vehicle.insurance_expiry,
            registration_expiry=vehicle.registration_expiry
        )
        self.db_session.add(db_vehicle)
        self.db_session.commit()
        self.db_session.refresh(db_vehicle)
        
        return Vehicle(
            id=db_vehicle.id,
            license_plate=db_vehicle.license_plate,
            vehicle_type=db_vehicle.vehicle_type,
            brand=db_vehicle.brand,
            model=db_vehicle.model,
            year=db_vehicle.year,
            capacity_weight=db_vehicle.capacity_weight,
            capacity_volume=db_vehicle.capacity_volume,
            fuel_type=db_vehicle.fuel_type,
            fuel_efficiency=db_vehicle.fuel_efficiency,
            status=db_vehicle.status,
            insurance_expiry=db_vehicle.insurance_expiry,
            registration_expiry=db_vehicle.registration_expiry,
            created_at=db_vehicle.created_at,
            updated_at=db_vehicle.updated_at
        )
    
    def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        db_vehicle = self.db_session.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not db_vehicle:
            return None
        
        return Vehicle(
            id=db_vehicle.id,
            license_plate=db_vehicle.license_plate,
            vehicle_type=db_vehicle.vehicle_type,
            brand=db_vehicle.brand,
            model=db_vehicle.model,
            year=db_vehicle.year,
            capacity_weight=db_vehicle.capacity_weight,
            capacity_volume=db_vehicle.capacity_volume,
            fuel_type=db_vehicle.fuel_type,
            fuel_efficiency=db_vehicle.fuel_efficiency,
            status=db_vehicle.status,
            insurance_expiry=db_vehicle.insurance_expiry,
            registration_expiry=db_vehicle.registration_expiry,
            created_at=db_vehicle.created_at,
            updated_at=db_vehicle.updated_at
        )
    
    def get_by_license_plate(self, license_plate: str) -> Optional[Vehicle]:
        db_vehicle = self.db_session.query(VehicleModel).filter(VehicleModel.license_plate == license_plate).first()
        if not db_vehicle:
            return None
        
        return Vehicle(
            id=db_vehicle.id,
            license_plate=db_vehicle.license_plate,
            vehicle_type=db_vehicle.vehicle_type,
            brand=db_vehicle.brand,
            model=db_vehicle.model,
            year=db_vehicle.year,
            capacity_weight=db_vehicle.capacity_weight,
            capacity_volume=db_vehicle.capacity_volume,
            fuel_type=db_vehicle.fuel_type,
            fuel_efficiency=db_vehicle.fuel_efficiency,
            status=db_vehicle.status,
            insurance_expiry=db_vehicle.insurance_expiry,
            registration_expiry=db_vehicle.registration_expiry,
            created_at=db_vehicle.created_at,
            updated_at=db_vehicle.updated_at
        )
    
    def get_by_status(self, status: str) -> List[Vehicle]:
        db_vehicles = self.db_session.query(VehicleModel).filter(VehicleModel.status == status).all()
        return [
            Vehicle(
                id=vehicle.id,
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
                insurance_expiry=vehicle.insurance_expiry,
                registration_expiry=vehicle.registration_expiry,
                created_at=vehicle.created_at,
                updated_at=vehicle.updated_at
            )
            for vehicle in db_vehicles
        ]
    
    def get_all(self) -> List[Vehicle]:
        db_vehicles = self.db_session.query(VehicleModel).all()
        return [
            Vehicle(
                id=db_vehicle.id,
                license_plate=db_vehicle.license_plate,
                vehicle_type=db_vehicle.vehicle_type,
                brand=db_vehicle.brand,
                model=db_vehicle.model,
                year=db_vehicle.year,
                capacity_weight=db_vehicle.capacity_weight,
                capacity_volume=db_vehicle.capacity_volume,
                fuel_type=db_vehicle.fuel_type,
                fuel_efficiency=db_vehicle.fuel_efficiency,
                status=db_vehicle.status,
                insurance_expiry=db_vehicle.insurance_expiry,
                registration_expiry=db_vehicle.registration_expiry,
                created_at=db_vehicle.created_at,
                updated_at=db_vehicle.updated_at
            )
            for db_vehicle in db_vehicles
        ]
    
    def update(self, vehicle_id: str, vehicle: VehicleUpdate) -> Optional[Vehicle]:
        db_vehicle = self.db_session.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not db_vehicle:
            return None
        
        update_data = vehicle.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vehicle, field, value)
        
        self.db_session.commit()
        self.db_session.refresh(db_vehicle)
        
        return Vehicle(
            id=db_vehicle.id,
            license_plate=db_vehicle.license_plate,
            vehicle_type=db_vehicle.vehicle_type,
            brand=db_vehicle.brand,
            model=db_vehicle.model,
            year=db_vehicle.year,
            capacity_weight=db_vehicle.capacity_weight,
            capacity_volume=db_vehicle.capacity_volume,
            fuel_type=db_vehicle.fuel_type,
            fuel_efficiency=db_vehicle.fuel_efficiency,
            status=db_vehicle.status,
            insurance_expiry=db_vehicle.insurance_expiry,
            registration_expiry=db_vehicle.registration_expiry,
            created_at=db_vehicle.created_at,
            updated_at=db_vehicle.updated_at
        )
    
    def delete(self, vehicle_id: str) -> bool:
        db_vehicle = self.db_session.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
        if not db_vehicle:
            return False
        
        self.db_session.delete(db_vehicle)
        self.db_session.commit()
        return True 