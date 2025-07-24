from entities.order import Order, OrderStatus
from repositories.interfaces.order_repository import OrderRepository
from pydantic import BaseModel
from typing import Optional
from utils.fleet_service_client import FleetServiceClient
from utils.warehouse_service_client import WarehouseServiceClient
from shared.events.publisher import Publisher

class AssignVehicleRequest(BaseModel):
    order_id: str
    vehicle_id: str
    cargo_id: Optional[str] = None

class AssignVehicleUseCase:
    def __init__(self, order_repository: OrderRepository, fleet_service_client: FleetServiceClient, warehouse_service_client: Optional[WarehouseServiceClient] = None, publisher: Publisher = None):
        self.order_repository = order_repository
        self.fleet_service_client = fleet_service_client
        self.warehouse_service_client = warehouse_service_client or WarehouseServiceClient()
        self.publisher = publisher

    def execute(self, request: AssignVehicleRequest) -> Order:
        order = self.order_repository.get_by_id(request.order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status == OrderStatus.CANCELLED:
            raise ValueError("Cannot assign vehicle to cancelled order")
        # Проверка груза
        if request.cargo_id:
            cargo = self.warehouse_service_client.get_cargo(request.cargo_id)
            if not cargo:
                raise ValueError("Cargo not found")
            if cargo["status"] not in ["stored", "ready_to_ship"]:
                raise ValueError("Cargo is not ready for shipping")
        # Проверка транспорта
        vehicle = self.fleet_service_client.get_vehicle(request.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")
        if vehicle["status"] != "active":
            raise ValueError("Vehicle is not available")
        if vehicle["capacity_weight"] < order.cargo_weight or vehicle["capacity_volume"] < order.cargo_volume:
            raise ValueError("Insufficient vehicle capacity")
        # Назначение транспорта
        order.vehicle_id = request.vehicle_id
        order.status = OrderStatus.ASSIGNED
        updated_order = self.order_repository.update(request.order_id, order)
        # Event-driven: publish order.vehicle_assigned
        if self.publisher:
            self.publisher.publish("order.vehicle_assigned", {
                "order_id": str(updated_order.id),
                "vehicle_id": str(updated_order.vehicle_id),
                "customer_email": updated_order.customer_email
            })
        return updated_order 