import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from uuid import uuid4
from main import app
from entities.order import OrderStatus


@pytest.fixture
def f_client():
    return TestClient(app)


@pytest.fixture
def f_valid_order_data():
    return {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "+1234567890",
        "pickup_address": "123 Pickup St, City",
        "delivery_address": "456 Delivery Ave, City",
        "cargo_type": "electronics",
        "cargo_weight": 100.0,
        "cargo_volume": 2.0,
        "notes": "Handle with care"
    }


@pytest.fixture
def f_created_order():
    return {
        "id": str(uuid4()),
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "+1234567890",
        "pickup_address": "123 Pickup St, City",
        "delivery_address": "456 Delivery Ave, City",
        "cargo_type": "electronics",
        "cargo_weight": 100.0,
        "cargo_volume": 2.0,
        "status": OrderStatus.PENDING,
        "vehicle_id": None,
        "driver_id": None,
        "estimated_cost": None,
        "actual_cost": None,
        "pickup_date": None,
        "delivery_date": None,
        "notes": "Handle with care",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": None
    }


def test_create_order_workflow(f_client, f_valid_order_data, f_created_order):
    with patch('controllers.order_controller.CreateOrderUseCase') as mock_use_case:
        mock_instance = MagicMock()
        mock_instance.execute.return_value = f_created_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.post("/orders", json=f_valid_order_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["customer_name"] == f_valid_order_data["customer_name"]
        assert data["status"] == OrderStatus.PENDING


def test_get_order_workflow(f_client, f_created_order):
    with patch('controllers.order_controller.GetOrderUseCase') as mock_use_case:
        mock_instance = MagicMock()
        mock_instance.execute.return_value = f_created_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.get(f"/orders/{f_created_order['id']}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == f_created_order["id"]


def test_assign_vehicle_workflow(f_client, f_created_order):
    order_id = f_created_order["id"]
    vehicle_id = str(uuid4())
    
    with patch('controllers.order_controller.AssignVehicleUseCase') as mock_use_case:
        mock_instance = MagicMock()
        updated_order = f_created_order.copy()
        updated_order["vehicle_id"] = vehicle_id
        updated_order["status"] = OrderStatus.ASSIGNED
        mock_instance.execute.return_value = updated_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.post(f"/orders/{order_id}/assign-vehicle", json={"vehicle_id": vehicle_id})
        
        assert response.status_code == 200
        data = response.json()
        assert data["vehicle_id"] == vehicle_id
        assert data["status"] == OrderStatus.ASSIGNED


def test_change_order_status_workflow(f_client, f_created_order):
    order_id = f_created_order["id"]
    
    with patch('controllers.order_controller.ChangeOrderStatusUseCase') as mock_use_case:
        mock_instance = MagicMock()
        updated_order = f_created_order.copy()
        updated_order["status"] = OrderStatus.IN_TRANSIT
        mock_instance.execute.return_value = updated_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.put(f"/orders/{order_id}/status", json={"new_status": OrderStatus.IN_TRANSIT})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == OrderStatus.IN_TRANSIT


def test_complete_delivery_workflow(f_client, f_created_order):
    order_id = f_created_order["id"]
    
    with patch('controllers.order_controller.CompleteDeliveryUseCase') as mock_use_case:
        mock_instance = MagicMock()
        updated_order = f_created_order.copy()
        updated_order["status"] = OrderStatus.DELIVERED
        mock_instance.execute.return_value = updated_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.post(f"/orders/{order_id}/complete-delivery")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == OrderStatus.DELIVERED


def test_cancel_order_workflow(f_client, f_created_order):
    order_id = f_created_order["id"]
    
    with patch('controllers.order_controller.CancelOrderUseCase') as mock_use_case:
        mock_instance = MagicMock()
        updated_order = f_created_order.copy()
        updated_order["status"] = OrderStatus.CANCELLED
        mock_instance.execute.return_value = updated_order
        mock_use_case.return_value = mock_instance
        
        response = f_client.post(f"/orders/{order_id}/cancel")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == OrderStatus.CANCELLED


def test_get_orders_list_workflow(f_client):
    orders_list = [
        {
            "id": str(uuid4()),
            "customer_name": "John Doe",
            "status": OrderStatus.PENDING
        },
        {
            "id": str(uuid4()),
            "customer_name": "Jane Doe",
            "status": OrderStatus.ASSIGNED
        }
    ]
    
    with patch('controllers.order_controller.ListOrdersUseCase') as mock_use_case:
        mock_instance = MagicMock()
        mock_instance.execute.return_value = orders_list
        mock_use_case.return_value = mock_instance
        
        response = f_client.get("/orders")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["customer_name"] == "John Doe"
        assert data[1]["customer_name"] == "Jane Doe"


def test_order_not_found_workflow(f_client):
    order_id = str(uuid4())
    
    with patch('controllers.order_controller.GetOrderUseCase') as mock_use_case:
        mock_instance = MagicMock()
        mock_instance.execute.side_effect = ValueError("Order not found")
        mock_use_case.return_value = mock_instance
        
        response = f_client.get(f"/orders/{order_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert "Order not found" in data["detail"]


def test_invalid_order_data_workflow(f_client):
    invalid_order_data = {
        "customer_name": "",  # Invalid empty name
        "customer_email": "invalid-email",  # Invalid email
        "customer_phone": "+1234567890",
        "pickup_address": "123 Pickup St, City",
        "delivery_address": "456 Delivery Ave, City",
        "cargo_type": "electronics",
        "cargo_weight": 0.0,  # Invalid weight
        "cargo_volume": 2.0
    }
    
    response = f_client.post("/orders", json=invalid_order_data)
    
    assert response.status_code == 422  # Validation error 