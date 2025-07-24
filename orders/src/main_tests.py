import requests
from uuid import uuid4
from entities.order import OrderStatus
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch

ORDER_SERVICE_URL = "http://orders-service:8000"

# Тестовые данные без зависимости от внешних сервисов
WAREHOUSE_ID = "test-warehouse-id"
CARGO_ID = "test-cargo-id"
VEHICLE_ID = "test-vehicle-id"

# Создаем тестовый JWT токен для аутентификации
def get_test_token():
    payload = {
        "sub": "test-user",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    secret_key = "your-secret-key-here"
    return jwt.encode(payload, secret_key, algorithm="HS256")

# Общие заголовки для всех запросов
def get_headers():
    return {
        "Authorization": f"Bearer {get_test_token()}",
        "Content-Type": "application/json"
    }

# Mock данные для внешних сервисов
def get_mock_vehicle_data():
    return {
        "id": VEHICLE_ID,
        "license_plate": "TEST123",
        "vehicle_type": "truck",
        "brand": "Test Brand",
        "model": "Test Model",
        "year": 2020,
        "capacity_weight": 1000.0,
        "capacity_volume": 10.0,
        "fuel_type": "diesel",
        "fuel_efficiency": 2.5,
        "status": "active",
        "insurance_expiry": "2025-12-31",
        "registration_expiry": "2025-12-31"
    }

def get_mock_cargo_data():
    return {
        "id": CARGO_ID,
        "name": "Test Cargo",
        "type": "electronics",
        "weight": 100.0,
        "volume": 2.0,
        "status": "stored",
        "warehouse_id": WAREHOUSE_ID
    }

def get_mock_warehouse_data():
    return {
        "id": WAREHOUSE_ID,
        "name": "Test Warehouse",
        "address": "Test Address",
        "capacity": 1000.0,
        "current_occupancy": 500.0,
        "status": "active"
    }


def test_create_order_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "+1234567890",
        "pickup_address": "123 Pickup St, City",
        "delivery_address": "456 Delivery Ave, City",
        "cargo_type": "electronics",
        "cargo_weight": 100.0,
        "cargo_volume": 2.0,
        "notes": "Handle with care"
        # Убираем warehouse_id, чтобы не зависеть от внешнего сервиса
    }
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["status"] == OrderStatus.PENDING
    global created_order_id
    created_order_id = data["id"]


def test_get_order_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
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
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    order_id = response.json()["id"]
    response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", headers=get_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id


def test_assign_vehicle_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
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
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    # Используем mock данные для внешних сервисов
    with patch('utils.fleet_service_client.FleetServiceClient.get_vehicle', return_value=get_mock_vehicle_data()), \
         patch('utils.warehouse_service_client.WarehouseServiceClient.get_cargo', return_value=get_mock_cargo_data()):
        response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/assign-vehicle", json={"vehicle_id": VEHICLE_ID, "cargo_id": CARGO_ID}, headers=get_headers())
        # Ожидаем 200, так как mock данные корректны
        assert response.status_code == 200


def test_change_order_status_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
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
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    # Используем mock данные для внешних сервисов
    with patch('utils.warehouse_service_client.WarehouseServiceClient.get_cargo', return_value=get_mock_cargo_data()), \
         patch('utils.warehouse_service_client.WarehouseServiceClient.update_cargo_status', return_value=True):
        response = requests.put(f"{ORDER_SERVICE_URL}/orders/{order_id}/status", json={"new_status": OrderStatus.ASSIGNED, "cargo_id": CARGO_ID}, headers=get_headers())
        # Ожидаем 200, так как изменение статуса работает с mock данными
        assert response.status_code == 200


def test_complete_delivery_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
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
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    # Используем mock данные для внешних сервисов
    with patch('utils.warehouse_service_client.WarehouseServiceClient.get_cargo', return_value=get_mock_cargo_data()), \
         patch('utils.warehouse_service_client.WarehouseServiceClient.update_cargo_status', return_value=True):
        response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/complete-delivery", json={"cargo_id": CARGO_ID}, headers=get_headers())
        # Ожидаем 200, так как завершение доставки работает с mock данными
        assert response.status_code == 200


def test_cancel_order_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data = {
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
    response = requests.post(url, json=data, headers=get_headers())
    assert response.status_code == 201
    order_id = response.json()["id"]
    
    # Используем mock данные для внешних сервисов
    with patch('utils.warehouse_service_client.WarehouseServiceClient.get_cargo', return_value=get_mock_cargo_data()), \
         patch('utils.warehouse_service_client.WarehouseServiceClient.update_cargo_status', return_value=True):
        response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/cancel", json={"cargo_id": CARGO_ID}, headers=get_headers())
        # Ожидаем 200, так как отмена заказа работает с mock данными
        assert response.status_code == 200


def test_get_orders_list_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
    data1 = {
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
    data2 = {
        **data1,
        "customer_email": "jane@example.com",
        "customer_name": "Jane Doe"
    }
    requests.post(url, json=data1, headers=get_headers())
    requests.post(url, json=data2, headers=get_headers())
    response = requests.get(url, headers=get_headers())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_order_not_found_workflow():
    order_id = str(uuid4())
    response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", headers=get_headers())
    assert response.status_code == 404
    data = response.json()
    assert "Order not found" in data["detail"]


def test_invalid_order_data_workflow():
    url = f"{ORDER_SERVICE_URL}/orders"
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
    response = requests.post(url, json=invalid_order_data, headers=get_headers())
    # Ожидаем 400, так как валидация происходит на уровне бизнес-логики
    assert response.status_code == 400 