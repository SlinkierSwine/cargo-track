from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from entities.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate, WarehouseType, WarehouseStatus
from entities.database_models import WarehouseModel
from repositories.interfaces.warehouse_repository import IWarehouseRepository


class WarehouseRepository(IWarehouseRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, warehouse_data: WarehouseCreate) -> Warehouse:
        db_warehouse = WarehouseModel(
            name=warehouse_data.name,
            warehouse_type=warehouse_data.warehouse_type.value,
            address=warehouse_data.address,
            city=warehouse_data.city,
            country=warehouse_data.country,
            postal_code=warehouse_data.postal_code,
            phone=warehouse_data.phone,
            email=warehouse_data.email,
            total_capacity_weight=warehouse_data.total_capacity_weight,
            total_capacity_volume=warehouse_data.total_capacity_volume,
            available_capacity_weight=warehouse_data.total_capacity_weight,
            available_capacity_volume=warehouse_data.total_capacity_volume,
            temperature_controlled=warehouse_data.temperature_controlled,
            hazardous_materials_allowed=warehouse_data.hazardous_materials_allowed,
            operating_hours=warehouse_data.operating_hours,
            status=WarehouseStatus.ACTIVE.value
        )
        
        self.session.add(db_warehouse)
        self.session.commit()
        self.session.refresh(db_warehouse)
        
        return Warehouse(
            id=db_warehouse.id,
            name=db_warehouse.name,
            warehouse_type=WarehouseType(db_warehouse.warehouse_type),
            address=db_warehouse.address,
            city=db_warehouse.city,
            country=db_warehouse.country,
            postal_code=db_warehouse.postal_code,
            phone=db_warehouse.phone,
            email=db_warehouse.email,
            total_capacity_weight=db_warehouse.total_capacity_weight,
            total_capacity_volume=db_warehouse.total_capacity_volume,
            available_capacity_weight=db_warehouse.available_capacity_weight,
            available_capacity_volume=db_warehouse.available_capacity_volume,
            temperature_controlled=db_warehouse.temperature_controlled,
            hazardous_materials_allowed=db_warehouse.hazardous_materials_allowed,
            operating_hours=db_warehouse.operating_hours,
            status=WarehouseStatus(db_warehouse.status),
            created_at=db_warehouse.created_at,
            updated_at=db_warehouse.updated_at
        )
    
    def get_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        db_warehouse = self.session.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()
        
        if not db_warehouse:
            return None
            
        return Warehouse(
            id=db_warehouse.id,
            name=db_warehouse.name,
            warehouse_type=WarehouseType(db_warehouse.warehouse_type),
            address=db_warehouse.address,
            city=db_warehouse.city,
            country=db_warehouse.country,
            postal_code=db_warehouse.postal_code,
            phone=db_warehouse.phone,
            email=db_warehouse.email,
            total_capacity_weight=db_warehouse.total_capacity_weight,
            total_capacity_volume=db_warehouse.total_capacity_volume,
            available_capacity_weight=db_warehouse.available_capacity_weight,
            available_capacity_volume=db_warehouse.available_capacity_volume,
            temperature_controlled=db_warehouse.temperature_controlled,
            hazardous_materials_allowed=db_warehouse.hazardous_materials_allowed,
            operating_hours=db_warehouse.operating_hours,
            status=WarehouseStatus(db_warehouse.status),
            created_at=db_warehouse.created_at,
            updated_at=db_warehouse.updated_at
        )
    
    def get_by_name(self, name: str) -> Optional[Warehouse]:
        db_warehouse = self.session.query(WarehouseModel).filter(WarehouseModel.name == name).first()
        
        if not db_warehouse:
            return None
            
        return Warehouse(
            id=db_warehouse.id,
            name=db_warehouse.name,
            warehouse_type=WarehouseType(db_warehouse.warehouse_type),
            address=db_warehouse.address,
            city=db_warehouse.city,
            country=db_warehouse.country,
            postal_code=db_warehouse.postal_code,
            phone=db_warehouse.phone,
            email=db_warehouse.email,
            total_capacity_weight=db_warehouse.total_capacity_weight,
            total_capacity_volume=db_warehouse.total_capacity_volume,
            available_capacity_weight=db_warehouse.available_capacity_weight,
            available_capacity_volume=db_warehouse.available_capacity_volume,
            temperature_controlled=db_warehouse.temperature_controlled,
            hazardous_materials_allowed=db_warehouse.hazardous_materials_allowed,
            operating_hours=db_warehouse.operating_hours,
            status=WarehouseStatus(db_warehouse.status),
            created_at=db_warehouse.created_at,
            updated_at=db_warehouse.updated_at
        )
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        db_warehouses = self.session.query(WarehouseModel).offset(skip).limit(limit).all()
        
        return [
            Warehouse(
                id=db_warehouse.id,
                name=db_warehouse.name,
                warehouse_type=WarehouseType(db_warehouse.warehouse_type),
                address=db_warehouse.address,
                city=db_warehouse.city,
                country=db_warehouse.country,
                postal_code=db_warehouse.postal_code,
                phone=db_warehouse.phone,
                email=db_warehouse.email,
                total_capacity_weight=db_warehouse.total_capacity_weight,
                total_capacity_volume=db_warehouse.total_capacity_volume,
                available_capacity_weight=db_warehouse.available_capacity_weight,
                available_capacity_volume=db_warehouse.available_capacity_volume,
                temperature_controlled=db_warehouse.temperature_controlled,
                hazardous_materials_allowed=db_warehouse.hazardous_materials_allowed,
                operating_hours=db_warehouse.operating_hours,
                status=WarehouseStatus(db_warehouse.status),
                created_at=db_warehouse.created_at,
                updated_at=db_warehouse.updated_at
            )
            for db_warehouse in db_warehouses
        ]
    
    def list_warehouses(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        return self.get_all(skip, limit)
    
    def update(self, warehouse_id: str, warehouse_update: WarehouseUpdate) -> Optional[Warehouse]:
        db_warehouse = self.session.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()
        
        if not db_warehouse:
            return None
        
        if warehouse_update.name is not None:
            db_warehouse.name = warehouse_update.name
        if warehouse_update.warehouse_type is not None:
            db_warehouse.warehouse_type = warehouse_update.warehouse_type.value
        if warehouse_update.address is not None:
            db_warehouse.address = warehouse_update.address
        if warehouse_update.city is not None:
            db_warehouse.city = warehouse_update.city
        if warehouse_update.country is not None:
            db_warehouse.country = warehouse_update.country
        if warehouse_update.postal_code is not None:
            db_warehouse.postal_code = warehouse_update.postal_code
        if warehouse_update.phone is not None:
            db_warehouse.phone = warehouse_update.phone
        if warehouse_update.email is not None:
            db_warehouse.email = warehouse_update.email
        if warehouse_update.total_capacity_weight is not None:
            db_warehouse.total_capacity_weight = warehouse_update.total_capacity_weight
        if warehouse_update.total_capacity_volume is not None:
            db_warehouse.total_capacity_volume = warehouse_update.total_capacity_volume
        if warehouse_update.temperature_controlled is not None:
            db_warehouse.temperature_controlled = warehouse_update.temperature_controlled
        if warehouse_update.hazardous_materials_allowed is not None:
            db_warehouse.hazardous_materials_allowed = warehouse_update.hazardous_materials_allowed
        if warehouse_update.operating_hours is not None:
            db_warehouse.operating_hours = warehouse_update.operating_hours
        if warehouse_update.status is not None:
            db_warehouse.status = warehouse_update.status.value
        
        self.session.commit()
        self.session.refresh(db_warehouse)
        
        return Warehouse(
            id=db_warehouse.id,
            name=db_warehouse.name,
            warehouse_type=WarehouseType(db_warehouse.warehouse_type),
            address=db_warehouse.address,
            city=db_warehouse.city,
            country=db_warehouse.country,
            postal_code=db_warehouse.postal_code,
            phone=db_warehouse.phone,
            email=db_warehouse.email,
            total_capacity_weight=db_warehouse.total_capacity_weight,
            total_capacity_volume=db_warehouse.total_capacity_volume,
            available_capacity_weight=db_warehouse.available_capacity_weight,
            available_capacity_volume=db_warehouse.available_capacity_volume,
            temperature_controlled=db_warehouse.temperature_controlled,
            hazardous_materials_allowed=db_warehouse.hazardous_materials_allowed,
            operating_hours=db_warehouse.operating_hours,
            status=WarehouseStatus(db_warehouse.status),
            created_at=db_warehouse.created_at,
            updated_at=db_warehouse.updated_at
        )
    
    def delete(self, warehouse_id: str) -> bool:
        db_warehouse = self.session.query(WarehouseModel).filter(WarehouseModel.id == warehouse_id).first()
        if not db_warehouse:
            return False
        
        self.session.delete(db_warehouse)
        self.session.commit()
        return True 