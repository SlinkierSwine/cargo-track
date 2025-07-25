import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from entities.order import Order, OrderStatus
from repositories.order_repository import OrderRepository
from use_cases.assign_vehicle_use_case import AssignVehicleUseCase, AssignVehicleRequest
from shared.events.publisher import Publisher


@pytest.fixture
def m_order_repository():
    return MagicMock()


@pytest.fixture
def m_fleet_service_client():
    return MagicMock()


@pytest.fixture
def m_warehouse_service_client():
    return MagicMock()


@pytest.fixture
def m_publisher():
    return MagicMock(spec=Publisher)


@pytest.fixture
def f_assign_vehicle_use_case(m_order_repository, m_fleet_service_client, m_warehouse_service_client, m_publisher):
    return AssignVehicleUseCase(m_order_repository, m_fleet_service_client, m_warehouse_service_client, m_publisher)


@pytest.fixture
def f_valid_assign_vehicle_request():
    return AssignVehicleRequest(
        order_id=str(uuid4()),
        vehicle_id=str(uuid4()),
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
        status=OrderStatus.PENDING
    )


def test_assign_vehicle_success(f_assign_vehicle_use_case, m_order_repository, m_fleet_service_client, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = {"id": f_valid_assign_vehicle_request.cargo_id, "status": "stored"}
    updated_order = Order(
        customer_name=f_existing_order.customer_name,
        customer_email=f_existing_order.customer_email,
        customer_phone=f_existing_order.customer_phone,
        pickup_address=f_existing_order.pickup_address,
        delivery_address=f_existing_order.delivery_address,
        cargo_type=f_existing_order.cargo_type,
        cargo_weight=f_existing_order.cargo_weight,
        cargo_volume=f_existing_order.cargo_volume,
        status=OrderStatus.ASSIGNED,
        vehicle_id=uuid4()
    )
    m_order_repository.update.return_value = updated_order
    m_fleet_service_client.get_vehicle.return_value = {
        "id": f_valid_assign_vehicle_request.vehicle_id,
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "status": "active"
    }
    result = f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)
    m_warehouse_service_client.get_cargo.assert_called_once_with(f_valid_assign_vehicle_request.cargo_id)
    m_fleet_service_client.get_vehicle.assert_called_once_with(f_valid_assign_vehicle_request.vehicle_id)
    assert result.vehicle_id == updated_order.vehicle_id
    assert result.status == OrderStatus.ASSIGNED


def test_assign_vehicle_order_not_found(f_assign_vehicle_use_case, m_order_repository, f_valid_assign_vehicle_request):
    # Mock repository to return None
    m_order_repository.get_by_id.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Order not found"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(f_valid_assign_vehicle_request.order_id)
    m_order_repository.update.assert_not_called()


def test_assign_vehicle_order_already_cancelled(f_assign_vehicle_use_case, m_order_repository, f_valid_assign_vehicle_request):
    # Mock order with cancelled status
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
    with pytest.raises(ValueError, match="Cannot assign vehicle to cancelled order"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)
    
    # Verify repository calls
    m_order_repository.get_by_id.assert_called_once_with(f_valid_assign_vehicle_request.order_id)
    m_order_repository.update.assert_not_called()


def test_assign_vehicle_vehicle_not_found(f_assign_vehicle_use_case, m_order_repository, m_fleet_service_client, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = {"id": f_valid_assign_vehicle_request.cargo_id, "status": "stored"}
    m_fleet_service_client.get_vehicle.return_value = None
    with pytest.raises(ValueError, match="Vehicle not found"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)


def test_assign_vehicle_vehicle_not_available(f_assign_vehicle_use_case, m_order_repository, m_fleet_service_client, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = {"id": f_valid_assign_vehicle_request.cargo_id, "status": "stored"}
    m_fleet_service_client.get_vehicle.return_value = {
        "id": f_valid_assign_vehicle_request.vehicle_id,
        "capacity_weight": 20000.0,
        "capacity_volume": 80.0,
        "status": "maintenance"
    }
    with pytest.raises(ValueError, match="Vehicle is not available"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)


def test_assign_vehicle_insufficient_capacity(f_assign_vehicle_use_case, m_order_repository, m_fleet_service_client, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = {"id": f_valid_assign_vehicle_request.cargo_id, "status": "stored"}
    m_fleet_service_client.get_vehicle.return_value = {
        "id": f_valid_assign_vehicle_request.vehicle_id,
        "capacity_weight": 50.0,  # Less than cargo weight (100.0)
        "capacity_volume": 80.0,
        "status": "active"
    }
    with pytest.raises(ValueError, match="Insufficient vehicle capacity"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)


def test_assign_vehicle_cargo_not_found(f_assign_vehicle_use_case, m_order_repository, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = None
    with pytest.raises(ValueError, match="Cargo not found"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request)


def test_assign_vehicle_cargo_not_ready(f_assign_vehicle_use_case, m_order_repository, m_warehouse_service_client, f_valid_assign_vehicle_request, f_existing_order):
    m_order_repository.get_by_id.return_value = f_existing_order
    m_warehouse_service_client.get_cargo.return_value = {"id": f_valid_assign_vehicle_request.cargo_id, "status": "damaged"}
    with pytest.raises(ValueError, match="Cargo is not ready for shipping"):
        f_assign_vehicle_use_case.execute(f_valid_assign_vehicle_request) 