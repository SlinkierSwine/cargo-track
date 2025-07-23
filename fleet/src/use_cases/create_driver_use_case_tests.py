import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime, timedelta
from entities.driver import Driver, DriverStatus
from use_cases.create_driver_use_case import CreateDriverUseCase, CreateDriverRequest


@pytest.fixture
def m_driver_repository():
    return MagicMock()


@pytest.fixture
def f_create_driver_use_case(m_driver_repository):
    return CreateDriverUseCase(m_driver_repository)


@pytest.fixture
def f_valid_driver_request():
    return CreateDriverRequest(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+1234567890",
        license_number="DL123456789",
        license_class="C",
        license_expiry=datetime.now() + timedelta(days=365),
        medical_certificate_expiry=datetime.now() + timedelta(days=180),
        experience_years=5,
        emergency_contact_name="Jane Doe",
        emergency_contact_phone="+1234567891"
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


def test_create_driver_success(f_create_driver_use_case, m_driver_repository, f_valid_driver_request, f_mock_driver):
    # Mock repository responses
    m_driver_repository.get_by_email.return_value = None
    m_driver_repository.get_by_license_number.return_value = None
    m_driver_repository.create.return_value = f_mock_driver
    
    # Execute use case
    result = f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_called_once_with(f_valid_driver_request.license_number)
    m_driver_repository.create.assert_called_once()
    
    # Verify result
    assert result.id == str(f_mock_driver.id)
    assert result.first_name == f_mock_driver.first_name
    assert result.last_name == f_mock_driver.last_name
    assert result.email == f_mock_driver.email
    assert result.phone == f_mock_driver.phone
    assert result.license_number == f_mock_driver.license_number
    assert result.license_class == f_mock_driver.license_class
    assert result.experience_years == f_mock_driver.experience_years
    assert result.status == f_mock_driver.status


def test_create_driver_email_already_exists(f_create_driver_use_case, m_driver_repository, f_valid_driver_request, f_mock_driver):
    # Mock repository to return existing driver
    m_driver_repository.get_by_email.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver with this email already exists"):
        f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_not_called()
    m_driver_repository.create.assert_not_called()


def test_create_driver_license_number_already_exists(f_create_driver_use_case, m_driver_repository, f_valid_driver_request, f_mock_driver):
    # Mock repository responses
    m_driver_repository.get_by_email.return_value = None
    m_driver_repository.get_by_license_number.return_value = f_mock_driver
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Driver with this license number already exists"):
        f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_called_once_with(f_valid_driver_request.license_number)
    m_driver_repository.create.assert_not_called()


def test_create_driver_negative_experience_years(f_create_driver_use_case, m_driver_repository, f_valid_driver_request):
    # Modify request with negative experience years
    f_valid_driver_request.experience_years = -5
    
    # Mock repository responses
    m_driver_repository.get_by_email.return_value = None
    m_driver_repository.get_by_license_number.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Experience years cannot be negative"):
        f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_called_once_with(f_valid_driver_request.license_number)
    m_driver_repository.create.assert_not_called()


def test_create_driver_expired_license(f_create_driver_use_case, m_driver_repository, f_valid_driver_request):
    # Modify request with expired license
    f_valid_driver_request.license_expiry = datetime.now() - timedelta(days=1)
    
    # Mock repository responses
    m_driver_repository.get_by_email.return_value = None
    m_driver_repository.get_by_license_number.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="License expiry date must be in the future"):
        f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_called_once_with(f_valid_driver_request.license_number)
    m_driver_repository.create.assert_not_called()


def test_create_driver_expired_medical_certificate(f_create_driver_use_case, m_driver_repository, f_valid_driver_request):
    # Modify request with expired medical certificate
    f_valid_driver_request.medical_certificate_expiry = datetime.now() - timedelta(days=1)
    
    # Mock repository responses
    m_driver_repository.get_by_email.return_value = None
    m_driver_repository.get_by_license_number.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Medical certificate expiry date must be in the future"):
        f_create_driver_use_case.execute(f_valid_driver_request)
    
    # Verify repository calls
    m_driver_repository.get_by_email.assert_called_once_with(f_valid_driver_request.email)
    m_driver_repository.get_by_license_number.assert_called_once_with(f_valid_driver_request.license_number)
    m_driver_repository.create.assert_not_called() 