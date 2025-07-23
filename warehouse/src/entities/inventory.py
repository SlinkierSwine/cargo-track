from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class InventoryStatus(str, Enum):
    RECEIVED = "received"
    STORED = "stored"
    RESERVED = "reserved"
    LOADING = "loading"
    SHIPPED = "shipped"
    DAMAGED = "damaged"
    LOST = "lost"


class Inventory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    warehouse_id: str
    cargo_id: str
    quantity: int
    location: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    expected_ship_date: Optional[datetime] = None
    status: InventoryStatus = InventoryStatus.RECEIVED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class InventoryCreate(BaseModel):
    warehouse_id: str
    cargo_id: str
    quantity: int
    location: str
    expected_ship_date: Optional[datetime] = None


class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    location: Optional[str] = None
    expected_ship_date: Optional[datetime] = None
    status: Optional[InventoryStatus] = None


class InventoryResponse(BaseModel):
    id: str
    warehouse_id: str
    cargo_id: str
    quantity: int
    location: str
    received_at: datetime
    expected_ship_date: Optional[datetime]
    status: InventoryStatus
    created_at: datetime
    updated_at: datetime


class InventoryTransferRequest(BaseModel):
    cargo_id: str
    from_warehouse_id: str
    to_warehouse_id: str
    quantity: int
    new_location: str


class InventoryTransferResponse(BaseModel):
    transfer_id: str
    cargo_id: str
    from_warehouse_id: str
    to_warehouse_id: str
    quantity: int
    new_location: str
    transferred_at: datetime
    status: str 