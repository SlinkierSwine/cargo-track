import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from entities.route_assignment import RouteAssignment, RouteAssignmentCreate, RouteAssignmentUpdate, RouteAssignmentStatus
from entities.database_models import RouteAssignment as RouteAssignmentModel
from repositories.route_assignment_repository import RouteAssignmentRepository


@pytest.fixture
def m_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def f_route_assignment_repository(m_db_session):
    return RouteAssignmentRepository(m_db_session)


@pytest.fixture
def f_route_assignment_create():
    return RouteAssignmentCreate(
        route_id=uuid4(),
        vehicle_id=uuid4(),
        driver_id=uuid4(),
        estimated_duration_hours=8.5,
        notes="Test assignment"
    )


@pytest.fixture
def f_route_assignment_update():
    return RouteAssignmentUpdate(
        status=RouteAssignmentStatus.IN_PROGRESS,
        started_at=datetime.now(),
        notes="Updated notes"
    )


@pytest.fixture
def f_db_route_assignment():
    assignment_id = uuid4()
    route_id = uuid4()
    vehicle_id = uuid4()
    driver_id = uuid4()
    current_time = datetime.now()
    
    db_assignment = MagicMock(spec=RouteAssignmentModel)
    db_assignment.id = assignment_id
    db_assignment.route_id = route_id
    db_assignment.vehicle_id = vehicle_id
    db_assignment.driver_id = driver_id
    db_assignment.status = "pending"
    db_assignment.assigned_at = None
    db_assignment.started_at = None
    db_assignment.completed_at = None
    db_assignment.estimated_duration_hours = 8.5
    db_assignment.actual_duration_hours = None
    db_assignment.notes = "Test assignment"
    db_assignment.created_at = current_time
    db_assignment.updated_at = current_time
    
    return db_assignment


def test_create_route_assignment_success(f_route_assignment_repository, m_db_session, f_route_assignment_create):
    # Mock database session
    m_db_session.add.return_value = None
    m_db_session.commit.return_value = None
    m_db_session.refresh.return_value = None
    
    # Mock the created assignment
    assignment_id = uuid4()
    current_time = datetime.now()
    mock_assignment = MagicMock(spec=RouteAssignmentModel)
    mock_assignment.id = assignment_id
    mock_assignment.route_id = f_route_assignment_create.route_id
    mock_assignment.vehicle_id = f_route_assignment_create.vehicle_id
    mock_assignment.driver_id = f_route_assignment_create.driver_id
    mock_assignment.status = "pending"
    mock_assignment.assigned_at = None
    mock_assignment.started_at = None
    mock_assignment.completed_at = None
    mock_assignment.estimated_duration_hours = f_route_assignment_create.estimated_duration_hours
    mock_assignment.actual_duration_hours = None
    mock_assignment.notes = f_route_assignment_create.notes
    mock_assignment.created_at = current_time
    mock_assignment.updated_at = current_time
    
    # Mock the query result
    m_db_session.add.side_effect = lambda x: setattr(x, 'id', assignment_id)
    m_db_session.refresh.side_effect = lambda x: setattr(x, 'status', 'pending') or setattr(x, 'created_at', current_time) or setattr(x, 'updated_at', current_time)
    
    # Execute
    result = f_route_assignment_repository.create(f_route_assignment_create)
    
    # Verify
    assert result.id == assignment_id
    assert result.route_id == f_route_assignment_create.route_id
    assert result.vehicle_id == f_route_assignment_create.vehicle_id
    assert result.driver_id == f_route_assignment_create.driver_id
    assert result.status == "pending"
    assert result.estimated_duration_hours == f_route_assignment_create.estimated_duration_hours
    assert result.notes == f_route_assignment_create.notes
    
    m_db_session.add.assert_called_once()
    m_db_session.commit.assert_called_once()
    m_db_session.refresh.assert_called_once()


def test_get_by_id_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_route_assignment
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_id(f_db_route_assignment.id)
    
    # Verify
    assert result is not None
    assert result.id == f_db_route_assignment.id
    assert result.route_id == f_db_route_assignment.route_id
    assert result.vehicle_id == f_db_route_assignment.vehicle_id
    assert result.driver_id == f_db_route_assignment.driver_id
    assert result.status == f_db_route_assignment.status
    assert result.estimated_duration_hours == f_db_route_assignment.estimated_duration_hours
    assert result.notes == f_db_route_assignment.notes
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()


def test_get_by_id_not_found(f_route_assignment_repository, m_db_session):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_id(uuid4())
    
    # Verify
    assert result is None
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()


def test_get_by_route_id_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [f_db_route_assignment]
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_route_id(f_db_route_assignment.route_id)
    
    # Verify
    assert len(result) == 1
    assert result[0].id == f_db_route_assignment.id
    assert result[0].route_id == f_db_route_assignment.route_id
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_by_vehicle_id_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [f_db_route_assignment]
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_vehicle_id(f_db_route_assignment.vehicle_id)
    
    # Verify
    assert len(result) == 1
    assert result[0].id == f_db_route_assignment.id
    assert result[0].vehicle_id == f_db_route_assignment.vehicle_id
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_by_driver_id_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [f_db_route_assignment]
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_driver_id(f_db_route_assignment.driver_id)
    
    # Verify
    assert len(result) == 1
    assert result[0].id == f_db_route_assignment.id
    assert result[0].driver_id == f_db_route_assignment.driver_id
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once()


def test_update_success(f_route_assignment_repository, m_db_session, f_db_route_assignment, f_route_assignment_update):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_route_assignment
    m_db_session.query.return_value = mock_query
    
    # Mock commit and refresh
    m_db_session.commit.return_value = None
    m_db_session.refresh.return_value = None
    
    # Execute
    result = f_route_assignment_repository.update(f_db_route_assignment.id, f_route_assignment_update)
    
    # Verify
    assert result is not None
    assert result.id == f_db_route_assignment.id
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()
    m_db_session.commit.assert_called_once()
    m_db_session.refresh.assert_called_once()


def test_update_not_found(f_route_assignment_repository, m_db_session, f_route_assignment_update):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.update(uuid4(), f_route_assignment_update)
    
    # Verify
    assert result is None
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()
    m_db_session.commit.assert_not_called()


def test_delete_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = f_db_route_assignment
    m_db_session.query.return_value = mock_query
    
    # Mock delete and commit
    m_db_session.delete.return_value = None
    m_db_session.commit.return_value = None
    
    # Execute
    result = f_route_assignment_repository.delete(f_db_route_assignment.id)
    
    # Verify
    assert result is True
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()
    m_db_session.delete.assert_called_once_with(f_db_route_assignment)
    m_db_session.commit.assert_called_once()


def test_delete_not_found(f_route_assignment_repository, m_db_session):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.delete(uuid4())
    
    # Verify
    assert result is False
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()
    m_db_session.delete.assert_not_called()


def test_get_all_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.all.return_value = [f_db_route_assignment]
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_all()
    
    # Verify
    assert len(result) == 1
    assert result[0].id == f_db_route_assignment.id
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.all.assert_called_once()


def test_get_by_status_success(f_route_assignment_repository, m_db_session, f_db_route_assignment):
    # Mock query
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [f_db_route_assignment]
    m_db_session.query.return_value = mock_query
    
    # Execute
    result = f_route_assignment_repository.get_by_status("pending")
    
    # Verify
    assert len(result) == 1
    assert result[0].id == f_db_route_assignment.id
    assert result[0].status == f_db_route_assignment.status
    
    m_db_session.query.assert_called_once_with(RouteAssignmentModel)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once() 