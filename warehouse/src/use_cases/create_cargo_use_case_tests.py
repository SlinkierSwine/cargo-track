import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from pydantic import ValidationError
from entities.cargo import Cargo, CargoType, CargoStatus, FragilityLevel, TemperatureRange, HumidityRange
from use_cases.create_cargo_use_case import CreateCargoUseCase, CreateCargoRequest


@pytest.fixture
def m_cargo_repository():
    return MagicMock()


@pytest.fixture
def f_create_cargo_use_case(m_cargo_repository):
    return CreateCargoUseCase(m_cargo_repository)


@pytest.fixture
def f_valid_cargo_request():
    return CreateCargoRequest(
        tracking_number="CARGO-2024-001",
        cargo_type=CargoType.GENERAL,
        name="Electronics Package",
        description="Fragile electronics equipment",
        weight=500.0,
        volume=2.5,
        dimensions={"length": 1.5, "width": 1.0, "height": 1.0},
        value=5000.0,
        insurance_amount=5500.0,
        temperature_requirements=TemperatureRange(min_temp=15.0, max_temp=25.0),
        humidity_requirements=HumidityRange(min_humidity=30.0, max_humidity=60.0),
        hazardous_material=False,
        special_handling=["fragile", "upright"],
        fragility_level=FragilityLevel.HIGH,
        storage_duration=30,
        expiration_date=datetime.utcnow() + timedelta(days=90)
    )


def test_create_cargo_success(f_create_cargo_use_case, m_cargo_repository, f_valid_cargo_request):
    # Mock repository responses
    m_cargo_repository.get_by_tracking_number.return_value = None
    
    mock_cargo = Cargo(
        id="123e4567-e89b-12d3-a456-426614174000",
        tracking_number=f_valid_cargo_request.tracking_number,
        cargo_type=f_valid_cargo_request.cargo_type,
        name=f_valid_cargo_request.name,
        description=f_valid_cargo_request.description,
        weight=f_valid_cargo_request.weight,
        volume=f_valid_cargo_request.volume,
        dimensions=f_valid_cargo_request.dimensions,
        value=f_valid_cargo_request.value,
        insurance_amount=f_valid_cargo_request.insurance_amount,
        temperature_requirements=f_valid_cargo_request.temperature_requirements,
        humidity_requirements=f_valid_cargo_request.humidity_requirements,
        hazardous_material=f_valid_cargo_request.hazardous_material,
        special_handling=f_valid_cargo_request.special_handling,
        fragility_level=f_valid_cargo_request.fragility_level,
        storage_duration=f_valid_cargo_request.storage_duration,
        expiration_date=f_valid_cargo_request.expiration_date,
        status=CargoStatus.RECEIVED
    )
    m_cargo_repository.create.return_value = mock_cargo
    
    # Execute use case
    result = f_create_cargo_use_case.execute(f_valid_cargo_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_tracking_number.assert_called_once_with(f_valid_cargo_request.tracking_number)
    m_cargo_repository.create.assert_called_once()
    
    # Verify result
    assert result.id == mock_cargo.id
    assert result.tracking_number == mock_cargo.tracking_number
    assert result.cargo_type == mock_cargo.cargo_type
    assert result.name == mock_cargo.name
    assert result.description == mock_cargo.description
    assert result.weight == mock_cargo.weight
    assert result.volume == mock_cargo.volume
    assert result.dimensions == mock_cargo.dimensions
    assert result.value == mock_cargo.value
    assert result.insurance_amount == mock_cargo.insurance_amount
    assert result.temperature_requirements == mock_cargo.temperature_requirements
    assert result.humidity_requirements == mock_cargo.humidity_requirements
    assert result.hazardous_material == mock_cargo.hazardous_material
    assert result.special_handling == mock_cargo.special_handling
    assert result.fragility_level == mock_cargo.fragility_level
    assert result.storage_duration == mock_cargo.storage_duration
    assert result.expiration_date == mock_cargo.expiration_date
    assert result.status == mock_cargo.status


def test_create_cargo_tracking_number_already_exists(f_create_cargo_use_case, m_cargo_repository, f_valid_cargo_request):
    # Mock repository to return existing cargo
    existing_cargo = Cargo(
        id="123e4567-e89b-12d3-a456-426614174000",
        tracking_number=f_valid_cargo_request.tracking_number,
        cargo_type=CargoType.GENERAL,
        name="Existing Cargo",
        description="Existing description",
        weight=300.0,
        volume=1.5,
        dimensions={"length": 1.0, "width": 0.8, "height": 0.8},
        value=2000.0,
        insurance_amount=2200.0,
        hazardous_material=False,
        special_handling=[],
        fragility_level=FragilityLevel.LOW,
        storage_duration=15,
        status=CargoStatus.STORED
    )
    m_cargo_repository.get_by_tracking_number.return_value = existing_cargo
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Cargo with this tracking number already exists"):
        f_create_cargo_use_case.execute(f_valid_cargo_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_tracking_number.assert_called_once_with(f_valid_cargo_request.tracking_number)
    m_cargo_repository.create.assert_not_called()


def test_create_cargo_invalid_weight(f_create_cargo_use_case, m_cargo_repository):
    # Create request with invalid weight - should fail validation
    with pytest.raises(ValidationError):
        invalid_request = CreateCargoRequest(
            tracking_number="CARGO-2024-002",
            cargo_type=CargoType.GENERAL,
            name="Invalid Cargo",
            description="Invalid cargo",
            weight=-100.0,  # Invalid negative weight
            volume=1.0,
            dimensions={"length": 1.0, "width": 1.0, "height": 1.0},
            value=1000.0,
            insurance_amount=1100.0,
            hazardous_material=False,
            special_handling=[],
            fragility_level=FragilityLevel.LOW,
            storage_duration=30
        )


def test_create_hazardous_cargo_without_classification(f_create_cargo_use_case, m_cargo_repository):
    # Create request for hazardous cargo without proper classification
    hazardous_request = CreateCargoRequest(
        tracking_number="CARGO-2024-003",
        cargo_type=CargoType.HAZARDOUS,
        name="Hazardous Cargo",
        description="Hazardous materials",
        weight=200.0,
        volume=1.0,
        dimensions={"length": 1.0, "width": 1.0, "height": 1.0},
        value=5000.0,
        insurance_amount=6000.0,
        hazardous_material=True,
        hazardous_class=None,  # Should be specified for hazardous cargo
        special_handling=["hazardous"],
        fragility_level=FragilityLevel.MEDIUM,
        storage_duration=15
    )
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Hazardous class must be specified for hazardous materials"):
        f_create_cargo_use_case.execute(hazardous_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_tracking_number.assert_not_called()
    m_cargo_repository.create.assert_not_called()


def test_create_cargo_invalid_dimensions(f_create_cargo_use_case, m_cargo_repository):
    # Create request with invalid dimensions
    invalid_request = CreateCargoRequest(
        tracking_number="CARGO-2024-004",
        cargo_type=CargoType.GENERAL,
        name="Invalid Dimensions Cargo",
        description="Cargo with invalid dimensions",
        weight=100.0,
        volume=1.0,
        dimensions={"length": -1.0, "width": 1.0, "height": 1.0},  # Invalid negative length
        value=1000.0,
        insurance_amount=1100.0,
        hazardous_material=False,
        special_handling=[],
        fragility_level=FragilityLevel.LOW,
        storage_duration=30
    )
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="All dimensions must be positive"):
        f_create_cargo_use_case.execute(invalid_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_tracking_number.assert_not_called()
    m_cargo_repository.create.assert_not_called() 