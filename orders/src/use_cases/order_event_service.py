from typing import Dict, Any
from datetime import datetime
from uuid import uuid4
import structlog
from shared.events.publisher import Publisher
from shared.events.subscriber import Subscriber
from repositories.order_repository import OrderRepository
from sqlalchemy.orm import Session


class OrderEventService:
    def __init__(self, publisher: Publisher, subscriber: Subscriber, order_repository: OrderRepository):
        self.publisher = publisher
        self.subscriber = subscriber
        self.order_repository = order_repository
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    def publish_order_created(self, order_data: Dict[str, Any]) -> None:
        """Publish OrderCreated event when a new order is created"""
        try:
            event_data = {
                "event_id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source_service": "orders",
                "order_id": order_data["id"],
                "customer_name": order_data["customer_name"],
                "customer_email": order_data["customer_email"],
                "pickup_address": order_data["pickup_address"],
                "delivery_address": order_data["delivery_address"],
                "cargo_type": order_data["cargo_type"],
                "cargo_weight": order_data["cargo_weight"],
                "cargo_volume": order_data["cargo_volume"],
                "notes": order_data.get("notes")
            }
            
            self.publisher.publish("order_created", event_data)
            self.logger.info("OrderCreated event published", order_id=order_data["id"])
        except Exception as e:
            self.logger.error("Failed to publish OrderCreated event", error=str(e), order_id=order_data["id"])
            raise
    
    def handle_vehicle_assigned(self, event_data: Dict[str, Any]) -> None:
        """Handle VehicleAssigned event from fleet service"""
        try:
            order_id = event_data["order_id"]
            vehicle_id = event_data["vehicle_id"]
            driver_id = event_data["driver_id"]
            
            # Update order with vehicle and driver assignment
            from entities.order import OrderUpdate
            update_data = OrderUpdate(
                vehicle_id=vehicle_id,
                driver_id=driver_id,
                status="assigned"
            )
            
            updated_order = self.order_repository.update(order_id, update_data)
            if updated_order:
                self.logger.info("Order updated with vehicle assignment", 
                               order_id=order_id, 
                               vehicle_id=vehicle_id, 
                               driver_id=driver_id)
            else:
                self.logger.error("Failed to update order with vehicle assignment", order_id=order_id)
        except Exception as e:
            self.logger.error("Failed to handle VehicleAssigned event", error=str(e))
            raise
    
    def handle_no_vehicle_available(self, event_data: Dict[str, Any]) -> None:
        """Handle NoVehicleAvailable event from fleet service"""
        try:
            order_id = event_data["order_id"]
            reason = event_data["reason"]
            
            # Update order status based on reason
            from entities.order import OrderUpdate
            status = "cancelled" if reason in ["no_drivers", "no_vehicles"] else "pending"
            update_data = OrderUpdate(status=status)
            
            updated_order = self.order_repository.update(order_id, update_data)
            if updated_order:
                self.logger.info("Order status updated", 
                               order_id=order_id, 
                               reason=reason,
                               status=status)
            else:
                self.logger.error("Failed to update order status", order_id=order_id)
        except Exception as e:
            self.logger.error("Failed to handle NoVehicleAvailable event", error=str(e))
            raise
    
    def start_listening(self) -> None:
        """Start listening for events from other services"""
        try:
            # Subscribe to events from fleet service
            self.subscriber.subscribe("vehicle_assigned", self.handle_vehicle_assigned)
            self.subscriber.subscribe("no_vehicle_available", self.handle_no_vehicle_available)
            
            # Start listening
            self.subscriber.start_listening()
            self.logger.info("Started listening for events")
        except Exception as e:
            self.logger.error("Failed to start listening for events", error=str(e))
            raise 