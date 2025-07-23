import pytest
from unittest.mock import MagicMock
from datetime import datetime
from pydantic import ValidationError
from entities.warehouse import Warehouse, WarehouseType, WarehouseStatus, WarehouseCreate
from use_cases.create_warehouse_use_case import CreateWarehouseUseCase, CreateWarehouseRequest


@pytest.fixture
def m_warehouse_repository():
    return MagicMock()


@pytest.fixture
def f_create_warehouse_use_case(m_warehouse_repository):
    return CreateWarehouseUseCase(m_warehouse_repository)


@pytest.fixture
def f_valid_warehouse_request():
    return CreateWarehouseRequest(
        name="Main Distribution Center",
        warehouse_type=WarehouseType.DISTRIBUTION_CENTER,
        address="123 Logistics Street",
        city="Moscow",
        country="Russia",
        postal_code="123456",
        phone="+7-495-123-45-67",
        email="warehouse@example.com",
        total_capacity_weight=50000.0,
        total_capacity_volume=2000.0,
        temperature_controlled=True,
        hazardous_materials_allowed=False,
        operating_hours="24/7"
    )


def test_create_warehouse_success(f_create_warehouse_use_case, m_warehouse_repository, f_valid_warehouse_request):
    # Mock repository responses
    m_warehouse_repository.get_by_name.return_value = None
    
    mock_warehouse = Warehouse(
        id="123e4567-e89b-12d3-a456-426614174000",
        name=f_valid_warehouse_request.name,
        warehouse_type=f_valid_warehouse_request.warehouse_type,
        address=f_valid_warehouse_request.address,
        city=f_valid_warehouse_request.city,
        country=f_valid_warehouse_request.country,
        postal_code=f_valid_warehouse_request.postal_code,
        phone=f_valid_warehouse_request.phone,
        email=f_valid_warehouse_request.email,
        total_capacity_weight=f_valid_warehouse_request.total_capacity_weight,
        total_capacity_volume=f_valid_warehouse_request.total_capacity_volume,
        available_capacity_weight=f_valid_warehouse_request.total_capacity_weight,
        available_capacity_volume=f_valid_warehouse_request.total_capacity_volume,
        temperature_controlled=f_valid_warehouse_request.temperature_controlled,
        hazardous_materials_allowed=f_valid_warehouse_request.hazardous_materials_allowed,
        operating_hours=f_valid_warehouse_request.operating_hours,
        status=WarehouseStatus.ACTIVE
    )
    m_warehouse_repository.create.return_value = mock_warehouse
    
    # Execute use case
    result = f_create_warehouse_use_case.execute(f_valid_warehouse_request)
    
    # Verify repository calls
    m_warehouse_repository.get_by_name.assert_called_once_with(f_valid_warehouse_request.name)
    m_warehouse_repository.create.assert_called_once()
    
    # Verify result
    assert result.id == mock_warehouse.id
    assert result.name == mock_warehouse.name
    assert result.warehouse_type == mock_warehouse.warehouse_type
    assert result.address == mock_warehouse.address
    assert result.city == mock_warehouse.city
    assert result.country == mock_warehouse.country
    assert result.postal_code == mock_warehouse.postal_code
    assert result.phone == mock_warehouse.phone
    assert result.email == mock_warehouse.email
    assert result.total_capacity_weight == mock_warehouse.total_capacity_weight
    assert result.total_capacity_volume == mock_warehouse.total_capacity_volume
    assert result.available_capacity_weight == mock_warehouse.available_capacity_weight
    assert result.available_capacity_volume == mock_warehouse.available_capacity_volume
    assert result.temperature_controlled == mock_warehouse.temperature_controlled
    assert result.hazardous_materials_allowed == mock_warehouse.hazardous_materials_allowed
    assert result.operating_hours == mock_warehouse.operating_hours
    assert result.status == mock_warehouse.status


def test_create_warehouse_name_already_exists(f_create_warehouse_use_case, m_warehouse_repository, f_valid_warehouse_request):
    # Mock repository to return existing warehouse
    existing_warehouse = Warehouse(
        id="123e4567-e89b-12d3-a456-426614174000",
        name=f_valid_warehouse_request.name,
        warehouse_type=WarehouseType.STORAGE_FACILITY,
        address="Existing Address",
        city="Existing City",
        country="Russia",
        postal_code="654321",
        phone="+7-495-654-32-10",
        email="existing@example.com",
        total_capacity_weight=30000.0,
        total_capacity_volume=1500.0,
        available_capacity_weight=30000.0,
        available_capacity_volume=1500.0,
        temperature_controlled=False,
        hazardous_materials_allowed=True,
        operating_hours="8/5",
        status=WarehouseStatus.ACTIVE
    )
    m_warehouse_repository.get_by_name.return_value = existing_warehouse
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Warehouse with this name already exists"):
        f_create_warehouse_use_case.execute(f_valid_warehouse_request)
    
    # Verify repository calls
    m_warehouse_repository.get_by_name.assert_called_once_with(f_valid_warehouse_request.name)
    m_warehouse_repository.create.assert_not_called()


def test_create_warehouse_invalid_capacity(f_create_warehouse_use_case, m_warehouse_repository):
    # Create request with invalid capacity - should fail validation
    with pytest.raises(ValidationError):
        invalid_request = CreateWarehouseRequest(
            name="Invalid Warehouse",
            warehouse_type=WarehouseType.GENERAL_WAREHOUSE,
            address="Test Address",
            city="Test City",
            country="Russia",
            postal_code="123456",
            phone="+7-495-123-45-67",
            email="test@example.com",
            total_capacity_weight=-1000.0,  # Invalid negative weight
            total_capacity_volume=500.0,
            temperature_controlled=False,
            hazardous_materials_allowed=False,
            operating_hours="24/7"
        )


def test_create_warehouse_hazardous_materials_without_certification(f_create_warehouse_use_case, m_warehouse_repository):
    # Create request for hazardous materials warehouse without proper setup
    hazardous_request = CreateWarehouseRequest(
        name="Hazardous Warehouse",
        warehouse_type=WarehouseType.HAZARDOUS_MATERIALS,
        address="Hazardous Address",
        city="Hazardous City",
        country="Russia",
        postal_code="123456",
        phone="+7-495-123-45-67",
        email="hazardous@example.com",
        total_capacity_weight=10000.0,
        total_capacity_volume=500.0,
        temperature_controlled=False,
        hazardous_materials_allowed=False,  # Should be True for hazardous warehouse
        operating_hours="24/7"
    )
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Hazardous materials warehouse must allow hazardous materials"):
        f_create_warehouse_use_case.execute(hazardous_request)
    
    # Verify repository calls
    m_warehouse_repository.get_by_name.assert_not_called()
    m_warehouse_repository.create.assert_not_called() 