import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta
from entities.vehicle import Vehicle, VehicleStatus
from entities.driver import Driver, DriverStatus
from entities.route_assignment import RouteAssignmentStatus
from use_cases.assign_route_use_case import AssignRouteUseCase, AssignRouteRequest


@pytest.fixture
def m_vehicle_repository():
    return MagicMock()


@pytest.fixture
def m_driver_repository():
    return MagicMock()


@pytest.fixture
def m_route_assignment_repository():
    return MagicMock()


@pytest.fixture
def f_assign_route_use_case(m_vehicle_repository, m_driver_repository, m_route_assignment_repository):
    return AssignRouteUseCase(m_vehicle_repository, m_driver_repository, m_route_assignment_repository)


@pytest.fixture
def f_valid_assign_route_request():
    return AssignRouteRequest(
        route_id=uuid4(),
        vehicle_id=uuid4(),
        driver_id=uuid4(),
        estimated_duration_hours=8.5,
        notes="Regular delivery route"
    )


@pytest.fixture
def f_mock_vehicle():
    return Vehicle(
        id=uuid4(),
        license_plate="ABC123",
        vehicle_type="truck",
        brand="Volvo",
        model="FH16",
        year=2020,
        capacity_weight=20000.0,
        capacity_volume=80.0,
        fuel_type="diesel",
        fuel_efficiency=2.5,
        status=VehicleStatus.ACTIVE,
        insurance_expiry=datetime.now() + timedelta(days=365),
        registration_expiry=datetime.now() + timedelta(days=365),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def f_mock_driver():
    return Driver(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        license_number="DL123456789",
        license_class="C",
        license_expiry=datetime.now() + timedelta(days=365),
        medical_certificate_expiry=datetime.now() + timedelta(days=180),
        experience_years=5,
        status=DriverStatus.ACTIVE,
        emergency_contact_name="Jane Doe",
        emergency_contact_phone="+1234567891",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


def test_assign_route_success(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle, f_mock_driver):
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = f_mock_driver
    
    # Mock route assignment creation
    from entities.route_assignment import RouteAssignment, RouteAssignmentStatus
    mock_assignment = RouteAssignment(
        id=uuid4(),
        route_id=f_valid_assign_route_request.route_id,
        vehicle_id=f_valid_assign_route_request.vehicle_id,
        driver_id=f_valid_assign_route_request.driver_id,
        status=RouteAssignmentStatus.ASSIGNED,
        assigned_at=datetime.now(),
        estimated_duration_hours=f_valid_assign_route_request.estimated_duration_hours,
        notes=f_valid_assign_route_request.notes,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    m_route_assignment_repository.create.return_value = mock_assignment
    
    # Execute use case
    result = f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)
    
    # Verify result
    assert result.route_id == str(f_valid_assign_route_request.route_id)
    assert result.vehicle_id == str(f_valid_assign_route_request.vehicle_id)
    assert result.driver_id == str(f_valid_assign_route_request.driver_id)
    assert result.status == RouteAssignmentStatus.ASSIGNED
    assert result.estimated_duration_hours == f_valid_assign_route_request.estimated_duration_hours
    assert result.notes == f_valid_assign_route_request.notes
    assert result.assigned_at is not None
    
    # Verify route assignment repository was called
    m_route_assignment_repository.create.assert_called_once()


def test_assign_route_vehicle_not_found(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request):
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Vehicle not found"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_not_called()
    m_route_assignment_repository.create.assert_not_called()


def test_assign_route_vehicle_not_available(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle):
    # Modify vehicle status to inactive
    f_mock_vehicle.status = VehicleStatus.MAINTENANCE
    
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Vehicle is not available for assignment"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_not_called()
    m_route_assignment_repository.create.assert_not_called()


def test_assign_route_driver_not_found(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle):
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver not found"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)
    m_route_assignment_repository.create.assert_not_called()


def test_assign_route_driver_not_available(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle, f_mock_driver):
    # Modify driver status to inactive
    f_mock_driver.status = DriverStatus.TERMINATED
    
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver is not available for assignment"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)
    m_route_assignment_repository.create.assert_not_called()


def test_assign_route_driver_license_expired(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle, f_mock_driver):
    # Modify driver license to expired
    f_mock_driver.license_expiry = datetime.now() - timedelta(days=1)
    
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver's license has expired"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)
    m_route_assignment_repository.create.assert_not_called()


def test_assign_route_driver_medical_certificate_expired(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle, f_mock_driver):
    # Modify driver medical certificate to expired
    f_mock_driver.medical_certificate_expiry = datetime.now() - timedelta(days=1)
    
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver's medical certificate has expired"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)


def test_assign_route_invalid_duration(f_assign_route_use_case, m_vehicle_repository, m_driver_repository, m_route_assignment_repository, f_valid_assign_route_request, f_mock_vehicle, f_mock_driver):
    # Modify request with invalid duration
    f_valid_assign_route_request.estimated_duration_hours = -5.0
    
    # Mock repository responses
    m_vehicle_repository.get_by_id.return_value = f_mock_vehicle
    m_driver_repository.get_by_id.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Estimated duration must be positive"):
        f_assign_route_use_case.execute(f_valid_assign_route_request)
    
    # Verify repository calls
    m_vehicle_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.vehicle_id)
    m_driver_repository.get_by_id.assert_called_once_with(f_valid_assign_route_request.driver_id)
    m_route_assignment_repository.create.assert_not_called() 