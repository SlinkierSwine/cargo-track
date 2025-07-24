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


class OrderStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(BaseEntity):
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_email: str = Field(..., min_length=1, max_length=100)
    customer_phone: str = Field(..., min_length=1, max_length=20)
    pickup_address: str = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1)
    cargo_type: str = Field(..., min_length=1, max_length=50)
    cargo_weight: float = Field(..., gt=0)
    cargo_volume: float = Field(..., gt=0)
    status: OrderStatus = OrderStatus.PENDING
    vehicle_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    estimated_cost: Optional[float] = Field(None, gt=0)
    actual_cost: Optional[float] = Field(None, gt=0)
    pickup_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_email: str = Field(..., min_length=1, max_length=100)
    customer_phone: str = Field(..., min_length=1, max_length=20)
    pickup_address: str = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1)
    cargo_type: str = Field(..., min_length=1, max_length=50)
    cargo_weight: float = Field(..., gt=0)
    cargo_volume: float = Field(..., gt=0)
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, min_length=1, max_length=100)
    customer_email: Optional[str] = Field(None, min_length=1, max_length=100)
    customer_phone: Optional[str] = Field(None, min_length=1, max_length=20)
    pickup_address: Optional[str] = Field(None, min_length=1)
    delivery_address: Optional[str] = Field(None, min_length=1)
    cargo_type: Optional[str] = Field(None, min_length=1, max_length=50)
    cargo_weight: Optional[float] = Field(None, gt=0)
    cargo_volume: Optional[float] = Field(None, gt=0)
    status: Optional[OrderStatus] = None
    vehicle_id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    estimated_cost: Optional[float] = Field(None, gt=0)
    actual_cost: Optional[float] = Field(None, gt=0)
    pickup_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: UUID
    customer_name: str
    customer_email: str
    customer_phone: str
    pickup_address: str
    delivery_address: str
    cargo_type: str
    cargo_weight: float
    cargo_volume: float
    status: OrderStatus
    vehicle_id: Optional[UUID]
    driver_id: Optional[UUID]
    estimated_cost: Optional[float]
    actual_cost: Optional[float]
    pickup_date: Optional[datetime]
    delivery_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] 