from abc import ABC, abstractmethod
from typing import Optional, List
from entities.cargo import Cargo, CargoCreate, CargoUpdate


class CargoRepositoryInterface(ABC):
    @abstractmethod
    def create(self, cargo: CargoCreate) -> Cargo:
        pass
    
    @abstractmethod
    def get_by_id(self, cargo_id: str) -> Optional[Cargo]:
        pass
    
    @abstractmethod
    def get_by_tracking_number(self, tracking_number: str) -> Optional[Cargo]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Cargo]:
        pass
    
    @abstractmethod
    def list_cargo(self, skip: int = 0, limit: int = 100) -> List[Cargo]:
        pass
    
    @abstractmethod
    def update(self, cargo_id: str, cargo_update: CargoUpdate) -> Optional[Cargo]:
        pass
    
    @abstractmethod
    def delete(self, cargo_id: str) -> bool:
        pass 