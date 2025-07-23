import httpx
from typing import Optional, Dict, Any
from config.settings import get_settings
from utils.auth_utils import get_auth_service_client


class FleetServiceClient:
    def __init__(self):
        self.settings = get_settings()
        # In Docker, use the service name, otherwise use localhost
        import os
        if os.getenv("DOCKER_ENV"):
            self.base_url = "http://fleet-fleet-service-1:8000"  # Docker service name
        else:
            self.base_url = "http://localhost:8001"  # Local development
        self.auth_client = get_auth_service_client()
    
    async def get_vehicle(self, vehicle_id: str, token: str) -> Optional[Dict[str, Any]]:
        """Get vehicle information from fleet service"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {token}"}
                response = await client.get(f"{self.base_url}/vehicles/{vehicle_id}", headers=headers)
                if response.status_code == 200:
                    vehicle_data = response.json()
                    return {
                        "id": vehicle_data["id"],
                        "capacity_weight": vehicle_data["capacity_weight"],
                        "capacity_volume": vehicle_data["capacity_volume"],
                        "temperature_controlled": self._is_temperature_controlled(vehicle_data),
                        "hazardous_materials_certified": self._is_hazardous_certified(vehicle_data),
                        "special_equipment": self._get_special_equipment(vehicle_data)
                    }
                return None
        except Exception:
            return None
    
    def _is_temperature_controlled(self, vehicle_data: Dict[str, Any]) -> bool:
        """Check if vehicle has temperature control capabilities"""
        # This would be based on vehicle type or special equipment
        vehicle_type = vehicle_data.get("vehicle_type", "")
        return vehicle_type in ["refrigerated_truck", "temperature_controlled"]
    
    def _is_hazardous_certified(self, vehicle_data: Dict[str, Any]) -> bool:
        """Check if vehicle is certified for hazardous materials"""
        # This would be based on vehicle certifications
        return vehicle_data.get("hazardous_certified", False)
    
    def _get_special_equipment(self, vehicle_data: Dict[str, Any]) -> list:
        """Get special equipment available on the vehicle"""
        # This would be based on vehicle equipment
        return vehicle_data.get("special_equipment", [])


class FleetServiceInterface:
    """Synchronous interface for fleet service"""
    
    def __init__(self):
        self.client = FleetServiceClient()
    
    def get_vehicle(self, vehicle_id: str, token: str) -> Optional[Dict[str, Any]]:
        """Get vehicle information synchronously"""
        import asyncio
        try:
            return asyncio.run(self.client.get_vehicle(vehicle_id, token))
        except Exception:
            # Fallback to mock data if service is unavailable
            return {
                "id": vehicle_id,
                "capacity_weight": 5000.0,
                "capacity_volume": 50.0,
                "temperature_controlled": True,
                "hazardous_materials_certified": True,
                "special_equipment": ["forklift", "crane"]
            } 