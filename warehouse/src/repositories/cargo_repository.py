from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from entities.cargo import Cargo, CargoCreate, CargoUpdate, CargoType, CargoStatus
from entities.database_models import CargoModel
from repositories.interfaces.cargo_repository import CargoRepositoryInterface


class CargoRepository(CargoRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, cargo_data: CargoCreate) -> Cargo:
        db_cargo = CargoModel(
            tracking_number=cargo_data.tracking_number,
            cargo_type=cargo_data.cargo_type.value,
            name=cargo_data.name,
            description=cargo_data.description,
            weight=cargo_data.weight,
            volume=cargo_data.volume,
            dimensions=cargo_data.dimensions,
            value=cargo_data.value,
            insurance_amount=cargo_data.insurance_amount,
            temperature_requirements=cargo_data.temperature_requirements,
            humidity_requirements=cargo_data.humidity_requirements,
            hazardous_material=cargo_data.hazardous_material,
            hazardous_class=cargo_data.hazardous_class,
            special_handling=cargo_data.special_handling,
            fragility_level=cargo_data.fragility_level,
            storage_duration=cargo_data.storage_duration,
            expiration_date=cargo_data.expiration_date,
            status=CargoStatus.RECEIVED.value,
            warehouse_id=None,
            location_in_warehouse=None
        )
        
        self.session.add(db_cargo)
        self.session.commit()
        self.session.refresh(db_cargo)
        
        return Cargo(
            id=db_cargo.id,
            tracking_number=db_cargo.tracking_number,
            cargo_type=CargoType(db_cargo.cargo_type),
            name=db_cargo.name,
            description=db_cargo.description,
            weight=db_cargo.weight,
            volume=db_cargo.volume,
            dimensions=db_cargo.dimensions,
            value=db_cargo.value,
            insurance_amount=db_cargo.insurance_amount,
            temperature_requirements=db_cargo.temperature_requirements,
            humidity_requirements=db_cargo.humidity_requirements,
            hazardous_material=db_cargo.hazardous_material,
            hazardous_class=db_cargo.hazardous_class,
            special_handling=db_cargo.special_handling,
            fragility_level=db_cargo.fragility_level,
            storage_duration=db_cargo.storage_duration,
            expiration_date=db_cargo.expiration_date,
            status=CargoStatus(db_cargo.status),
            warehouse_id=db_cargo.warehouse_id,
            location_in_warehouse=db_cargo.location_in_warehouse,
            created_at=db_cargo.created_at,
            updated_at=db_cargo.updated_at
        )
    
    def get_by_id(self, cargo_id: str) -> Optional[Cargo]:
        db_cargo = self.session.query(CargoModel).filter(CargoModel.id == cargo_id).first()
        
        if not db_cargo:
            return None
            
        return Cargo(
            id=db_cargo.id,
            tracking_number=db_cargo.tracking_number,
            cargo_type=CargoType(db_cargo.cargo_type),
            name=db_cargo.name,
            description=db_cargo.description,
            weight=db_cargo.weight,
            volume=db_cargo.volume,
            dimensions=db_cargo.dimensions,
            value=db_cargo.value,
            insurance_amount=db_cargo.insurance_amount,
            temperature_requirements=db_cargo.temperature_requirements,
            humidity_requirements=db_cargo.humidity_requirements,
            hazardous_material=db_cargo.hazardous_material,
            hazardous_class=db_cargo.hazardous_class,
            special_handling=db_cargo.special_handling,
            fragility_level=db_cargo.fragility_level,
            storage_duration=db_cargo.storage_duration,
            expiration_date=db_cargo.expiration_date,
            status=CargoStatus(db_cargo.status),
            warehouse_id=db_cargo.warehouse_id,
            location_in_warehouse=db_cargo.location_in_warehouse,
            created_at=db_cargo.created_at,
            updated_at=db_cargo.updated_at
        )
    
    def get_by_tracking_number(self, tracking_number: str) -> Optional[Cargo]:
        db_cargo = self.session.query(CargoModel).filter(CargoModel.tracking_number == tracking_number).first()
        
        if not db_cargo:
            return None
            
        return Cargo(
            id=db_cargo.id,
            tracking_number=db_cargo.tracking_number,
            cargo_type=CargoType(db_cargo.cargo_type),
            name=db_cargo.name,
            description=db_cargo.description,
            weight=db_cargo.weight,
            volume=db_cargo.volume,
            dimensions=db_cargo.dimensions,
            value=db_cargo.value,
            insurance_amount=db_cargo.insurance_amount,
            temperature_requirements=db_cargo.temperature_requirements,
            humidity_requirements=db_cargo.humidity_requirements,
            hazardous_material=db_cargo.hazardous_material,
            hazardous_class=db_cargo.hazardous_class,
            special_handling=db_cargo.special_handling,
            fragility_level=db_cargo.fragility_level,
            storage_duration=db_cargo.storage_duration,
            expiration_date=db_cargo.expiration_date,
            status=CargoStatus(db_cargo.status),
            warehouse_id=db_cargo.warehouse_id,
            location_in_warehouse=db_cargo.location_in_warehouse,
            created_at=db_cargo.created_at,
            updated_at=db_cargo.updated_at
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cargo]:
        db_cargos = self.session.query(CargoModel).offset(skip).limit(limit).all()
        
        return [
            Cargo(
                id=db_cargo.id,
                tracking_number=db_cargo.tracking_number,
                cargo_type=CargoType(db_cargo.cargo_type),
                name=db_cargo.name,
                description=db_cargo.description,
                weight=db_cargo.weight,
                volume=db_cargo.volume,
                dimensions=db_cargo.dimensions,
                value=db_cargo.value,
                insurance_amount=db_cargo.insurance_amount,
                temperature_requirements=db_cargo.temperature_requirements,
                humidity_requirements=db_cargo.humidity_requirements,
                hazardous_material=db_cargo.hazardous_material,
                hazardous_class=db_cargo.hazardous_class,
                special_handling=db_cargo.special_handling,
                fragility_level=db_cargo.fragility_level,
                storage_duration=db_cargo.storage_duration,
                expiration_date=db_cargo.expiration_date,
                status=CargoStatus(db_cargo.status),
                warehouse_id=db_cargo.warehouse_id,
                location_in_warehouse=db_cargo.location_in_warehouse,
                created_at=db_cargo.created_at,
                updated_at=db_cargo.updated_at
            )
            for db_cargo in db_cargos
        ]
    
    def list_cargo(self, skip: int = 0, limit: int = 100) -> List[Cargo]:
        return self.get_all(skip, limit)
    
    def get_by_warehouse_id(self, warehouse_id: str) -> List[Cargo]:
        db_cargos = self.session.query(CargoModel).filter(CargoModel.warehouse_id == warehouse_id).all()
        
        return [
            Cargo(
                id=db_cargo.id,
                tracking_number=db_cargo.tracking_number,
                cargo_type=CargoType(db_cargo.cargo_type),
                name=db_cargo.name,
                description=db_cargo.description,
                weight=db_cargo.weight,
                volume=db_cargo.volume,
                dimensions=db_cargo.dimensions,
                value=db_cargo.value,
                insurance_amount=db_cargo.insurance_amount,
                temperature_requirements=db_cargo.temperature_requirements,
                humidity_requirements=db_cargo.humidity_requirements,
                hazardous_material=db_cargo.hazardous_material,
                hazardous_class=db_cargo.hazardous_class,
                special_handling=db_cargo.special_handling,
                fragility_level=db_cargo.fragility_level,
                storage_duration=db_cargo.storage_duration,
                expiration_date=db_cargo.expiration_date,
                status=CargoStatus(db_cargo.status),
                warehouse_id=db_cargo.warehouse_id,
                location_in_warehouse=db_cargo.location_in_warehouse,
                created_at=db_cargo.created_at,
                updated_at=db_cargo.updated_at
            )
            for db_cargo in db_cargos
        ]
    
    def update(self, cargo_id: str, cargo_update: CargoUpdate) -> Optional[Cargo]:
        db_cargo = self.session.query(CargoModel).filter(CargoModel.id == cargo_id).first()
        
        if not db_cargo:
            return None
        
        if cargo_update.tracking_number is not None:
            db_cargo.tracking_number = cargo_update.tracking_number
        if cargo_update.cargo_type is not None:
            db_cargo.cargo_type = cargo_update.cargo_type.value
        if cargo_update.name is not None:
            db_cargo.name = cargo_update.name
        if cargo_update.description is not None:
            db_cargo.description = cargo_update.description
        if cargo_update.weight is not None:
            db_cargo.weight = cargo_update.weight
        if cargo_update.volume is not None:
            db_cargo.volume = cargo_update.volume
        if cargo_update.dimensions is not None:
            db_cargo.dimensions = cargo_update.dimensions
        if cargo_update.value is not None:
            db_cargo.value = cargo_update.value
        if cargo_update.insurance_amount is not None:
            db_cargo.insurance_amount = cargo_update.insurance_amount
        if cargo_update.temperature_requirements is not None:
            db_cargo.temperature_requirements = cargo_update.temperature_requirements
        if cargo_update.humidity_requirements is not None:
            db_cargo.humidity_requirements = cargo_update.humidity_requirements
        if cargo_update.hazardous_material is not None:
            db_cargo.hazardous_material = cargo_update.hazardous_material
        if cargo_update.hazardous_class is not None:
            db_cargo.hazardous_class = cargo_update.hazardous_class
        if cargo_update.special_handling is not None:
            db_cargo.special_handling = cargo_update.special_handling
        if cargo_update.fragility_level is not None:
            db_cargo.fragility_level = cargo_update.fragility_level
        if cargo_update.storage_duration is not None:
            db_cargo.storage_duration = cargo_update.storage_duration
        if cargo_update.expiration_date is not None:
            db_cargo.expiration_date = cargo_update.expiration_date
        if cargo_update.status is not None:
            db_cargo.status = cargo_update.status.value
        if cargo_update.warehouse_id is not None:
            db_cargo.warehouse_id = cargo_update.warehouse_id
        if cargo_update.location_in_warehouse is not None:
            db_cargo.location_in_warehouse = cargo_update.location_in_warehouse
        
        self.session.commit()
        self.session.refresh(db_cargo)
        
        return Cargo(
            id=db_cargo.id,
            tracking_number=db_cargo.tracking_number,
            cargo_type=CargoType(db_cargo.cargo_type),
            name=db_cargo.name,
            description=db_cargo.description,
            weight=db_cargo.weight,
            volume=db_cargo.volume,
            dimensions=db_cargo.dimensions,
            value=db_cargo.value,
            insurance_amount=db_cargo.insurance_amount,
            temperature_requirements=db_cargo.temperature_requirements,
            humidity_requirements=db_cargo.humidity_requirements,
            hazardous_material=db_cargo.hazardous_material,
            hazardous_class=db_cargo.hazardous_class,
            special_handling=db_cargo.special_handling,
            fragility_level=db_cargo.fragility_level,
            storage_duration=db_cargo.storage_duration,
            expiration_date=db_cargo.expiration_date,
            status=CargoStatus(db_cargo.status),
            warehouse_id=db_cargo.warehouse_id,
            location_in_warehouse=db_cargo.location_in_warehouse,
            created_at=db_cargo.created_at,
            updated_at=db_cargo.updated_at
        )
    
    def delete(self, cargo_id: str) -> bool:
        db_cargo = self.session.query(CargoModel).filter(CargoModel.id == cargo_id).first()
        if not db_cargo:
            return False
        
        self.session.delete(db_cargo)
        self.session.commit()
        return True 