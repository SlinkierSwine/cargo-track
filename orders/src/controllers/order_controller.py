from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from entities.order import Order, OrderCreate, OrderUpdate, OrderStatus
from repositories.order_repository import OrderRepository
from config.database import get_db
from sqlalchemy.orm import Session
from use_cases.create_order_use_case import CreateOrderUseCase, CreateOrderRequest
from use_cases.assign_vehicle_use_case import AssignVehicleUseCase, AssignVehicleRequest
from use_cases.change_order_status_use_case import ChangeOrderStatusUseCase, ChangeOrderStatusRequest
from use_cases.order_event_service import OrderEventService
from utils.fleet_service_client import FleetServiceClient
from utils.warehouse_service_client import WarehouseServiceClient
from shared.events.publisher import Publisher
from config.settings import get_settings
from utils.auth_utils import get_current_user, require_any_role

router = APIRouter()

def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)

def get_fleet_service_client() -> FleetServiceClient:
    return FleetServiceClient()

def get_warehouse_service_client() -> WarehouseServiceClient:
    settings = get_settings()
    return WarehouseServiceClient(settings.warehouse_service_url)

def get_publisher(request: Request) -> Publisher:
    return request.app.state.publisher

def get_order_event_service(request: Request) -> OrderEventService:
    return request.app.state.order_event_service

@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(
    request: dict, 
    repo: OrderRepository = Depends(get_order_repository), 
    warehouse_client: WarehouseServiceClient = Depends(get_warehouse_service_client), 
    order_event_service: OrderEventService = Depends(get_order_event_service),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"]))
):
    use_case = CreateOrderUseCase(repo, order_event_service, warehouse_client)
    try:
        return use_case.execute(CreateOrderRequest(**request))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/orders/{order_id}", response_model=Order)
def get_order(
    order_id: str, 
    repo: OrderRepository = Depends(get_order_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver", "client"]))
):
    order = repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders", response_model=List[Order])
def list_orders(
    repo: OrderRepository = Depends(get_order_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"]))
):
    return repo.get_all()

@router.put("/orders/{order_id}", response_model=Order)
def update_order(
    order_id: str, 
    update: OrderUpdate, 
    repo: OrderRepository = Depends(get_order_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    order = repo.update(order_id, update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: str, 
    repo: OrderRepository = Depends(get_order_repository),
    current_user: dict = Depends(require_any_role(["admin"]))
):
    deleted = repo.delete(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return

# --- Assignment ---
@router.post("/orders/{order_id}/assign-vehicle", response_model=Order)
def assign_vehicle(
    order_id: str, 
    data: dict, 
    repo: OrderRepository = Depends(get_order_repository), 
    fleet_client: FleetServiceClient = Depends(get_fleet_service_client), 
    warehouse_client: WarehouseServiceClient = Depends(get_warehouse_service_client), 
    publisher: Publisher = Depends(get_publisher),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    use_case = AssignVehicleUseCase(repo, fleet_client, warehouse_client, publisher)
    req = AssignVehicleRequest(order_id=order_id, vehicle_id=data["vehicle_id"], cargo_id=data.get("cargo_id"))
    return use_case.execute(req)

# --- Status Management ---
@router.put("/orders/{order_id}/status", response_model=Order)
def change_status(
    order_id: str, 
    data: dict, 
    repo: OrderRepository = Depends(get_order_repository), 
    warehouse_client: WarehouseServiceClient = Depends(get_warehouse_service_client), 
    publisher: Publisher = Depends(get_publisher),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"]))
):
    use_case = ChangeOrderStatusUseCase(repo, warehouse_client, publisher)
    req = ChangeOrderStatusRequest(order_id=order_id, new_status=data["new_status"], cargo_id=data.get("cargo_id"))
    return use_case.execute(req)

@router.post("/orders/{order_id}/complete-delivery", response_model=Order)
def complete_delivery(
    order_id: str, 
    data: dict = None, 
    repo: OrderRepository = Depends(get_order_repository), 
    warehouse_client: WarehouseServiceClient = Depends(get_warehouse_service_client), 
    publisher: Publisher = Depends(get_publisher),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"]))
):
    use_case = ChangeOrderStatusUseCase(repo, warehouse_client, publisher)
    cargo_id = data["cargo_id"] if data and "cargo_id" in data else None
    req = ChangeOrderStatusRequest(order_id=order_id, new_status=OrderStatus.DELIVERED, cargo_id=cargo_id)
    return use_case.execute(req)

@router.post("/orders/{order_id}/cancel", response_model=Order)
def cancel_order(
    order_id: str, 
    repo: OrderRepository = Depends(get_order_repository),
    publisher: Publisher = Depends(get_publisher),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    use_case = ChangeOrderStatusUseCase(repo, publisher=publisher)
    req = ChangeOrderStatusRequest(order_id=order_id, new_status=OrderStatus.CANCELLED)
    return use_case.execute(req) 