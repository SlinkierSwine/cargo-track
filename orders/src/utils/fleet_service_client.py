import httpx
from config.settings import get_settings

class FleetServiceClient:
    def __init__(self):
        self.base_url = get_settings().fleet_service_url

    def get_vehicle(self, vehicle_id: str) -> dict:
        url = f"{self.base_url}/vehicles/{vehicle_id}"
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_driver(self, driver_id: str) -> dict:
        url = f"{self.base_url}/drivers/{driver_id}"
        response = httpx.get(url)
        if response.status_code == 200:
            return response.json()
        return None 