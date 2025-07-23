from abc import ABC, abstractmethod
from typing import Optional, List
from entities.vehicle import Vehicle, VehicleCreate, VehicleUpdate


class IVehicleRepository(ABC):
    @abstractmethod
    def create(self, vehicle: VehicleCreate) -> Vehicle:
        pass
    
    @abstractmethod
    def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        pass
    
    @abstractmethod
    def get_by_license_plate(self, license_plate: str) -> Optional[Vehicle]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Vehicle]:
        pass
    
    @abstractmethod
    def update(self, vehicle_id: str, vehicle: VehicleUpdate) -> Optional[Vehicle]:
        pass
    
    @abstractmethod
    def delete(self, vehicle_id: str) -> bool:
        pass 