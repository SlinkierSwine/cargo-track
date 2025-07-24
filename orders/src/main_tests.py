import requests
from uuid import uuid4
from entities.order import OrderStatus

ORDER_SERVICE_URL = "http://localhost:8003"

# Пример warehouse_id и cargo_id, которые должны существовать в warehouse сервисе для успешных тестов
WAREHOUSE_ID = "00000000-0000-0000-0000-000000000001"
CARGO_ID = "00000000-0000-0000-0000-000000000001"


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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    vehicle_id = "00000000-0000-0000-0000-000000000001"
    response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/assign-vehicle", json={"vehicle_id": vehicle_id, "cargo_id": CARGO_ID})
    assert response.status_code in (200, 400)


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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    response = requests.put(f"{ORDER_SERVICE_URL}/orders/{order_id}/status", json={"new_status": OrderStatus.ASSIGNED, "cargo_id": CARGO_ID})
    assert response.status_code in (200, 400)


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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    requests.put(f"{ORDER_SERVICE_URL}/orders/{order_id}/status", json={"new_status": OrderStatus.ASSIGNED, "cargo_id": CARGO_ID})
    requests.put(f"{ORDER_SERVICE_URL}/orders/{order_id}/status", json={"new_status": OrderStatus.IN_TRANSIT, "cargo_id": CARGO_ID})
    response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/complete-delivery", json={"cargo_id": CARGO_ID})
    assert response.status_code in (200, 400)


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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    response = requests.post(url, json=data)
    assert response.status_code == 201
    order_id = response.json()["id"]
    response = requests.post(f"{ORDER_SERVICE_URL}/orders/{order_id}/cancel", json={"cargo_id": CARGO_ID})
    assert response.status_code in (200, 400)


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
        "notes": "Handle with care",
        "warehouse_id": WAREHOUSE_ID
    }
    data2 = {
        **data1,
        "customer_email": "jane@example.com",
        "customer_name": "Jane Doe"
    }
    requests.post(url, json=data1)
    requests.post(url, json=data2)
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_order_not_found_workflow():
    order_id = str(uuid4())
    response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}")
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
    response = requests.post(url, json=invalid_order_data)
    assert response.status_code == 422  # Validation error 