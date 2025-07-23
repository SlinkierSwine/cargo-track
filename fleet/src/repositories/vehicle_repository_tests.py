import pytest
from uuid import uuid4
from datetime import datetime, timedelta

from entities.vehicle import Vehicle, VehicleCreate, VehicleUpdate, VehicleType, FuelType, VehicleStatus
from repositories.vehicle_repository import VehicleRepository


@pytest.fixture
def f_vehicle_create_data():
    return VehicleCreate(
        license_plate="ABC123",
        vehicle_type=VehicleType.TRUCK,
        brand="Volvo",
        model="FH16",
        year=2020,
        capacity_weight=20000.0,
        capacity_volume=80.0,
        fuel_type=FuelType.DIESEL,
        fuel_efficiency=2.5,
        insurance_expiry=datetime.now() + timedelta(days=365),
        registration_expiry=datetime.now() + timedelta(days=365)
    )


@pytest.fixture
def f_vehicle_update_data():
    return VehicleUpdate(
        brand="Scania",
        model="R500",
        capacity_weight=25000.0
    )


def test_create_vehicle(f_vehicle_repository: VehicleRepository, f_vehicle_create_data: VehicleCreate):
    vehicle = f_vehicle_repository.create(f_vehicle_create_data)
    
    assert vehicle.id is not None
    assert vehicle.license_plate == f_vehicle_create_data.license_plate
    assert vehicle.vehicle_type == f_vehicle_create_data.vehicle_type
    assert vehicle.brand == f_vehicle_create_data.brand
    assert vehicle.model == f_vehicle_create_data.model
    assert vehicle.year == f_vehicle_create_data.year
    assert vehicle.capacity_weight == f_vehicle_create_data.capacity_weight
    assert vehicle.capacity_volume == f_vehicle_create_data.capacity_volume
    assert vehicle.fuel_type == f_vehicle_create_data.fuel_type
    assert vehicle.fuel_efficiency == f_vehicle_create_data.fuel_efficiency
    assert vehicle.status == VehicleStatus.ACTIVE


def test_get_by_id(f_vehicle_repository: VehicleRepository, f_vehicle_create_data: VehicleCreate):
    created_vehicle = f_vehicle_repository.create(f_vehicle_create_data)
    vehicle = f_vehicle_repository.get_by_id(str(created_vehicle.id))
    
    assert vehicle is not None
    assert vehicle.id == created_vehicle.id
    assert vehicle.license_plate == created_vehicle.license_plate


def test_get_by_id_not_found(f_vehicle_repository: VehicleRepository):
    vehicle = f_vehicle_repository.get_by_id(str(uuid4()))
    assert vehicle is None


def test_get_by_license_plate(f_vehicle_repository: VehicleRepository, f_vehicle_create_data: VehicleCreate):
    created_vehicle = f_vehicle_repository.create(f_vehicle_create_data)
    vehicle = f_vehicle_repository.get_by_license_plate(created_vehicle.license_plate)
    
    assert vehicle is not None
    assert vehicle.id == created_vehicle.id
    assert vehicle.license_plate == created_vehicle.license_plate


def test_get_by_license_plate_not_found(f_vehicle_repository: VehicleRepository):
    vehicle = f_vehicle_repository.get_by_license_plate("XYZ999")
    assert vehicle is None


def test_update_vehicle(f_vehicle_repository: VehicleRepository, f_vehicle_create_data: VehicleCreate, f_vehicle_update_data: VehicleUpdate):
    created_vehicle = f_vehicle_repository.create(f_vehicle_create_data)
    updated_vehicle = f_vehicle_repository.update(str(created_vehicle.id), f_vehicle_update_data)
    
    assert updated_vehicle is not None
    assert updated_vehicle.id == created_vehicle.id
    assert updated_vehicle.brand == f_vehicle_update_data.brand
    assert updated_vehicle.model == f_vehicle_update_data.model
    assert updated_vehicle.capacity_weight == f_vehicle_update_data.capacity_weight
    assert updated_vehicle.license_plate == created_vehicle.license_plate  # unchanged


def test_update_vehicle_not_found(f_vehicle_repository: VehicleRepository, f_vehicle_update_data: VehicleUpdate):
    vehicle = f_vehicle_repository.update(str(uuid4()), f_vehicle_update_data)
    assert vehicle is None


def test_delete_vehicle(f_vehicle_repository: VehicleRepository, f_vehicle_create_data: VehicleCreate):
    created_vehicle = f_vehicle_repository.create(f_vehicle_create_data)
    deleted = f_vehicle_repository.delete(str(created_vehicle.id))
    
    assert deleted is True
    
    # Verify vehicle is deleted
    vehicle = f_vehicle_repository.get_by_id(str(created_vehicle.id))
    assert vehicle is None


def test_delete_vehicle_not_found(f_vehicle_repository: VehicleRepository):
    deleted = f_vehicle_repository.delete(str(uuid4()))
    assert deleted is False


def test_get_all_vehicles(f_vehicle_repository: VehicleRepository):
    # Create multiple vehicles
    vehicle1_data = VehicleCreate(
        license_plate="ABC123",
        vehicle_type=VehicleType.TRUCK,
        brand="Volvo",
        model="FH16",
        year=2020,
        capacity_weight=20000.0,
        capacity_volume=80.0,
        fuel_type=FuelType.DIESEL,
        fuel_efficiency=2.5,
        insurance_expiry=datetime.now() + timedelta(days=365),
        registration_expiry=datetime.now() + timedelta(days=365)
    )
    
    vehicle2_data = VehicleCreate(
        license_plate="XYZ789",
        vehicle_type=VehicleType.VAN,
        brand="Mercedes",
        model="Sprinter",
        year=2021,
        capacity_weight=5000.0,
        capacity_volume=20.0,
        fuel_type=FuelType.DIESEL,
        fuel_efficiency=3.0,
        insurance_expiry=datetime.now() + timedelta(days=365),
        registration_expiry=datetime.now() + timedelta(days=365)
    )
    
    f_vehicle_repository.create(vehicle1_data)
    f_vehicle_repository.create(vehicle2_data)
    
    vehicles = f_vehicle_repository.get_all()
    assert len(vehicles) >= 2 