import pytest
from uuid import uuid4
from datetime import datetime

from entities.order import Order, OrderCreate, OrderUpdate, OrderStatus
from repositories.order_repository import OrderRepository


@pytest.fixture
def f_order_create_data():
    return OrderCreate(
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


@pytest.fixture
def f_order_update_data():
    return OrderUpdate(
        customer_name="Jane Doe",
        cargo_weight=150.0,
        notes="Updated notes"
    )


def test_create_order(f_order_repository: OrderRepository, f_order_create_data: OrderCreate):
    order = f_order_repository.create(f_order_create_data)
    
    assert order.id is not None
    assert order.customer_name == f_order_create_data.customer_name
    assert order.customer_email == f_order_create_data.customer_email
    assert order.customer_phone == f_order_create_data.customer_phone
    assert order.pickup_address == f_order_create_data.pickup_address
    assert order.delivery_address == f_order_create_data.delivery_address
    assert order.cargo_type == f_order_create_data.cargo_type
    assert order.cargo_weight == f_order_create_data.cargo_weight
    assert order.cargo_volume == f_order_create_data.cargo_volume
    assert order.status == OrderStatus.PENDING
    assert order.notes == f_order_create_data.notes


def test_get_by_id(f_order_repository: OrderRepository, f_order_create_data: OrderCreate):
    created_order = f_order_repository.create(f_order_create_data)
    order = f_order_repository.get_by_id(str(created_order.id))
    
    assert order is not None
    assert order.id == created_order.id
    assert order.customer_name == created_order.customer_name


def test_get_by_id_not_found(f_order_repository: OrderRepository):
    order = f_order_repository.get_by_id(str(uuid4()))
    assert order is None


def test_update_order(f_order_repository: OrderRepository, f_order_create_data: OrderCreate, f_order_update_data: OrderUpdate):
    created_order = f_order_repository.create(f_order_create_data)
    updated_order = f_order_repository.update(str(created_order.id), f_order_update_data)
    
    assert updated_order is not None
    assert updated_order.id == created_order.id
    assert updated_order.customer_name == f_order_update_data.customer_name
    assert updated_order.cargo_weight == f_order_update_data.cargo_weight
    assert updated_order.notes == f_order_update_data.notes
    assert updated_order.customer_email == created_order.customer_email  # unchanged


def test_update_order_not_found(f_order_repository: OrderRepository, f_order_update_data: OrderUpdate):
    order = f_order_repository.update(str(uuid4()), f_order_update_data)
    assert order is None


def test_delete_order(f_order_repository: OrderRepository, f_order_create_data: OrderCreate):
    created_order = f_order_repository.create(f_order_create_data)
    deleted = f_order_repository.delete(str(created_order.id))
    
    assert deleted is True
    
    # Verify order is deleted
    order = f_order_repository.get_by_id(str(created_order.id))
    assert order is None


def test_delete_order_not_found(f_order_repository: OrderRepository):
    deleted = f_order_repository.delete(str(uuid4()))
    assert deleted is False


def test_get_all_orders(f_order_repository: OrderRepository):
    # Create multiple orders
    order1_data = OrderCreate(
        customer_name="Customer 1",
        customer_email="customer1@example.com",
        customer_phone="+1111111111",
        pickup_address="Address 1",
        delivery_address="Address 2",
        cargo_type="cargo1",
        cargo_weight=50.0,
        cargo_volume=1.0
    )
    
    order2_data = OrderCreate(
        customer_name="Customer 2",
        customer_email="customer2@example.com",
        customer_phone="+2222222222",
        pickup_address="Address 3",
        delivery_address="Address 4",
        cargo_type="cargo2",
        cargo_weight=75.0,
        cargo_volume=1.5
    )
    
    f_order_repository.create(order1_data)
    f_order_repository.create(order2_data)
    
    orders = f_order_repository.get_all()
    assert len(orders) >= 2


def test_get_by_status(f_order_repository: OrderRepository, f_order_create_data: OrderCreate):
    created_order = f_order_repository.create(f_order_create_data)
    
    # Update status to assigned
    update_data = OrderUpdate(status=OrderStatus.ASSIGNED)
    f_order_repository.update(str(created_order.id), update_data)
    
    assigned_orders = f_order_repository.get_by_status(OrderStatus.ASSIGNED)
    assert len(assigned_orders) >= 1
    assert assigned_orders[0].status == OrderStatus.ASSIGNED


def test_get_by_customer_email(f_order_repository: OrderRepository, f_order_create_data: OrderCreate):
    created_order = f_order_repository.create(f_order_create_data)
    
    customer_orders = f_order_repository.get_by_customer_email(f_order_create_data.customer_email)
    assert len(customer_orders) >= 1
    assert customer_orders[0].customer_email == f_order_create_data.customer_email 