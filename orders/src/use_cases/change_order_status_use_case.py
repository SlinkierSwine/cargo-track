from entities.order import Order, OrderStatus
from repositories.interfaces.order_repository import OrderRepository
from pydantic import BaseModel
from typing import Optional
from utils.warehouse_service_client import WarehouseServiceClient
from shared.events.publisher import Publisher
import httpx

class ChangeOrderStatusRequest(BaseModel):
    order_id: str
    new_status: OrderStatus
    cargo_id: Optional[str] = None

class ChangeOrderStatusUseCase:
    def __init__(self, order_repository: OrderRepository, warehouse_service_client: Optional[WarehouseServiceClient] = None, publisher: Publisher = None):
        self.order_repository = order_repository
        self.warehouse_service_client = warehouse_service_client or WarehouseServiceClient()
        self.publisher = publisher

    def execute(self, request: ChangeOrderStatusRequest) -> Order:
        order = self.order_repository.get_by_id(request.order_id)
        if not order:
            raise ValueError("Order not found")
        # Проверка валидности перехода статуса
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.ASSIGNED, OrderStatus.CANCELLED],
            OrderStatus.ASSIGNED: [OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED],
            OrderStatus.IN_TRANSIT: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
            OrderStatus.DELIVERED: [],
            OrderStatus.CANCELLED: []
        }
        if request.new_status not in valid_transitions.get(order.status, []):
            raise ValueError("Invalid status transition")
        # Обновление статуса заказа
        order.status = request.new_status
        updated_order = self.order_repository.update(request.order_id, order)
        # Обновление статуса груза в warehouse service
        if request.cargo_id and self.warehouse_service_client:
            self._update_cargo_status(request.cargo_id, request.new_status)
        # Event-driven: publish order.status_changed
        if self.publisher:
            self.publisher.publish("order.status_changed", {
                "order_id": str(updated_order.id),
                "old_status": order.status,
                "new_status": str(updated_order.status),
                "customer_email": updated_order.customer_email
            })
        return updated_order

    def _update_cargo_status(self, cargo_id: str, order_status: OrderStatus):
        cargo_status_map = {
            OrderStatus.IN_TRANSIT: "shipped",
            OrderStatus.DELIVERED: "delivered"
        }
        if order_status in cargo_status_map:
            self.warehouse_service_client.update_cargo_status(cargo_id, cargo_status_map[order_status]) 