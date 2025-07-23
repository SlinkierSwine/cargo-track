from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime


class BaseEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class VehicleType(str, Enum):
    TRUCK = "truck"
    VAN = "van"
    TRAILER = "trailer"


class FuelType(str, Enum):
    DIESEL = "diesel"
    GASOLINE = "gasoline"
    ELECTRIC = "electric"


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"


class Vehicle(BaseEntity):
    license_plate: str = Field(..., min_length=1, max_length=20)
    vehicle_type: VehicleType
    brand: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=2030)
    capacity_weight: float = Field(..., gt=0)
    capacity_volume: float = Field(..., gt=0)
    fuel_type: FuelType
    fuel_efficiency: float = Field(..., gt=0)
    status: VehicleStatus = VehicleStatus.ACTIVE
    insurance_expiry: datetime
    registration_expiry: datetime


class VehicleCreate(BaseModel):
    license_plate: str = Field(..., min_length=1, max_length=20)
    vehicle_type: VehicleType
    brand: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1900, le=2030)
    capacity_weight: float = Field(..., gt=0)
    capacity_volume: float = Field(..., gt=0)
    fuel_type: FuelType
    fuel_efficiency: float = Field(..., gt=0)
    insurance_expiry: datetime
    registration_expiry: datetime


class VehicleUpdate(BaseModel):
    license_plate: Optional[str] = Field(None, min_length=1, max_length=20)
    vehicle_type: Optional[VehicleType] = None
    brand: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=1900, le=2030)
    capacity_weight: Optional[float] = Field(None, gt=0)
    capacity_volume: Optional[float] = Field(None, gt=0)
    fuel_type: Optional[FuelType] = None
    fuel_efficiency: Optional[float] = Field(None, gt=0)
    status: Optional[VehicleStatus] = None
    insurance_expiry: Optional[datetime] = None
    registration_expiry: Optional[datetime] = None


class VehicleResponse(BaseModel):
    id: UUID
    license_plate: str
    vehicle_type: VehicleType
    brand: str
    model: str
    year: int
    capacity_weight: float
    capacity_volume: float
    fuel_type: FuelType
    fuel_efficiency: float
    status: VehicleStatus
    insurance_expiry: datetime
    registration_expiry: datetime
    created_at: datetime
    updated_at: Optional[datetime] 