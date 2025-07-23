import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm import Session
from entities.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate, WarehouseType, WarehouseStatus
from entities.database_models import WarehouseModel
from repositories.warehouse_repository import WarehouseRepository


@pytest.fixture
def m_session():
    return MagicMock(spec=Session)


@pytest.fixture
def f_warehouse_repository(m_session):
    return WarehouseRepository(m_session)


@pytest.fixture
def f_warehouse_create_data():
    return WarehouseCreate(
        name="Test Warehouse",
        warehouse_type=WarehouseType.DISTRIBUTION_CENTER,
        address="123 Test Street",
        city="Test City",
        country="Test Country",
        postal_code="12345",
        phone="+1-234-567-8900",
        email="test@warehouse.com",
        total_capacity_weight=10000.0,
        total_capacity_volume=500.0,
        temperature_controlled=True,
        hazardous_materials_allowed=False,
        operating_hours="24/7"
    )


@pytest.fixture
def f_db_warehouse_model():
    return WarehouseModel(
        id="warehouse-123",
        name="Test Warehouse",
        warehouse_type="distribution_center",
        address="123 Test Street",
        city="Test City",
        country="Test Country",
        postal_code="12345",
        phone="+1-234-567-8900",
        email="test@warehouse.com",
        total_capacity_weight=10000.0,
        total_capacity_volume=500.0,
        available_capacity_weight=10000.0,
        available_capacity_volume=500.0,
        temperature_controlled=True,
        hazardous_materials_allowed=False,
        operating_hours="24/7",
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_create_warehouse_success(f_warehouse_repository, m_session, f_warehouse_create_data, f_db_warehouse_model):
    # Mock session behavior
    m_session.add.return_value = None
    m_session.commit.return_value = None
    m_session.refresh.return_value = None
    
    # Mock the created object to have proper values
    created_warehouse = WarehouseModel(
        id="warehouse-123",
        name=f_warehouse_create_data.name,
        warehouse_type=f_warehouse_create_data.warehouse_type.value,
        address=f_warehouse_create_data.address,
        city=f_warehouse_create_data.city,
        country=f_warehouse_create_data.country,
        postal_code=f_warehouse_create_data.postal_code,
        phone=f_warehouse_create_data.phone,
        email=f_warehouse_create_data.email,
        total_capacity_weight=f_warehouse_create_data.total_capacity_weight,
        total_capacity_volume=f_warehouse_create_data.total_capacity_volume,
        available_capacity_weight=f_warehouse_create_data.total_capacity_weight,
        available_capacity_volume=f_warehouse_create_data.total_capacity_volume,
        temperature_controlled=f_warehouse_create_data.temperature_controlled,
        hazardous_materials_allowed=f_warehouse_create_data.hazardous_materials_allowed,
        operating_hours=f_warehouse_create_data.operating_hours,
        status=WarehouseStatus.ACTIVE.value,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Mock refresh to set the created object
    def mock_refresh(obj):
        obj.id = created_warehouse.id
        obj.created_at = created_warehouse.created_at
        obj.updated_at = created_warehouse.updated_at
    
    m_session.refresh.side_effect = mock_refresh
    
    # Execute repository method
    result = f_warehouse_repository.create(f_warehouse_create_data)
    
    # Verify session calls
    m_session.add.assert_called_once()
    m_session.commit.assert_called_once()
    m_session.refresh.assert_called_once()
    
    # Verify result
    assert result.name == f_warehouse_create_data.name
    assert result.warehouse_type == f_warehouse_create_data.warehouse_type
    assert result.address == f_warehouse_create_data.address
    assert result.city == f_warehouse_create_data.city
    assert result.country == f_warehouse_create_data.country
    assert result.postal_code == f_warehouse_create_data.postal_code
    assert result.phone == f_warehouse_create_data.phone
    assert result.email == f_warehouse_create_data.email
    assert result.total_capacity_weight == f_warehouse_create_data.total_capacity_weight
    assert result.total_capacity_volume == f_warehouse_create_data.total_capacity_volume
    assert result.available_capacity_weight == f_warehouse_create_data.total_capacity_weight
    assert result.available_capacity_volume == f_warehouse_create_data.total_capacity_volume
    assert result.temperature_controlled == f_warehouse_create_data.temperature_controlled
    assert result.hazardous_materials_allowed == f_warehouse_create_data.hazardous_materials_allowed
    assert result.operating_hours == f_warehouse_create_data.operating_hours
    assert result.status == WarehouseStatus.ACTIVE


def test_get_by_id_success(f_warehouse_repository, m_session, f_db_warehouse_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_warehouse_model
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.get_by_id("warehouse-123")
    
    # Verify result
    assert result is not None
    assert result.id == f_db_warehouse_model.id
    assert result.name == f_db_warehouse_model.name
    assert result.warehouse_type == WarehouseType(f_db_warehouse_model.warehouse_type)
    assert result.status == WarehouseStatus(f_db_warehouse_model.status)


def test_get_by_id_not_found(f_warehouse_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.get_by_id("nonexistent-id")
    
    # Verify result
    assert result is None


def test_get_by_name_success(f_warehouse_repository, m_session, f_db_warehouse_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_warehouse_model
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.get_by_name("Test Warehouse")
    
    # Verify result
    assert result is not None
    assert result.name == f_db_warehouse_model.name
    assert result.warehouse_type == WarehouseType(f_db_warehouse_model.warehouse_type)


def test_get_by_name_not_found(f_warehouse_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.get_by_name("Nonexistent Warehouse")
    
    # Verify result
    assert result is None


def test_get_all_success(f_warehouse_repository, m_session, f_db_warehouse_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [f_db_warehouse_model]
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.get_all(skip=0, limit=10)
    
    # Verify result
    assert len(result) == 1
    assert result[0].id == f_db_warehouse_model.id
    assert result[0].name == f_db_warehouse_model.name


def test_update_warehouse_success(f_warehouse_repository, m_session, f_db_warehouse_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_warehouse_model
    m_session.query.return_value = mock_query
    m_session.commit.return_value = None
    m_session.refresh.return_value = None
    
    # Create update data
    update_data = WarehouseUpdate(
        name="Updated Warehouse",
        city="Updated City"
    )
    
    # Execute repository method
    result = f_warehouse_repository.update("warehouse-123", update_data)
    
    # Verify session calls
    m_session.commit.assert_called_once()
    m_session.refresh.assert_called_once()
    
    # Verify result
    assert result is not None
    assert result.name == "Updated Warehouse"
    assert result.city == "Updated City"


def test_update_warehouse_not_found(f_warehouse_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Create update data
    update_data = WarehouseUpdate(name="Updated Warehouse")
    
    # Execute repository method
    result = f_warehouse_repository.update("nonexistent-id", update_data)
    
    # Verify result
    assert result is None
    m_session.commit.assert_not_called()


def test_delete_warehouse_success(f_warehouse_repository, m_session, f_db_warehouse_model):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_warehouse_model
    m_session.query.return_value = mock_query
    m_session.delete.return_value = None
    m_session.commit.return_value = None
    
    # Execute repository method
    result = f_warehouse_repository.delete("warehouse-123")
    
    # Verify session calls
    m_session.delete.assert_called_once_with(f_db_warehouse_model)
    m_session.commit.assert_called_once()
    
    # Verify result
    assert result is True


def test_delete_warehouse_not_found(f_warehouse_repository, m_session):
    # Mock query result
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_session.query.return_value = mock_query
    
    # Execute repository method
    result = f_warehouse_repository.delete("nonexistent-id")
    
    # Verify result
    assert result is False
    m_session.delete.assert_not_called()
    m_session.commit.assert_not_called() 