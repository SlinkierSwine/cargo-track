import pytest
from unittest.mock import MagicMock
from datetime import datetime
from entities.cargo import Cargo, CargoType, FragilityLevel, TemperatureRange
from entities.warehouse import Warehouse, WarehouseType
from entities.compatibility import CompatibilityReport, CompatibilityCheckRequest
from use_cases.check_compatibility_use_case import CheckCompatibilityUseCase


@pytest.fixture
def m_cargo_repository():
    return MagicMock()


@pytest.fixture
def m_warehouse_repository():
    return MagicMock()


@pytest.fixture
def m_fleet_service():
    return MagicMock()


@pytest.fixture
def f_check_compatibility_use_case(m_cargo_repository, m_warehouse_repository, m_fleet_service):
    return CheckCompatibilityUseCase(m_cargo_repository, m_warehouse_repository, m_fleet_service)


@pytest.fixture
def f_sample_cargo():
    return Cargo(
        id="cargo-123",
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
        hazardous_material=False,
        special_handling=["fragile", "upright"],
        fragility_level=FragilityLevel.HIGH,
        storage_duration=30
    )


@pytest.fixture
def f_sample_vehicle():
    return {
        "id": "vehicle-456",
        "license_plate": "ABC123",
        "vehicle_type": "TRUCK",
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "temperature_controlled": True,
        "hazardous_materials_certified": False,
        "special_equipment": ["refrigeration", "loading_ramp"]
    }


@pytest.fixture
def f_valid_compatibility_request():
    return CompatibilityCheckRequest(
        cargo_id="cargo-123",
        vehicle_id="vehicle-456"
    )


def test_check_compatibility_success(f_check_compatibility_use_case, m_cargo_repository, 
                                   m_warehouse_repository, m_fleet_service, 
                                   f_sample_cargo, f_sample_vehicle, f_valid_compatibility_request):
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = f_sample_cargo
    m_fleet_service.get_vehicle.return_value = f_sample_vehicle
    
    # Execute use case
    result = f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_id.assert_called_once_with(f_valid_compatibility_request.cargo_id)
    m_fleet_service.get_vehicle.assert_called_once_with(f_valid_compatibility_request.vehicle_id)
    
    # Verify result
    assert result.cargo_id == f_valid_compatibility_request.cargo_id
    assert result.vehicle_id == f_valid_compatibility_request.vehicle_id
    assert result.is_compatible is True
    assert result.score > 0.8  # High compatibility score
    assert result.weight_compatible is True
    assert result.volume_compatible is True
    assert result.temperature_compatible is True
    assert result.hazardous_compatible is True
    assert result.special_requirements_met is True
    assert len(result.risks) == 0
    assert len(result.recommendations) > 0


def test_check_compatibility_cargo_not_found(f_check_compatibility_use_case, m_cargo_repository, 
                                           m_warehouse_repository, m_fleet_service, 
                                           f_valid_compatibility_request):
    # Mock repository to return None for cargo
    m_cargo_repository.get_by_id.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Cargo not found"):
        f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_id.assert_called_once_with(f_valid_compatibility_request.cargo_id)
    m_fleet_service.get_vehicle.assert_not_called()


def test_check_compatibility_vehicle_not_found(f_check_compatibility_use_case, m_cargo_repository, 
                                             m_warehouse_repository, m_fleet_service, 
                                             f_sample_cargo, f_valid_compatibility_request):
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = f_sample_cargo
    m_fleet_service.get_vehicle.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Vehicle not found"):
        f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify repository calls
    m_cargo_repository.get_by_id.assert_called_once_with(f_valid_compatibility_request.cargo_id)
    m_fleet_service.get_vehicle.assert_called_once_with(f_valid_compatibility_request.vehicle_id)


def test_check_compatibility_weight_exceeds_capacity(f_check_compatibility_use_case, m_cargo_repository, 
                                                   m_warehouse_repository, m_fleet_service, 
                                                   f_valid_compatibility_request):
    # Create heavy cargo
    heavy_cargo = Cargo(
        id="cargo-123",
        tracking_number="CARGO-2024-001",
        cargo_type=CargoType.GENERAL,
        name="Heavy Equipment",
        description="Very heavy equipment",
        weight=25000.0,  # Exceeds vehicle capacity
        volume=10.0,
        dimensions={"length": 3.0, "width": 2.0, "height": 2.0},
        value=50000.0,
        insurance_amount=55000.0,
        hazardous_material=False,
        special_handling=[],
        fragility_level=FragilityLevel.LOW,
        storage_duration=30
    )
    
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = heavy_cargo
    m_fleet_service.get_vehicle.return_value = {
        "id": "vehicle-456",
        "license_plate": "ABC123",
        "vehicle_type": "TRUCK",
        "capacity_weight": 20000.0,  # Less than cargo weight
        "capacity_volume": 80.0,
        "temperature_controlled": False,
        "hazardous_materials_certified": False,
        "special_equipment": []
    }
    
    # Execute use case
    result = f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify result
    assert result.is_compatible is False
    assert result.weight_compatible is False
    assert result.score < 0.5  # Low compatibility score
    assert "Weight exceeds vehicle capacity" in result.risks


def test_check_compatibility_hazardous_materials_not_certified(f_check_compatibility_use_case, m_cargo_repository, 
                                                             m_warehouse_repository, m_fleet_service, 
                                                             f_valid_compatibility_request):
    # Create hazardous cargo
    hazardous_cargo = Cargo(
        id="cargo-123",
        tracking_number="CARGO-2024-001",
        cargo_type=CargoType.HAZARDOUS,
        name="Hazardous Materials",
        description="Dangerous goods",
        weight=500.0,
        volume=2.5,
        dimensions={"length": 1.5, "width": 1.0, "height": 1.0},
        value=5000.0,
        insurance_amount=5500.0,
        hazardous_material=True,
        hazardous_class="Class 3",
        special_handling=["hazardous"],
        fragility_level=FragilityLevel.MEDIUM,
        storage_duration=15
    )
    
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = hazardous_cargo
    m_fleet_service.get_vehicle.return_value = {
        "id": "vehicle-456",
        "license_plate": "ABC123",
        "vehicle_type": "TRUCK",
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "temperature_controlled": False,
        "hazardous_materials_certified": False,  # Not certified for hazardous materials
        "special_equipment": []
    }
    
    # Execute use case
    result = f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify result
    assert result.is_compatible is False
    assert result.hazardous_compatible is False
    assert result.score < 0.5  # Low compatibility score
    assert "Vehicle not certified for hazardous materials" in result.risks


def test_check_compatibility_temperature_requirements_not_met(f_check_compatibility_use_case, m_cargo_repository, 
                                                            m_warehouse_repository, m_fleet_service, 
                                                            f_valid_compatibility_request):
    # Create temperature-sensitive cargo
    temp_cargo = Cargo(
        id="cargo-123",
        tracking_number="CARGO-2024-001",
        cargo_type=CargoType.REFRIGERATED,
        name="Frozen Food",
        description="Temperature-sensitive food items",
        weight=500.0,
        volume=2.5,
        dimensions={"length": 1.5, "width": 1.0, "height": 1.0},
        value=5000.0,
        insurance_amount=5500.0,
        temperature_requirements=TemperatureRange(min_temp=-20.0, max_temp=-10.0),
        hazardous_material=False,
        special_handling=["frozen"],
        fragility_level=FragilityLevel.MEDIUM,
        storage_duration=7
    )
    
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = temp_cargo
    m_fleet_service.get_vehicle.return_value = {
        "id": "vehicle-456",
        "license_plate": "ABC123",
        "vehicle_type": "TRUCK",
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "temperature_controlled": False,  # No temperature control
        "hazardous_materials_certified": False,
        "special_equipment": []
    }
    
    # Execute use case
    result = f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify result
    assert result.is_compatible is False
    assert result.temperature_compatible is False
    assert result.score < 0.5  # Low compatibility score
    assert "Vehicle does not support temperature requirements" in result.risks


def test_check_compatibility_special_requirements_not_met(f_check_compatibility_use_case, m_cargo_repository, 
                                                        m_warehouse_repository, m_fleet_service, 
                                                        f_valid_compatibility_request):
    # Create cargo with special handling requirements
    special_cargo = Cargo(
        id="cargo-123",
        tracking_number="CARGO-2024-001",
        cargo_type=CargoType.FRAGILE,
        name="Glass Items",
        description="Fragile glass items",
        weight=100.0,
        volume=1.0,
        dimensions={"length": 1.0, "width": 1.0, "height": 1.0},
        value=10000.0,
        insurance_amount=11000.0,
        hazardous_material=False,
        special_handling=["fragile", "upright", "shock_absorbing"],
        fragility_level=FragilityLevel.EXTREME,
        storage_duration=30
    )
    
    # Mock repository responses
    m_cargo_repository.get_by_id.return_value = special_cargo
    m_fleet_service.get_vehicle.return_value = {
        "id": "vehicle-456",
        "license_plate": "ABC123",
        "vehicle_type": "TRUCK",
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "temperature_controlled": False,
        "hazardous_materials_certified": False,
        "special_equipment": []  # No special equipment
    }
    
    # Execute use case
    result = f_check_compatibility_use_case.execute(f_valid_compatibility_request)
    
    # Verify result
    assert result.is_compatible is False
    assert result.special_requirements_met is False
    assert result.score < 0.7  # Lower compatibility score
    assert "Special handling requirements not met" in result.risks 