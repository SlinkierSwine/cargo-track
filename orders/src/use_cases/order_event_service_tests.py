import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from uuid import uuid4
from use_cases.order_event_service import OrderEventService
from shared.events.models import OrderCreatedEvent, VehicleAssignedEvent, NoVehicleAvailableEvent


class TestOrderEventService:
    
    @pytest.fixture
    def m_publisher(self):
        return Mock()
    
    @pytest.fixture
    def m_subscriber(self):
        return Mock()
    
    @pytest.fixture
    def order_event_service(self, m_publisher, m_subscriber):
        return OrderEventService(m_publisher, m_subscriber)
    
    @pytest.fixture
    def sample_order_data(self):
        return {
            "id": str(uuid4()),
            "customer_name": "John Doe",
            "customer_email": "john@example.com",
            "pickup_address": "123 Pickup St",
            "delivery_address": "456 Delivery Ave",
            "cargo_type": "electronics",
            "cargo_weight": 100.0,
            "cargo_volume": 2.0,
            "notes": "Handle with care"
        }
    
    def test_publish_order_created_event(self, order_event_service, m_publisher, sample_order_data):
        # Arrange
        order_data = sample_order_data
        
        # Act
        order_event_service.publish_order_created(order_data)
        
        # Assert
        m_publisher.publish.assert_called_once()
        call_args = m_publisher.publish.call_args
        assert call_args[0][0] == "order_created"
        event_data = call_args[0][1]
        assert event_data["order_id"] == order_data["id"]
        assert event_data["customer_name"] == order_data["customer_name"]
        assert event_data["customer_email"] == order_data["customer_email"]
    
    def test_handle_vehicle_assigned_event(self, order_event_service, m_subscriber):
        # Arrange
        event_data = {
            "order_id": str(uuid4()),
            "vehicle_id": str(uuid4()),
            "driver_id": str(uuid4()),
            "vehicle_license_plate": "ABC123",
            "driver_name": "John Driver",
            "estimated_delivery_time": datetime.now().isoformat()
        }
        
        # Act
        order_event_service.handle_vehicle_assigned(event_data)
        
        # Assert
        # Здесь будет логика обновления статуса заказа
        # Пока просто проверяем, что метод не падает
        assert True
    
    def test_handle_no_vehicle_available_event(self, order_event_service, m_subscriber):
        # Arrange
        event_data = {
            "order_id": str(uuid4()),
            "reason": "no_drivers"
        }
        
        # Act
        order_event_service.handle_no_vehicle_available(event_data)
        
        # Assert
        # Здесь будет логика обработки отсутствия транспорта
        # Пока просто проверяем, что метод не падает
        assert True
    
    def test_start_listening(self, order_event_service, m_subscriber):
        # Act
        order_event_service.start_listening()
        
        # Assert
        m_subscriber.subscribe.assert_called()
        # Проверяем, что подписались на нужные события
        calls = m_subscriber.subscribe.call_args_list
        event_types = [call[0][0] for call in calls]
        assert "vehicle_assigned" in event_types
        assert "no_vehicle_available" in event_types 