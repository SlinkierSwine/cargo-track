import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from uuid import uuid4
from use_cases.fleet_event_service import FleetEventService
from entities.vehicle import Vehicle, VehicleType, FuelType, VehicleStatus
from entities.driver import Driver, DriverStatus


class TestFleetEventService:
    
    @pytest.fixture
    def m_publisher(self):
        return Mock()
    
    @pytest.fixture
    def m_subscriber(self):
        return Mock()
    
    @pytest.fixture
    def m_driver_repository(self):
        return Mock()
    
    @pytest.fixture
    def m_vehicle_repository(self):
        return Mock()
    
    @pytest.fixture
    def fleet_event_service(self, m_publisher, m_subscriber, m_driver_repository, m_vehicle_repository):
        return FleetEventService(m_publisher, m_subscriber, m_driver_repository, m_vehicle_repository)
    
    @pytest.fixture
    def sample_order_event_data(self):
        return {
            "order_id": str(uuid4()),
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "pickup_address": "123 Pickup St",
            "delivery_address": "456 Delivery Ave",
            "cargo_type": "electronics",
            "cargo_weight": 100.0,
            "cargo_volume": 2.0,
            "notes": "Handle with care"
        }
    
    @pytest.fixture
    def sample_available_driver(self):
        return Driver(
            id=uuid4(),
            first_name="John",
            last_name="Driver",
            email="driver@example.com",
            phone="+1234567890",
            license_number="DL123456",
            license_class="C",
            license_expiry=datetime(2025, 12, 31),
            medical_certificate_expiry=datetime(2025, 12, 31),
            status=DriverStatus.ACTIVE,
            experience_years=5,
            emergency_contact_name="Jane Driver",
            emergency_contact_phone="+1234567891",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    @pytest.fixture
    def sample_available_vehicle(self):
        return Vehicle(
            id=uuid4(),
            license_plate="ABC123",
            vehicle_type=VehicleType.TRUCK,
            brand="Volvo",
            model="FH16",
            year=2020,
            capacity_weight=20000.0,
            capacity_volume=80.0,
            fuel_type=FuelType.DIESEL,
            fuel_efficiency=2.5,
            status=VehicleStatus.ACTIVE,
            insurance_expiry=datetime(2025, 12, 31),
            registration_expiry=datetime(2025, 12, 31),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    def test_handle_order_created_with_available_resources(self, fleet_event_service, m_publisher, 
                                                         sample_order_event_data, sample_available_driver, 
                                                         sample_available_vehicle):
        # Arrange
        fleet_event_service.driver_repository.get_available_drivers.return_value = [sample_available_driver]
        fleet_event_service.vehicle_repository.get_available_vehicles.return_value = [sample_available_vehicle]
        
        # Act
        fleet_event_service.handle_order_created(sample_order_event_data)
        
        # Assert
        m_publisher.publish.assert_called_once()
        call_args = m_publisher.publish.call_args
        assert call_args[0][0] == "vehicle_assigned"
        event_data = call_args[0][1]
        assert event_data["order_id"] == sample_order_event_data["order_id"]
        assert event_data["vehicle_id"] == str(sample_available_vehicle.id)
        assert event_data["driver_id"] == str(sample_available_driver.id)
    
    def test_handle_order_created_no_available_drivers(self, fleet_event_service, m_publisher, 
                                                     sample_order_event_data, sample_available_vehicle):
        # Arrange
        fleet_event_service.driver_repository.get_available_drivers.return_value = []
        fleet_event_service.vehicle_repository.get_available_vehicles.return_value = [sample_available_vehicle]
        
        # Act
        fleet_event_service.handle_order_created(sample_order_event_data)
        
        # Assert
        m_publisher.publish.assert_called_once()
        call_args = m_publisher.publish.call_args
        assert call_args[0][0] == "no_vehicle_available"
        event_data = call_args[0][1]
        assert event_data["order_id"] == sample_order_event_data["order_id"]
        assert event_data["reason"] == "no_drivers"
    
    def test_handle_order_created_no_available_vehicles(self, fleet_event_service, m_publisher, 
                                                      sample_order_event_data, sample_available_driver):
        # Arrange
        fleet_event_service.driver_repository.get_available_drivers.return_value = [sample_available_driver]
        fleet_event_service.vehicle_repository.get_available_vehicles.return_value = []
        
        # Act
        fleet_event_service.handle_order_created(sample_order_event_data)
        
        # Assert
        m_publisher.publish.assert_called_once()
        call_args = m_publisher.publish.call_args
        assert call_args[0][0] == "no_vehicle_available"
        event_data = call_args[0][1]
        assert event_data["order_id"] == sample_order_event_data["order_id"]
        assert event_data["reason"] == "no_vehicles"
    
    def test_handle_order_created_capacity_mismatch(self, fleet_event_service, m_publisher, 
                                                  sample_order_event_data, sample_available_driver):
        # Arrange
        small_vehicle = Vehicle(
            id=uuid4(),
            license_plate="SMALL123",
            vehicle_type=VehicleType.VAN,
            brand="Ford",
            model="Transit",
            year=2020,
            capacity_weight=50.0,  # Too small for cargo weight 100.0
            capacity_volume=1.0,   # Too small for cargo volume 2.0
            fuel_type=FuelType.DIESEL,
            fuel_efficiency=2.5,
            status=VehicleStatus.ACTIVE,
            insurance_expiry=datetime(2025, 12, 31),
            registration_expiry=datetime(2025, 12, 31),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        fleet_event_service.driver_repository.get_available_drivers.return_value = [sample_available_driver]
        fleet_event_service.vehicle_repository.get_available_vehicles.return_value = [small_vehicle]
        
        # Act
        fleet_event_service.handle_order_created(sample_order_event_data)
        
        # Assert
        m_publisher.publish.assert_called_once()
        call_args = m_publisher.publish.call_args
        assert call_args[0][0] == "no_vehicle_available"
        event_data = call_args[0][1]
        assert event_data["order_id"] == sample_order_event_data["order_id"]
        assert event_data["reason"] == "capacity_mismatch"
    
    def test_start_listening(self, fleet_event_service, m_subscriber):
        # Act
        fleet_event_service.start_listening()
        
        # Assert
        m_subscriber.subscribe.assert_called_once_with("order_created", fleet_event_service.handle_order_created) 