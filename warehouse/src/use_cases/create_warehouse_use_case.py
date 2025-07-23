from typing import Optional
from pydantic import BaseModel, Field
from entities.warehouse import Warehouse, WarehouseCreate, WarehouseResponse, WarehouseType, WarehouseStatus
from repositories.interfaces.warehouse_repository import IWarehouseRepository
from shared.use_cases.base_use_case import BaseUseCase


class CreateWarehouseRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    warehouse_type: WarehouseType
    address: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    phone: str = Field(..., min_length=1, max_length=20)
    email: str = Field(..., min_length=1, max_length=100)
    total_capacity_weight: float = Field(..., gt=0)
    total_capacity_volume: float = Field(..., gt=0)
    temperature_controlled: bool = False
    hazardous_materials_allowed: bool = False
    operating_hours: str = "24/7"


class CreateWarehouseResponse(BaseModel):
    id: str
    name: str
    warehouse_type: WarehouseType
    address: str
    city: str
    country: str
    postal_code: str
    phone: str
    email: str
    total_capacity_weight: float
    total_capacity_volume: float
    available_capacity_weight: float
    available_capacity_volume: float
    temperature_controlled: bool
    hazardous_materials_allowed: bool
    operating_hours: str
    status: WarehouseStatus
    created_at: str
    updated_at: str


class CreateWarehouseUseCase(BaseUseCase[CreateWarehouseResponse]):
    def __init__(self, warehouse_repository: IWarehouseRepository):
        super().__init__()
        self.warehouse_repository = warehouse_repository
    
    def execute(self, request: CreateWarehouseRequest) -> CreateWarehouseResponse:
        # Validate capacity values
        if request.total_capacity_weight <= 0 or request.total_capacity_volume <= 0:
            raise ValueError("Capacity values must be positive")
        
        # Validate hazardous materials warehouse requirements
        if request.warehouse_type == WarehouseType.HAZARDOUS_MATERIALS and not request.hazardous_materials_allowed:
            raise ValueError("Hazardous materials warehouse must allow hazardous materials")
        
        # Check if warehouse with this name already exists
        existing_warehouse = self.warehouse_repository.get_by_name(request.name)
        if existing_warehouse:
            raise ValueError("Warehouse with this name already exists")
        
        warehouse_data = WarehouseCreate(
            name=request.name,
            warehouse_type=request.warehouse_type,
            address=request.address,
            city=request.city,
            country=request.country,
            postal_code=request.postal_code,
            phone=request.phone,
            email=request.email,
            total_capacity_weight=request.total_capacity_weight,
            total_capacity_volume=request.total_capacity_volume,
            temperature_controlled=request.temperature_controlled,
            hazardous_materials_allowed=request.hazardous_materials_allowed,
            operating_hours=request.operating_hours
        )
        
        warehouse = self.warehouse_repository.create(warehouse_data)
        
        return CreateWarehouseResponse(
            id=warehouse.id,
            name=warehouse.name,
            warehouse_type=warehouse.warehouse_type,
            address=warehouse.address,
            city=warehouse.city,
            country=warehouse.country,
            postal_code=warehouse.postal_code,
            phone=warehouse.phone,
            email=warehouse.email,
            total_capacity_weight=warehouse.total_capacity_weight,
            total_capacity_volume=warehouse.total_capacity_volume,
            available_capacity_weight=warehouse.available_capacity_weight,
            available_capacity_volume=warehouse.available_capacity_volume,
            temperature_controlled=warehouse.temperature_controlled,
            hazardous_materials_allowed=warehouse.hazardous_materials_allowed,
            operating_hours=warehouse.operating_hours,
            status=warehouse.status,
            created_at=str(warehouse.created_at),
            updated_at=str(warehouse.updated_at)
        ) 