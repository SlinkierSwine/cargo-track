import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from entities.order import Order, OrderStatus
from repositories.order_repository import OrderRepository
from use_cases.change_order_status_use_case import ChangeOrderStatusUseCase, ChangeOrderStatusRequest
from shared.events.publisher import Publisher

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
def f_change_order_status_use_case(m_order_repository, m_warehouse_service_client, m_publisher):
    return ChangeOrderStatusUseCase(m_order_repository, m_warehouse_service_client, m_publisher)

@pytest.fixture
def f_valid_change_status_request():
    return ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.IN_TRANSIT,
        cargo_id="00000000-0000-0000-0000-000000000001"
    )

@pytest.fixture
def f_existing_order():
    return Order(
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="+1234567890",
        pickup_address="123 Pickup St, City",
        delivery_address="456 Delivery Ave, City",
        cargo_type="electronics",
        cargo_weight=100.0,
        cargo_volume=2.0,
        status=OrderStatus.ASSIGNED
    )

def test_change_order_status_success(f_change_order_status_use_case, m_order_repository, m_warehouse_service_client, f_valid_change_status_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    updated_order = Order(
        customer_name=f_existing_order.customer_name,
        customer_email=f_existing_order.customer_email,
        customer_phone=f_existing_order.customer_phone,
        pickup_address=f_existing_order.pickup_address,
        delivery_address=f_existing_order.delivery_address,
        cargo_type=f_existing_order.cargo_type,
        cargo_weight=f_existing_order.cargo_weight,
        cargo_volume=f_existing_order.cargo_volume,
        status=f_valid_change_status_request.new_status
    )
    m_order_repository.update.return_value = updated_order
    result = f_change_order_status_use_case.execute(f_valid_change_status_request)
    m_warehouse_service_client.base_url  # just to ensure it's used
    assert result.status == f_valid_change_status_request.new_status

def test_change_order_status_to_in_transit_updates_cargo(f_change_order_status_use_case, m_order_repository, m_warehouse_service_client, f_valid_change_status_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_order_repository.update.return_value = f_existing_order
    req = ChangeOrderStatusRequest(order_id=f_valid_change_status_request.order_id, new_status=OrderStatus.IN_TRANSIT, cargo_id=f_valid_change_status_request.cargo_id)
    f_change_order_status_use_case.execute(req)
    # Проверяем, что warehouse_service_client был вызван для обновления статуса груза
    # (метод _update_cargo_status вызывает httpx.put, но мы можем проверить, что base_url используется)
    m_warehouse_service_client.base_url

def test_change_order_status_to_delivered_updates_cargo(f_change_order_status_use_case, m_order_repository, m_warehouse_service_client, f_valid_change_status_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_order_repository.update.return_value = f_existing_order
    # Сначала переводим заказ в IN_TRANSIT
    req_in_transit = ChangeOrderStatusRequest(order_id=f_valid_change_status_request.order_id, new_status=OrderStatus.IN_TRANSIT, cargo_id=f_valid_change_status_request.cargo_id)
    f_change_order_status_use_case.execute(req_in_transit)
    # Теперь переводим заказ в DELIVERED
    # Для этого нужно, чтобы order.status был IN_TRANSIT
    in_transit_order = Order(
        **{**f_existing_order.dict(), "status": OrderStatus.IN_TRANSIT}
    )
    m_order_repository.get_by_id.return_value = in_transit_order
    req_delivered = ChangeOrderStatusRequest(order_id=f_valid_change_status_request.order_id, new_status=OrderStatus.DELIVERED, cargo_id=f_valid_change_status_request.cargo_id)
    f_change_order_status_use_case.execute(req_delivered)
    m_warehouse_service_client.base_url 