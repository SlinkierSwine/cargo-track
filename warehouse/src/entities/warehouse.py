from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class WarehouseType(str, Enum):
    DISTRIBUTION_CENTER = "distribution_center"
    STORAGE_FACILITY = "storage_facility"
    COLD_STORAGE = "cold_storage"
    HAZARDOUS_MATERIALS = "hazardous_materials"
    GENERAL_WAREHOUSE = "general_warehouse"


class WarehouseStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    CLOSED = "closed"
    INACTIVE = "inactive"


class Warehouse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    warehouse_type: WarehouseType
    address: str
    city: str
    country: str
    postal_code: str
    phone: str
    email: str
    total_capacity_weight: float  # kg
    total_capacity_volume: float  # m³
    available_capacity_weight: float  # kg
    available_capacity_volume: float  # m³
    temperature_controlled: bool
    hazardous_materials_allowed: bool
    operating_hours: str
    status: WarehouseStatus = WarehouseStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WarehouseCreate(BaseModel):
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
    temperature_controlled: bool = False
    hazardous_materials_allowed: bool = False
    operating_hours: str = "24/7"


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    warehouse_type: Optional[WarehouseType] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    total_capacity_weight: Optional[float] = None
    total_capacity_volume: Optional[float] = None
    temperature_controlled: Optional[bool] = None
    hazardous_materials_allowed: Optional[bool] = None
    operating_hours: Optional[str] = None
    status: Optional[WarehouseStatus] = None


class WarehouseResponse(BaseModel):
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
    created_at: datetime
    updated_at: datetime 