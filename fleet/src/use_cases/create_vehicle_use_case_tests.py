import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from entities.vehicle import Vehicle, VehicleType, FuelType, VehicleStatus
from use_cases.create_vehicle_use_case import CreateVehicleUseCase, CreateVehicleRequest


@pytest.fixture
def m_vehicle_repository():
    return MagicMock()


@pytest.fixture
def f_create_vehicle_use_case(m_vehicle_repository):
    return CreateVehicleUseCase(m_vehicle_repository)


@pytest.fixture
def f_valid_vehicle_request():
    return CreateVehicleRequest(
        license_plate="ABC123",
        vehicle_type=VehicleType.TRUCK,
        brand="Volvo",
        model="FH16",
        year=2020,
        capacity_weight=20000.0,
        capacity_volume=80.0,
        fuel_type=FuelType.DIESEL,
        fuel_efficiency=2.5,
        insurance_expiry="2025-12-31T00:00:00",
        registration_expiry="2025-12-31T00:00:00"
    )


def test_create_vehicle_success(f_create_vehicle_use_case, m_vehicle_repository, f_valid_vehicle_request):
    # Mock repository responses
    m_vehicle_repository.get_by_license_plate.return_value = None
    
    mock_vehicle = Vehicle(
        license_plate=f_valid_vehicle_request.license_plate,
        vehicle_type=f_valid_vehicle_request.vehicle_type,
        brand=f_valid_vehicle_request.brand,
        model=f_valid_vehicle_request.model,
        year=f_valid_vehicle_request.year,
        capacity_weight=f_valid_vehicle_request.capacity_weight,
        capacity_volume=f_valid_vehicle_request.capacity_volume,
        fuel_type=f_valid_vehicle_request.fuel_type,
        fuel_efficiency=f_valid_vehicle_request.fuel_efficiency,
        status=VehicleStatus.ACTIVE,
        insurance_expiry=datetime.fromisoformat(f_valid_vehicle_request.insurance_expiry),
        registration_expiry=datetime.fromisoformat(f_valid_vehicle_request.registration_expiry)
    )
    m_vehicle_repository.create.return_value = mock_vehicle
    
    # Execute use case
    result = f_create_vehicle_use_case.execute(f_valid_vehicle_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_license_plate.assert_called_once_with(f_valid_vehicle_request.license_plate)
    m_vehicle_repository.create.assert_called_once()
    
    # Verify result
    assert result.license_plate == mock_vehicle.license_plate
    assert result.vehicle_type == mock_vehicle.vehicle_type
    assert result.brand == mock_vehicle.brand
    assert result.model == mock_vehicle.model
    assert result.year == mock_vehicle.year
    assert result.capacity_weight == mock_vehicle.capacity_weight
    assert result.capacity_volume == mock_vehicle.capacity_volume
    assert result.fuel_type == mock_vehicle.fuel_type
    assert result.fuel_efficiency == mock_vehicle.fuel_efficiency
    assert result.status == mock_vehicle.status


def test_create_vehicle_license_plate_already_exists(f_create_vehicle_use_case, m_vehicle_repository, f_valid_vehicle_request):
    # Mock repository to return existing vehicle
    existing_vehicle = Vehicle(
        license_plate=f_valid_vehicle_request.license_plate,
        vehicle_type=VehicleType.TRUCK,
        brand="Existing",
        model="Truck",
        year=2019,
        capacity_weight=15000.0,
        capacity_volume=60.0,
        fuel_type=FuelType.DIESEL,
        fuel_efficiency=2.0,
        status=VehicleStatus.ACTIVE,
        insurance_expiry=datetime.now() + timedelta(days=365),
        registration_expiry=datetime.now() + timedelta(days=365)
    )
    m_vehicle_repository.get_by_license_plate.return_value = existing_vehicle
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Vehicle with this license plate already exists"):
        f_create_vehicle_use_case.execute(f_valid_vehicle_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_license_plate.assert_called_once_with(f_valid_vehicle_request.license_plate)
    m_vehicle_repository.create.assert_not_called() 