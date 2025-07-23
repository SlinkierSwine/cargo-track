import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from entities.driver import Driver, DriverCreate, DriverUpdate, DriverStatus
from repositories.driver_repository import DriverRepository


@pytest.fixture
def f_driver_repository(f_db_session):
    return DriverRepository(f_db_session)


@pytest.fixture
def f_valid_driver_data():
    return DriverCreate(
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


def test_create_driver(f_driver_repository, f_valid_driver_data):
    driver = f_driver_repository.create(f_valid_driver_data)
    
    assert driver.id is not None
    assert driver.first_name == f_valid_driver_data.first_name
    assert driver.last_name == f_valid_driver_data.last_name
    assert driver.email == f_valid_driver_data.email
    assert driver.phone == f_valid_driver_data.phone
    assert driver.license_number == f_valid_driver_data.license_number
    assert driver.license_class == f_valid_driver_data.license_class
    assert driver.license_expiry == f_valid_driver_data.license_expiry
    assert driver.medical_certificate_expiry == f_valid_driver_data.medical_certificate_expiry
    assert driver.experience_years == f_valid_driver_data.experience_years
    assert driver.status == DriverStatus.ACTIVE
    assert driver.emergency_contact_name == f_valid_driver_data.emergency_contact_name
    assert driver.emergency_contact_phone == f_valid_driver_data.emergency_contact_phone
    assert driver.created_at is not None
    assert driver.updated_at is not None


def test_get_by_id(f_driver_repository, f_valid_driver_data):
    created_driver = f_driver_repository.create(f_valid_driver_data)
    retrieved_driver = f_driver_repository.get_by_id(created_driver.id)
    
    assert retrieved_driver is not None
    assert retrieved_driver.id == created_driver.id
    assert retrieved_driver.first_name == created_driver.first_name
    assert retrieved_driver.email == created_driver.email


def test_get_by_id_not_found(f_driver_repository):
    non_existent_id = uuid4()
    driver = f_driver_repository.get_by_id(non_existent_id)
    
    assert driver is None


def test_get_by_email(f_driver_repository, f_valid_driver_data):
    created_driver = f_driver_repository.create(f_valid_driver_data)
    retrieved_driver = f_driver_repository.get_by_email(created_driver.email)
    
    assert retrieved_driver is not None
    assert retrieved_driver.id == created_driver.id
    assert retrieved_driver.email == created_driver.email


def test_get_by_email_not_found(f_driver_repository):
    driver = f_driver_repository.get_by_email("nonexistent@example.com")
    
    assert driver is None


def test_get_by_license_number(f_driver_repository, f_valid_driver_data):
    created_driver = f_driver_repository.create(f_valid_driver_data)
    retrieved_driver = f_driver_repository.get_by_license_number(created_driver.license_number)
    
    assert retrieved_driver is not None
    assert retrieved_driver.id == created_driver.id
    assert retrieved_driver.license_number == created_driver.license_number


def test_get_by_license_number_not_found(f_driver_repository):
    driver = f_driver_repository.get_by_license_number("NONEXISTENT")
    
    assert driver is None


def test_update_driver(f_driver_repository, f_valid_driver_data):
    created_driver = f_driver_repository.create(f_valid_driver_data)
    
    update_data = DriverUpdate(
        first_name="Jane",
        experience_years=10
    )
    
    updated_driver = f_driver_repository.update(created_driver.id, update_data)
    
    assert updated_driver is not None
    assert updated_driver.id == created_driver.id
    assert updated_driver.first_name == "Jane"
    assert updated_driver.last_name == created_driver.last_name  # unchanged
    assert updated_driver.experience_years == 10
    assert updated_driver.updated_at > created_driver.updated_at


def test_update_driver_not_found(f_driver_repository):
    non_existent_id = uuid4()
    update_data = DriverUpdate(first_name="Jane")
    
    updated_driver = f_driver_repository.update(non_existent_id, update_data)
    
    assert updated_driver is None


def test_delete_driver(f_driver_repository, f_valid_driver_data):
    created_driver = f_driver_repository.create(f_valid_driver_data)
    
    result = f_driver_repository.delete(created_driver.id)
    
    assert result is True
    
    # Verify driver is deleted
    retrieved_driver = f_driver_repository.get_by_id(created_driver.id)
    assert retrieved_driver is None


def test_delete_driver_not_found(f_driver_repository):
    non_existent_id = uuid4()
    
    result = f_driver_repository.delete(non_existent_id)
    
    assert result is False


def test_get_all_drivers(f_driver_repository, f_valid_driver_data):
    # Create multiple drivers
    driver1 = f_driver_repository.create(f_valid_driver_data)
    
    driver2_data = DriverCreate(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        phone="+1234567892",
        license_number="DL987654321",
        license_class="B",
        license_expiry=datetime.now() + timedelta(days=365),
        medical_certificate_expiry=datetime.now() + timedelta(days=180),
        experience_years=3,
        emergency_contact_name="John Smith",
        emergency_contact_phone="+1234567893"
    )
    driver2 = f_driver_repository.create(driver2_data)
    
    all_drivers = f_driver_repository.get_all()
    
    assert len(all_drivers) >= 2
    driver_ids = [driver.id for driver in all_drivers]
    assert driver1.id in driver_ids
    assert driver2.id in driver_ids


def test_get_by_status(f_driver_repository, f_valid_driver_data):
    # Create active driver
    active_driver = f_driver_repository.create(f_valid_driver_data)
    
    # Create inactive driver
    inactive_driver_data = DriverCreate(
        first_name="Inactive",
        last_name="Driver",
        email="inactive@example.com",
        phone="+1234567894",
        license_number="DL111111111",
        license_class="C",
        license_expiry=datetime.now() + timedelta(days=365),
        medical_certificate_expiry=datetime.now() + timedelta(days=180),
        experience_years=2,
        emergency_contact_name="Contact",
        emergency_contact_phone="+1234567895"
    )
    inactive_driver = f_driver_repository.create(inactive_driver_data)
    
    # Update inactive driver status
    f_driver_repository.update(inactive_driver.id, DriverUpdate(status=DriverStatus.TERMINATED))
    
    active_drivers = f_driver_repository.get_by_status(DriverStatus.ACTIVE)
    terminated_drivers = f_driver_repository.get_by_status(DriverStatus.TERMINATED)
    
    assert len(active_drivers) >= 1
    assert len(terminated_drivers) >= 1
    
    active_driver_ids = [driver.id for driver in active_drivers]
    terminated_driver_ids = [driver.id for driver in terminated_drivers]
    
    assert active_driver.id in active_driver_ids
    assert inactive_driver.id in terminated_driver_ids


def test_get_available_drivers(f_driver_repository, f_valid_driver_data):
    # Create available driver (active with valid documents)
    available_driver = f_driver_repository.create(f_valid_driver_data)
    
    # Create unavailable driver (expired license)
    expired_driver_data = DriverCreate(
        first_name="Expired",
        last_name="Driver",
        email="expired@example.com",
        phone="+1234567896",
        license_number="DL222222222",
        license_class="C",
        license_expiry=datetime.now() - timedelta(days=1),  # expired
        medical_certificate_expiry=datetime.now() + timedelta(days=180),
        experience_years=1,
        emergency_contact_name="Contact",
        emergency_contact_phone="+1234567897"
    )
    expired_driver = f_driver_repository.create(expired_driver_data)
    
    available_drivers = f_driver_repository.get_available_drivers()
    
    assert len(available_drivers) >= 1
    
    available_driver_ids = [driver.id for driver in available_drivers]
    assert available_driver.id in available_driver_ids
    assert expired_driver.id not in available_driver_ids 