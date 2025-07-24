from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class BaseEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: datetime
    source_service: str
    data: Dict[str, Any]


class OrderCreatedEvent(BaseEvent):
    event_type: str = "order_created"
    order_id: str
    customer_name: str
    customer_email: str
    pickup_address: str
    delivery_address: str
    cargo_type: str
    cargo_weight: float
    cargo_volume: float
    notes: Optional[str] = None


class VehicleAssignedEvent(BaseEvent):
    event_type: str = "vehicle_assigned"
    order_id: str
    vehicle_id: str
    driver_id: str
    vehicle_license_plate: str
    driver_name: str
    estimated_delivery_time: Optional[datetime] = None


class NoVehicleAvailableEvent(BaseEvent):
    event_type: str = "no_vehicle_available"
    order_id: str
    reason: str  # "no_drivers", "no_vehicles", "capacity_mismatch"


class OrderStatusUpdatedEvent(BaseEvent):
    event_type: str = "order_status_updated"
    order_id: str
    status: str  # "pending", "assigned", "in_transit", "delivered", "cancelled"
    updated_at: datetime 