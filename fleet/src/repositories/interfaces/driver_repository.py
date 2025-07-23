from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from entities.driver import Driver, DriverCreate, DriverUpdate


class IDriverRepository(ABC):
    @abstractmethod
    def create(self, driver: DriverCreate) -> Driver:
        pass
    
    @abstractmethod
    def get_by_id(self, driver_id: UUID) -> Optional[Driver]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Driver]:
        pass
    
    @abstractmethod
    def get_by_license_number(self, license_number: str) -> Optional[Driver]:
        pass
    
    @abstractmethod
    def update(self, driver_id: UUID, driver: DriverUpdate) -> Optional[Driver]:
        pass
    
    @abstractmethod
    def delete(self, driver_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Driver]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Driver]:
        pass
    
    @abstractmethod
    def get_available_drivers(self) -> List[Driver]:
        pass 