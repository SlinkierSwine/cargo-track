from abc import ABC, abstractmethod
from typing import Optional, List
from entities.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate


class IWarehouseRepository(ABC):
    @abstractmethod
    def create(self, warehouse: WarehouseCreate) -> Warehouse:
        pass
    
    @abstractmethod
    def get_by_id(self, warehouse_id: str) -> Optional[Warehouse]:
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Warehouse]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Warehouse]:
        pass
    
    @abstractmethod
    def update(self, warehouse_id: str, warehouse_update: WarehouseUpdate) -> Optional[Warehouse]:
        pass
    
    @abstractmethod
    def delete(self, warehouse_id: str) -> bool:
        pass 