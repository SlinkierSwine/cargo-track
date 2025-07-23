import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm import Session
from entities.cargo import Cargo, CargoCreate, CargoUpdate, CargoType, CargoStatus
from entities.database_models import CargoModel
from repositories.cargo_repository import CargoRepository


@pytest.fixture
def m_session():
    return MagicMock(spec=Session)


@pytest.fixture
def f_cargo_repository(m_session):
    return CargoRepository(m_session)


@pytest.fixture
def f_cargo_create_data():
    return CargoCreate(
        tracking_number="TRK123456",
        cargo_type=CargoType.GENERAL,
        name="Test Cargo",
        description="Test cargo description",
        weight=100.0,
        volume=10.0,
        dimensions={"length": 100, "width": 50, "height": 30},
        value=5000.0,
        insurance_amount=5500.0,
        temperature_requirements=None,
        humidity_requirements=None,
        hazardous_material=False,
        hazardous_class=None,
        special_handling=[],
        fragility_level="low",
        storage_duration=30,
        expiration_date=None
    )


@pytest.fixture
def f_db_cargo_model():
    return CargoModel(
        id="cargo-123",
        tracking_number="TRK123456",
        cargo_type="general",
        name="Test Cargo",
        description="Test cargo description",
        weight=100.0,
        volume=10.0,
        dimensions={"length": 100, "width": 50, "height": 30},
        value=5000.0,
        insurance_amount=5500.0,
        temperature_requirements=None,
        humidity_requirements=None,
        hazardous_material=False,
        hazardous_class=None,
        special_handling=[],
        fragility_level="low",
        storage_duration=30,
        expiration_date=None,
        status="received",
        warehouse_id="warehouse-123",
        location_in_warehouse="A1-B2",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_create_cargo_success(f_cargo_repository, m_session, f_cargo_create_data):
    # Mock session behavior
    m_session.add.return_value = None
    m_session.commit.return_value = None
    m_session.refresh.return_value = None
    
    # Mock the created object to have proper values
    created_cargo = CargoModel(
        id="cargo-123",
        tracking_number=f_cargo_create_data.tracking_number,
        cargo_type=f_cargo_create_data.cargo_type.value,
        name=f_cargo_create_data.name,
        description=f_cargo_create_data.description,
        weight=f_cargo_create_data.weight,
        volume=f_cargo_create_data.volume,
        dimensions=f_cargo_create_data.dimensions,
        value=f_cargo_create_data.value,
        insurance_amount=f_cargo_create_data.insurance_amount,
        temperature_requirements=f_cargo_create_data.temperature_requirements,
        humidity_requirements=f_cargo_create_data.humidity_requirements,
        hazardous_material=f_cargo_create_data.hazardous_material,
        hazardous_class=f_cargo_create_data.hazardous_class,
        special_handling=f_cargo_create_data.special_handling,
        fragility_level=f_cargo_create_data.fragility_level,
        storage_duration=f_cargo_create_data.storage_duration,
        expiration_date=f_cargo_create_data.expiration_date,
        status=CargoStatus.RECEIVED.value,
        warehouse_id=None,
        location_in_warehouse=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Mock refresh to set the created object
    def mock_refresh(obj):
        obj.id = created_cargo.id
        obj.created_at = created_cargo.created_at
        obj.updated_at = created_cargo.updated_at
    
    m_session.refresh.side_effect = mock_refresh
    
    # Execute repository method
    result = f_cargo_repository.create(f_cargo_create_data)
    
    # Verify session calls
    m_session.add.assert_called_once()
    m_session.commit.assert_called_once()
    m_session.refresh.assert_called_once()
    
    # Verify result
    assert result.tracking_number == f_cargo_create_data.tracking_number
    assert result.cargo_type == f_cargo_create_data.cargo_type
    assert result.name == f_cargo_create_data.name
    assert result.description == f_cargo_create_data.description
    assert result.weight == f_cargo_create_data.weight
    assert result.volume == f_cargo_create_data.volume
    assert result.dimensions == f_cargo_create_data.dimensions
    assert result.value == f_cargo_create_data.value
    assert result.insurance_amount == f_cargo_create_data.insurance_amount
    assert result.hazardous_material == f_cargo_create_data.hazardous_material
    assert result.fragility_level == f_cargo_create_data.fragility_level
    assert result.storage_duration == f_cargo_create_data.storage_duration
    assert result.warehouse_id is None
    assert result.location_in_warehouse is None
    assert result.status == CargoStatus.RECEIVED


def test_get_by_id_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_cargo_model
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_by_id("cargo-123")
    
    # Verify result
    assert result is not None
    assert result.id == f_db_cargo_model.id
    assert result.tracking_number == f_db_cargo_model.tracking_number
    assert result.cargo_type == CargoType(f_db_cargo_model.cargo_type)
    assert result.status == CargoStatus(f_db_cargo_model.status)


def test_get_by_id_not_found(f_cargo_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_by_id("nonexistent-id")
    
    # Verify result
    assert result is None


def test_get_by_tracking_number_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_cargo_model
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_by_tracking_number("TRK123456")
    
    # Verify result
    assert result is not None
    assert result.tracking_number == f_db_cargo_model.tracking_number
    assert result.cargo_type == CargoType(f_db_cargo_model.cargo_type)


def test_get_by_tracking_number_not_found(f_cargo_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_by_tracking_number("TRK999999")
    
    # Verify result
    assert result is None


def test_get_all_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [f_db_cargo_model]
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_all(skip=0, limit=10)
    
    # Verify result
    assert len(result) == 1
    assert result[0].id == f_db_cargo_model.id
    assert result[0].tracking_number == f_db_cargo_model.tracking_number


def test_get_by_warehouse_id_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [f_db_cargo_model]
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.get_by_warehouse_id("warehouse-123")
    
    # Verify result
    assert len(result) == 1
    assert result[0].warehouse_id == f_db_cargo_model.warehouse_id
    assert result[0].tracking_number == f_db_cargo_model.tracking_number


def test_update_cargo_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_cargo_model
    m_session.query.return_value = mock_query
    m_session.commit.return_value = None
    m_session.refresh.return_value = None
    
    # Create update data
    update_data = CargoUpdate(
        name="Updated Cargo",
        description="Updated description"
    )
    
    # Execute repository method
    result = f_cargo_repository.update("cargo-123", update_data)
    
    # Verify session calls
    m_session.commit.assert_called_once()
    m_session.refresh.assert_called_once()
    
    # Verify result
    assert result is not None
    assert result.name == "Updated Cargo"
    assert result.description == "Updated description"


def test_update_cargo_not_found(f_cargo_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Create update data
    update_data = CargoUpdate(name="Updated Cargo")
    
    # Execute repository method
    result = f_cargo_repository.update("nonexistent-id", update_data)
    
    # Verify result
    assert result is None
    m_session.commit.assert_not_called()


def test_delete_cargo_success(f_cargo_repository, m_session, f_db_cargo_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_cargo_model
    m_session.query.return_value = mock_query
    m_session.delete.return_value = None
    m_session.commit.return_value = None
    
    # Execute repository method
    result = f_cargo_repository.delete("cargo-123")
    
    # Verify session calls
    m_session.delete.assert_called_once_with(f_db_cargo_model)
    m_session.commit.assert_called_once()
    
    # Verify result
    assert result is True


def test_delete_cargo_not_found(f_cargo_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_cargo_repository.delete("nonexistent-id")
    
    # Verify result
    assert result is False
    m_session.delete.assert_not_called()
    m_session.commit.assert_not_called() 