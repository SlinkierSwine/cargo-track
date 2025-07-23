from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class RouteAssignmentStatus:
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RouteAssignment(BaseModel):
    id: UUID
    route_id: UUID
    vehicle_id: UUID
    driver_id: UUID
    status: str = Field(default=RouteAssignmentStatus.PENDING)
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration_hours: float = Field(..., gt=0)
    actual_duration_hours: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RouteAssignmentCreate(BaseModel):
    route_id: UUID
    vehicle_id: UUID
    driver_id: UUID
    estimated_duration_hours: float = Field(..., gt=0)
    notes: Optional[str] = None


class RouteAssignmentUpdate(BaseModel):
    status: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_duration_hours: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = None 