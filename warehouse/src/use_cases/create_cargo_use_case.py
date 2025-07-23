from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
from entities.cargo import Cargo, CargoCreate, CargoResponse, CargoType, CargoStatus, FragilityLevel, TemperatureRange, HumidityRange
from repositories.interfaces.cargo_repository import CargoRepositoryInterface
from shared.use_cases.base_use_case import BaseUseCase


class CreateCargoRequest(BaseModel):
    tracking_number: str = Field(..., min_length=1, max_length=50)
    cargo_type: CargoType
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    weight: float = Field(..., gt=0)
    volume: float = Field(..., gt=0)
    dimensions: Dict[str, float] = Field(..., min_length=3, max_length=3)
    value: float = Field(..., gt=0)
    insurance_amount: float = Field(..., gt=0)
    temperature_requirements: Optional[TemperatureRange] = None
    humidity_requirements: Optional[HumidityRange] = None
    hazardous_material: bool = False
    hazardous_class: Optional[str] = None
    special_handling: List[str] = Field(default_factory=list)
    fragility_level: FragilityLevel = FragilityLevel.LOW
    storage_duration: int = Field(..., gt=0)
    expiration_date: Optional[datetime] = None


class CreateCargoResponse(BaseModel):
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
    created_at: str
    updated_at: str


class CreateCargoUseCase(BaseUseCase[CreateCargoResponse]):
    def __init__(self, cargo_repository: CargoRepositoryInterface):
        super().__init__()
        self.cargo_repository = cargo_repository
    
    def execute(self, request: CreateCargoRequest) -> CreateCargoResponse:
        # Validate weight and volume
        if request.weight <= 0 or request.volume <= 0:
            raise ValueError("Weight and volume must be positive")
        
        # Validate dimensions
        for dimension, value in request.dimensions.items():
            if value <= 0:
                raise ValueError("All dimensions must be positive")
        
        # Validate hazardous materials
        if request.hazardous_material and not request.hazardous_class:
            raise ValueError("Hazardous class must be specified for hazardous materials")
        
        # Check if cargo with this tracking number already exists
        existing_cargo = self.cargo_repository.get_by_tracking_number(request.tracking_number)
        if existing_cargo:
            raise ValueError("Cargo with this tracking number already exists")
        
        cargo_data = CargoCreate(
            tracking_number=request.tracking_number,
            cargo_type=request.cargo_type,
            name=request.name,
            description=request.description,
            weight=request.weight,
            volume=request.volume,
            dimensions=request.dimensions,
            value=request.value,
            insurance_amount=request.insurance_amount,
            temperature_requirements=request.temperature_requirements,
            humidity_requirements=request.humidity_requirements,
            hazardous_material=request.hazardous_material,
            hazardous_class=request.hazardous_class,
            special_handling=request.special_handling,
            fragility_level=request.fragility_level,
            storage_duration=request.storage_duration,
            expiration_date=request.expiration_date
        )
        
        cargo = self.cargo_repository.create(cargo_data)
        
        return CreateCargoResponse(
            id=cargo.id,
            tracking_number=cargo.tracking_number,
            cargo_type=cargo.cargo_type,
            name=cargo.name,
            description=cargo.description,
            weight=cargo.weight,
            volume=cargo.volume,
            dimensions=cargo.dimensions,
            value=cargo.value,
            insurance_amount=cargo.insurance_amount,
            temperature_requirements=cargo.temperature_requirements,
            humidity_requirements=cargo.humidity_requirements,
            hazardous_material=cargo.hazardous_material,
            hazardous_class=cargo.hazardous_class,
            special_handling=cargo.special_handling,
            fragility_level=cargo.fragility_level,
            storage_duration=cargo.storage_duration,
            expiration_date=cargo.expiration_date,
            status=cargo.status,
            warehouse_id=cargo.warehouse_id,
            location_in_warehouse=cargo.location_in_warehouse,
            created_at=str(cargo.created_at),
            updated_at=str(cargo.updated_at)
        ) 