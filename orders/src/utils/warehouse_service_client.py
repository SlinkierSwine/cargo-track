import httpx
from config.settings import get_settings
from typing import Optional

class WarehouseServiceClient:
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url

    def get_warehouse(self, warehouse_id: str) -> Optional[dict]:
        try:
            response = httpx.get(f"{self.base_url}/warehouses/{warehouse_id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def get_cargo(self, cargo_id: str) -> Optional[dict]:
        try:
            response = httpx.get(f"{self.base_url}/cargo/{cargo_id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def update_cargo_status(self, cargo_id: str, new_status: str) -> bool:
        try:
            response = httpx.put(f"{self.base_url}/cargo/{cargo_id}/status", json={"new_status": new_status})
            response.raise_for_status()
            return True
        except Exception:
            return False 