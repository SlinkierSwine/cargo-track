import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from entities.order import Order, OrderStatus
from use_cases.change_order_status_use_case import ChangeOrderStatusUseCase, ChangeOrderStatusRequest


@pytest.fixture
def m_order_repository():
    return MagicMock()


@pytest.fixture
def f_change_order_status_use_case(m_order_repository):
    return ChangeOrderStatusUseCase(m_order_repository)


@pytest.fixture
def f_valid_change_status_request():
    return ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.IN_TRANSIT
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


def test_change_order_status_success(f_change_order_status_use_case, m_order_repository, f_valid_change_status_request, f_existing_order):
    # Mock repository responses
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
    
    # Execute use case
    result = f_change_order_status_use_case.execute(f_valid_change_status_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(f_valid_change_status_request.order_id)
    m_order_repository.update.assert_called_once()
    
    # Verify result
    assert result.status == f_valid_change_status_request.new_status


def test_change_order_status_order_not_found(f_change_order_status_use_case, m_order_repository, f_valid_change_status_request):
    # Mock repository to return None
    m_order_repository.get_by_id.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Order not found"):
        f_change_order_status_use_case.execute(f_valid_change_status_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(f_valid_change_status_request.order_id)
    m_order_repository.update.assert_not_called()


def test_change_order_status_invalid_transition(f_change_order_status_use_case, m_order_repository, f_existing_order):
    # Test invalid transition from pending to delivered
    invalid_request = ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.DELIVERED
    )
    
    # Mock order with pending status
    pending_order = Order(
        customer_name=f_existing_order.customer_name,
        customer_email=f_existing_order.customer_email,
        customer_phone=f_existing_order.customer_phone,
        pickup_address=f_existing_order.pickup_address,
        delivery_address=f_existing_order.delivery_address,
        cargo_type=f_existing_order.cargo_type,
        cargo_weight=f_existing_order.cargo_weight,
        cargo_volume=f_existing_order.cargo_volume,
        status=OrderStatus.PENDING
    )
    m_order_repository.get_by_id.return_value = pending_order
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Invalid status transition"):
        f_change_order_status_use_case.execute(invalid_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(invalid_request.order_id)
    m_order_repository.update.assert_not_called()


def test_change_order_status_to_cancelled(f_change_order_status_use_case, m_order_repository, f_existing_order):
    # Test cancelling an order
    cancel_request = ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.CANCELLED
    )
    
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
        status=OrderStatus.CANCELLED
    )
    m_order_repository.update.return_value = updated_order
    
    # Execute use case
    result = f_change_order_status_use_case.execute(cancel_request)
    
    # Verify result
    assert result.status == OrderStatus.CANCELLED


def test_change_order_status_already_cancelled(f_change_order_status_use_case, m_order_repository):
    # Test changing status of already cancelled order
    request = ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.IN_TRANSIT
    )
    
    # Mock cancelled order
    cancelled_order = Order(
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="+1234567890",
        pickup_address="123 Pickup St, City",
        delivery_address="456 Delivery Ave, City",
        cargo_type="electronics",
        cargo_weight=100.0,
        cargo_volume=2.0,
        status=OrderStatus.CANCELLED
    )
    m_order_repository.get_by_id.return_value = cancelled_order
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Cannot change status of cancelled order"):
        f_change_order_status_use_case.execute(request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(request.order_id)
    m_order_repository.update.assert_not_called()


def test_change_order_status_to_same_status(f_change_order_status_use_case, m_order_repository, f_existing_order):
    # Test changing to the same status
    same_status_request = ChangeOrderStatusRequest(
        order_id=str(uuid4()),
        new_status=OrderStatus.ASSIGNED  # Same as existing order
    )
    
    m_order_repository.get_by_id.return_value = f_existing_order
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Order is already in this status"):
        f_change_order_status_use_case.execute(same_status_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(same_status_request.order_id)
    m_order_repository.update.assert_not_called() 