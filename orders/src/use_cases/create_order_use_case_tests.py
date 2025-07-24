import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from entities.order import Order, OrderStatus
from repositories.order_repository import OrderRepository
from use_cases.create_order_use_case import CreateOrderUseCase, CreateOrderRequest
from shared.events.publisher import Publisher
from pydantic import ValidationError

@pytest.fixture
def m_order_repository():
    return MagicMock()

@pytest.fixture
def m_warehouse_service_client():
    return MagicMock()

@pytest.fixture
def m_publisher():
    return MagicMock(spec=Publisher)

@pytest.fixture
def f_create_order_use_case(m_order_repository, m_warehouse_service_client, m_publisher):
    return CreateOrderUseCase(m_order_repository, m_publisher, m_warehouse_service_client)

@pytest.fixture
def f_valid_order_request():
    return CreateOrderRequest(
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="+1234567890",
        pickup_address="123 Pickup St, City",
        delivery_address="456 Delivery Ave, City",
        cargo_type="electronics",
        cargo_weight=100.0,
        cargo_volume=2.0,
        notes="Handle with care",
        warehouse_id="00000000-0000-0000-0000-000000000001"
    )

def test_create_order_success(f_create_order_use_case, m_order_repository, m_warehouse_service_client, f_valid_order_request):
    # Mock warehouse_service_client
    m_warehouse_service_client.get_warehouse.return_value = {
        "id": f_valid_order_request.warehouse_id,
        "status": "active",
        "available_capacity_weight": 1000.0,
        "available_capacity_volume": 100.0
    }
    # Mock repository response
    mock_order = Order(
        customer_name=f_valid_order_request.customer_name,
        customer_email=f_valid_order_request.customer_email,
        customer_phone=f_valid_order_request.customer_phone,
        pickup_address=f_valid_order_request.pickup_address,
        delivery_address=f_valid_order_request.delivery_address,
        cargo_type=f_valid_order_request.cargo_type,
        cargo_weight=f_valid_order_request.cargo_weight,
        cargo_volume=f_valid_order_request.cargo_volume,
        status=OrderStatus.PENDING,
        notes=f_valid_order_request.notes
    )
    m_order_repository.create.return_value = mock_order
    # Execute use case
    result = f_create_order_use_case.execute(f_valid_order_request)
    # Verify warehouse_service_client called
    m_warehouse_service_client.get_warehouse.assert_called_once_with(f_valid_order_request.warehouse_id)
    # Verify repository calls
    m_order_repository.create.assert_called_once()
    # Verify result
    assert result.customer_name == mock_order.customer_name
    assert result.status == mock_order.status

def test_create_order_warehouse_not_found(f_create_order_use_case, m_warehouse_service_client, f_valid_order_request):
    m_warehouse_service_client.get_warehouse.return_value = None
    with pytest.raises(ValueError, match="Warehouse not found"):
        f_create_order_use_case.execute(f_valid_order_request)

def test_create_order_warehouse_not_active(f_create_order_use_case, m_warehouse_service_client, f_valid_order_request):
    m_warehouse_service_client.get_warehouse.return_value = {
        "id": f_valid_order_request.warehouse_id,
        "status": "inactive",
        "available_capacity_weight": 1000.0,
        "available_capacity_volume": 100.0
    }
    with pytest.raises(ValueError, match="Warehouse is not active"):
        f_create_order_use_case.execute(f_valid_order_request)

def test_create_order_not_enough_capacity(f_create_order_use_case, m_warehouse_service_client, f_valid_order_request):
    m_warehouse_service_client.get_warehouse.return_value = {
        "id": f_valid_order_request.warehouse_id,
        "status": "active",
        "available_capacity_weight": 10.0,
        "available_capacity_volume": 1.0
    }
    with pytest.raises(ValueError, match="Not enough capacity in warehouse"):
        f_create_order_use_case.execute(f_valid_order_request)

def test_create_order_invalid_cargo_weight(f_create_order_use_case, f_valid_order_request):
    with pytest.raises(ValidationError, match="cargo_weight"):
        CreateOrderRequest(
            **{**f_valid_order_request.dict(), "cargo_weight": 0.0}
        )

def test_create_order_invalid_cargo_volume(f_create_order_use_case, f_valid_order_request):
    with pytest.raises(ValidationError, match="cargo_volume"):
        CreateOrderRequest(
            **{**f_valid_order_request.dict(), "cargo_volume": -1.0}
        )

def test_create_order_empty_customer_name(f_create_order_use_case, f_valid_order_request):
    with pytest.raises(ValidationError, match="customer_name"):
        CreateOrderRequest(
            **{**f_valid_order_request.dict(), "customer_name": ""}
        )

def test_create_order_invalid_email(f_create_order_use_case, f_valid_order_request):
    with pytest.raises(ValidationError, match="customer_email"):
        CreateOrderRequest(
            **{**f_valid_order_request.dict(), "customer_email": "invalid-email"}
        ) 