from entities.order import Order, OrderCreate, OrderStatus
from repositories.interfaces.order_repository import OrderRepository
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from utils.warehouse_service_client import WarehouseServiceClient
from shared.events.publisher import Publisher
from use_cases.order_event_service import OrderEventService

class CreateOrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_email: EmailStr
    customer_phone: str = Field(..., min_length=1, max_length=20)
    pickup_address: str = Field(..., min_length=1)
    delivery_address: str = Field(..., min_length=1)
    cargo_type: str = Field(..., min_length=1, max_length=50)
    cargo_weight: float = Field(..., gt=0)
    cargo_volume: float = Field(..., gt=0)
    notes: Optional[str] = None
    warehouse_id: Optional[str] = None

class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository, order_event_service: OrderEventService, warehouse_service_client: Optional[WarehouseServiceClient] = None):
        self.order_repository = order_repository
        self.order_event_service = order_event_service
        self.warehouse_service_client = warehouse_service_client or WarehouseServiceClient()

    def execute(self, request: CreateOrderRequest) -> Order:
        if not request.customer_name:
            raise ValueError("Customer name cannot be empty")
        if request.cargo_weight <= 0:
            raise ValueError("Cargo weight must be greater than 0")
        if request.cargo_volume <= 0:
            raise ValueError("Cargo volume must be greater than 0")
        # Проверка склада и вместимости
        if request.warehouse_id:
            warehouse = self.warehouse_service_client.get_warehouse(request.warehouse_id)
            if not warehouse:
                raise ValueError("Warehouse not found")
            if warehouse["status"] != "active":
                raise ValueError("Warehouse is not active")
            if warehouse["available_capacity_weight"] < request.cargo_weight or warehouse["available_capacity_volume"] < request.cargo_volume:
                raise ValueError("Not enough capacity in warehouse")
        order_data = OrderCreate(
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            customer_phone=request.customer_phone,
            pickup_address=request.pickup_address,
            delivery_address=request.delivery_address,
            cargo_type=request.cargo_type,
            cargo_weight=request.cargo_weight,
            cargo_volume=request.cargo_volume,
            notes=request.notes
        )
        order = self.order_repository.create(order_data)
        
        # Event-driven: publish OrderCreated event
        order_dict = {
            "id": str(order.id),
            "customer_name": order.customer_name,
            "customer_email": order.customer_email,
            "pickup_address": order.pickup_address,
            "delivery_address": order.delivery_address,
            "cargo_type": order.cargo_type,
            "cargo_weight": order.cargo_weight,
            "cargo_volume": order.cargo_volume,
            "notes": order.notes
        }
        self.order_event_service.publish_order_created(order_dict)
        
        return order 