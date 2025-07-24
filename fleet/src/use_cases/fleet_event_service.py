from typing import Dict, Any, List, Optional
from datetime import datetime
from uuid import uuid4
import structlog
from shared.events.publisher import Publisher
from shared.events.subscriber import Subscriber
from repositories.interfaces.driver_repository import IDriverRepository
from repositories.interfaces.vehicle_repository import IVehicleRepository


class FleetEventService:
    def __init__(self, publisher: Publisher, subscriber: Subscriber, 
                 driver_repository: IDriverRepository, vehicle_repository: IVehicleRepository):
        self.publisher = publisher
        self.subscriber = subscriber
        self.driver_repository = driver_repository
        self.vehicle_repository = vehicle_repository
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    def handle_order_created(self, event_data: Dict[str, Any]) -> None:
        """Handle OrderCreated event from orders service"""
        try:
            order_id = event_data["order_id"]
            cargo_weight = event_data["cargo_weight"]
            cargo_volume = event_data["cargo_volume"]
            
            self.logger.info("Processing OrderCreated event", order_id=order_id)
            
            # Get available drivers
            available_drivers = self.driver_repository.get_available_drivers()
            if not available_drivers:
                self._publish_no_vehicle_available(order_id, "no_drivers")
                return
            
            # Get available vehicles that can handle the cargo
            available_vehicles = self.vehicle_repository.get_available_vehicles()
            if not available_vehicles:
                self._publish_no_vehicle_available(order_id, "no_vehicles")
                return
            
            suitable_vehicles = [
                v for v in available_vehicles 
                if v.capacity_weight >= cargo_weight and v.capacity_volume >= cargo_volume
            ]
            
            if not suitable_vehicles:
                self._publish_no_vehicle_available(order_id, "capacity_mismatch")
                return
            
            # Assign the first available driver and suitable vehicle
            selected_driver = available_drivers[0]
            selected_vehicle = suitable_vehicles[0]
            
            self._publish_vehicle_assigned(order_id, selected_vehicle, selected_driver)
            
        except Exception as e:
            self.logger.error("Failed to handle OrderCreated event", error=str(e), order_id=event_data.get("order_id"))
            raise
    
    def _publish_vehicle_assigned(self, order_id: str, vehicle, driver) -> None:
        """Publish VehicleAssigned event"""
        try:
            event_data = {
                "event_id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source_service": "fleet",
                "order_id": order_id,
                "vehicle_id": str(vehicle.id),
                "driver_id": str(driver.id),
                "vehicle_license_plate": vehicle.license_plate,
                "driver_name": f"{driver.first_name} {driver.last_name}",
                "estimated_delivery_time": None  # TODO: Calculate based on distance
            }
            
            self.publisher.publish("vehicle_assigned", event_data)
            self.logger.info("VehicleAssigned event published", 
                           order_id=order_id, 
                           vehicle_id=str(vehicle.id), 
                           driver_id=str(driver.id))
        except Exception as e:
            self.logger.error("Failed to publish VehicleAssigned event", error=str(e), order_id=order_id)
            raise
    
    def _publish_no_vehicle_available(self, order_id: str, reason: str) -> None:
        """Publish NoVehicleAvailable event"""
        try:
            event_data = {
                "event_id": str(uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source_service": "fleet",
                "order_id": order_id,
                "reason": reason
            }
            
            self.publisher.publish("no_vehicle_available", event_data)
            self.logger.info("NoVehicleAvailable event published", order_id=order_id, reason=reason)
        except Exception as e:
            self.logger.error("Failed to publish NoVehicleAvailable event", error=str(e), order_id=order_id)
            raise
    
    def start_listening(self) -> None:
        """Start listening for events from other services"""
        try:
            # Subscribe to events from orders service
            self.subscriber.subscribe("order_created", self.handle_order_created)
            
            # Start listening
            self.subscriber.start_listening()
            self.logger.info("Started listening for events")
        except Exception as e:
            self.logger.error("Failed to start listening for events", error=str(e))
            raise 