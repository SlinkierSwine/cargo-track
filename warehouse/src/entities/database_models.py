from sqlalchemy import Column, String, Float, Boolean, DateTime, Text, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class WarehouseModel(Base):
    __tablename__ = "warehouses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    warehouse_type = Column(String(50), nullable=False)
    address = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    total_capacity_weight = Column(Float, nullable=False)
    total_capacity_volume = Column(Float, nullable=False)
    available_capacity_weight = Column(Float, nullable=False)
    available_capacity_volume = Column(Float, nullable=False)
    temperature_controlled = Column(Boolean, default=False)
    hazardous_materials_allowed = Column(Boolean, default=False)
    operating_hours = Column(String(50), default="24/7")
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CargoModel(Base):
    __tablename__ = "cargo"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tracking_number = Column(String(50), nullable=False, unique=True)
    cargo_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    dimensions = Column(JSON, nullable=False)
    value = Column(Float, nullable=False)
    insurance_amount = Column(Float, nullable=False)
    temperature_requirements = Column(JSON, nullable=True)
    humidity_requirements = Column(JSON, nullable=True)
    hazardous_material = Column(Boolean, default=False)
    hazardous_class = Column(String(50), nullable=True)
    special_handling = Column(JSON, default=list)
    fragility_level = Column(String(20), default="low")
    storage_duration = Column(Integer, nullable=False)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="received")
    warehouse_id = Column(String, nullable=True)
    location_in_warehouse = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CompatibilityReportModel(Base):
    __tablename__ = "compatibility_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cargo_id = Column(String, nullable=False)
    vehicle_id = Column(String, nullable=False)
    is_compatible = Column(Boolean, nullable=False)
    score = Column(Float, nullable=False)
    weight_compatible = Column(Boolean, nullable=False)
    volume_compatible = Column(Boolean, nullable=False)
    temperature_compatible = Column(Boolean, nullable=False)
    hazardous_compatible = Column(Boolean, nullable=False)
    special_requirements_met = Column(Boolean, nullable=False)
    risks = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InventoryModel(Base):
    __tablename__ = "inventory"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    warehouse_id = Column(String, nullable=False)
    cargo_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    location = Column(String(100), nullable=False)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    expected_ship_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="received")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) 