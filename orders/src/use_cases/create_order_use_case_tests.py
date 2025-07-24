import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from entities.order import Order, OrderCreate, OrderStatus
from use_cases.create_order_use_case import CreateOrderUseCase, CreateOrderRequest


@pytest.fixture
def m_order_repository():
    return MagicMock()


@pytest.fixture
def f_create_order_use_case(m_order_repository):
    return CreateOrderUseCase(m_order_repository)


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
        notes="Handle with care"
    )


def test_create_order_success(f_create_order_use_case, m_order_repository, f_valid_order_request):
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
    
    # Verify repository calls
    m_order_repository.create.assert_called_once()
    
    # Verify result
    assert result.customer_name == mock_order.customer_name
    assert result.customer_email == mock_order.customer_email
    assert result.customer_phone == mock_order.customer_phone
    assert result.pickup_address == mock_order.pickup_address
    assert result.delivery_address == mock_order.delivery_address
    assert result.cargo_type == mock_order.cargo_type
    assert result.cargo_weight == mock_order.cargo_weight
    assert result.cargo_volume == mock_order.cargo_volume
    assert result.status == mock_order.status
    assert result.notes == mock_order.notes


def test_create_order_invalid_cargo_weight(f_create_order_use_case, f_valid_order_request):
    # Test with invalid cargo weight
    invalid_request = CreateOrderRequest(
        customer_name=f_valid_order_request.customer_name,
        customer_email=f_valid_order_request.customer_email,
        customer_phone=f_valid_order_request.customer_phone,
        pickup_address=f_valid_order_request.pickup_address,
        delivery_address=f_valid_order_request.delivery_address,
        cargo_type=f_valid_order_request.cargo_type,
        cargo_weight=0.0,  # Invalid weight
        cargo_volume=f_valid_order_request.cargo_volume,
        notes=f_valid_order_request.notes
    )
    
    with pytest.raises(ValueError, match="Cargo weight must be greater than 0"):
        f_create_order_use_case.execute(invalid_request)


def test_create_order_invalid_cargo_volume(f_create_order_use_case, f_valid_order_request):
    # Test with invalid cargo volume
    invalid_request = CreateOrderRequest(
        customer_name=f_valid_order_request.customer_name,
        customer_email=f_valid_order_request.customer_email,
        customer_phone=f_valid_order_request.customer_phone,
        pickup_address=f_valid_order_request.pickup_address,
        delivery_address=f_valid_order_request.delivery_address,
        cargo_type=f_valid_order_request.cargo_type,
        cargo_weight=f_valid_order_request.cargo_weight,
        cargo_volume=-1.0,  # Invalid volume
        notes=f_valid_order_request.notes
    )
    
    with pytest.raises(ValueError, match="Cargo volume must be greater than 0"):
        f_create_order_use_case.execute(invalid_request)


def test_create_order_empty_customer_name(f_create_order_use_case, f_valid_order_request):
    # Test with empty customer name
    invalid_request = CreateOrderRequest(
        customer_name="",  # Empty name
        customer_email=f_valid_order_request.customer_email,
        customer_phone=f_valid_order_request.customer_phone,
        pickup_address=f_valid_order_request.pickup_address,
        delivery_address=f_valid_order_request.delivery_address,
        cargo_type=f_valid_order_request.cargo_type,
        cargo_weight=f_valid_order_request.cargo_weight,
        cargo_volume=f_valid_order_request.cargo_volume,
        notes=f_valid_order_request.notes
    )
    
    with pytest.raises(ValueError, match="Customer name cannot be empty"):
        f_create_order_use_case.execute(invalid_request)


def test_create_order_invalid_email(f_create_order_use_case, f_valid_order_request):
    # Test with invalid email
    invalid_request = CreateOrderRequest(
        customer_name=f_valid_order_request.customer_name,
        customer_email="invalid-email",  # Invalid email
        customer_phone=f_valid_order_request.customer_phone,
        pickup_address=f_valid_order_request.pickup_address,
        delivery_address=f_valid_order_request.delivery_address,
        cargo_type=f_valid_order_request.cargo_type,
        cargo_weight=f_valid_order_request.cargo_weight,
        cargo_volume=f_valid_order_request.cargo_volume,
        notes=f_valid_order_request.notes
    )
    
    with pytest.raises(ValueError, match="Invalid email format"):
        f_create_order_use_case.execute(invalid_request) 