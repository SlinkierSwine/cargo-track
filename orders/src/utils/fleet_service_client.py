import httpx
from typing import Optional, Dict, Any
import os

class FleetServiceClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        # Проверяем, находимся ли мы в тестовом режиме
        self.mock_mode = os.getenv("E2E_TEST_MODE", "false").lower() == "true"

    def get_vehicle(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        if self.mock_mode:
            # Возвращаем mock данные для e2e тестов
            return {
                "id": vehicle_id,
                "license_plate": "TEST123",
                "vehicle_type": "truck",
                "brand": "Test Brand",
                "model": "Test Model",
                "year": 2020,
                "capacity_weight": 1000.0,
                "capacity_volume": 10.0,
                "fuel_type": "diesel",
                "fuel_efficiency": 2.5,
                "status": "active",
                "insurance_expiry": "2025-12-31",
                "registration_expiry": "2025-12-31"
            }
        
        try:
            response = httpx.get(f"{self.base_url}/vehicles/{vehicle_id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def get_driver(self, driver_id: str) -> Optional[Dict[str, Any]]:
        if self.mock_mode:
            # Возвращаем mock данные для e2e тестов
            return {
                "id": driver_id,
                "first_name": "Test",
                "last_name": "Driver",
                "email": "test.driver@example.com",
                "phone": "+1234567890",
                "license_number": "DL123456789",
                "license_class": "C",
                "status": "active"
            }
        
        try:
            response = httpx.get(f"{self.base_url}/drivers/{driver_id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            return None 