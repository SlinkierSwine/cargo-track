from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class CompatibilityReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cargo_id: str
    vehicle_id: str
    is_compatible: bool
    score: float  # 0.0 to 1.0
    weight_compatible: bool
    volume_compatible: bool
    temperature_compatible: bool
    hazardous_compatible: bool
    special_requirements_met: bool
    risks: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CompatibilityCheckRequest(BaseModel):
    cargo_id: str
    vehicle_id: str


class CompatibilityCheckResponse(BaseModel):
    id: str
    cargo_id: str
    vehicle_id: str
    is_compatible: bool
    score: float
    weight_compatible: bool
    volume_compatible: bool
    temperature_compatible: bool
    hazardous_compatible: bool
    special_requirements_met: bool
    risks: List[str]
    recommendations: List[str]
    created_at: datetime


class CompatibilityValidationRequest(BaseModel):
    cargo_ids: List[str]
    vehicle_ids: List[str]


class CompatibilityValidationResponse(BaseModel):
    valid_combinations: List[CompatibilityCheckResponse]
    invalid_combinations: List[CompatibilityCheckResponse]
    summary: dict 