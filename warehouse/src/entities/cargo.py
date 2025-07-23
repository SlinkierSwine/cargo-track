from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum
import uuid


class CargoType(str, Enum):
    GENERAL = "general"
    HAZARDOUS = "hazardous"
    PERISHABLE = "perishable"
    FRAGILE = "fragile"
    OVERSIZED = "oversized"
    REFRIGERATED = "refrigerated"


class CargoStatus(str, Enum):
    RECEIVED = "received"
    STORED = "stored"
    LOADING = "loading"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    DAMAGED = "damaged"
    LOST = "lost"


class FragilityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class TemperatureRange(BaseModel):
    min_temp: float  # Celsius
    max_temp: float  # Celsius


class HumidityRange(BaseModel):
    min_humidity: float  # Percentage
    max_humidity: float  # Percentage


class Cargo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tracking_number: str
    cargo_type: CargoType
    name: str
    description: str
    weight: float  # kg
    volume: float  # m³
    dimensions: Dict[str, float]  # length, width, height
    value: float
    insurance_amount: float
    temperature_requirements: Optional[TemperatureRange] = None
    humidity_requirements: Optional[HumidityRange] = None
    hazardous_material: bool = False
    hazardous_class: Optional[str] = None
    special_handling: List[str] = Field(default_factory=list)
    fragility_level: FragilityLevel = FragilityLevel.LOW
    storage_duration: int  # days
    expiration_date: Optional[datetime] = None
    status: CargoStatus = CargoStatus.RECEIVED
    warehouse_id: Optional[str] = None
    location_in_warehouse: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CargoCreate(BaseModel):
    tracking_number: str
    cargo_type: CargoType
    name: str
    description: str
    weight: float
    volume: float
    dimensions: Dict[str, float]
    value: float
    insurance_amount: float
    temperature_requirements: Optional[TemperatureRange] = None
    humidity_requirements: Optional[HumidityRange] = None
    hazardous_material: bool = False
    hazardous_class: Optional[str] = None
    special_handling: List[str] = Field(default_factory=list)
    fragility_level: FragilityLevel = FragilityLevel.LOW
    storage_duration: int
    expiration_date: Optional[datetime] = None


class CargoUpdate(BaseModel):
    tracking_number: Optional[str] = None
    cargo_type: Optional[CargoType] = None
    name: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    volume: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None
    value: Optional[float] = None
    insurance_amount: Optional[float] = None
    temperature_requirements: Optional[TemperatureRange] = None
    humidity_requirements: Optional[HumidityRange] = None
    hazardous_material: Optional[bool] = None
    hazardous_class: Optional[str] = None
    special_handling: Optional[List[str]] = None
    fragility_level: Optional[FragilityLevel] = None
    storage_duration: Optional[int] = None
    expiration_date: Optional[datetime] = None
    status: Optional[CargoStatus] = None
    warehouse_id: Optional[str] = None
    location_in_warehouse: Optional[str] = None


class CargoResponse(BaseModel):
    id: str
    tracking_number: str
    cargo_type: CargoType
    name: str
    description: str
    weight: float
    volume: float
    dimensions: Dict[str, float]
    value: float
    insurance_amount: float
    temperature_requirements: Optional[TemperatureRange]
    humidity_requirements: Optional[HumidityRange]
    hazardous_material: bool
    hazardous_class: Optional[str]
    special_handling: List[str]
    fragility_level: FragilityLevel
    storage_duration: int
    expiration_date: Optional[datetime]
    status: CargoStatus
    warehouse_id: Optional[str]
    location_in_warehouse: Optional[str]
    created_at: datetime
    updated_at: datetime 