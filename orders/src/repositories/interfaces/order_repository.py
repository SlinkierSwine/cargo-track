from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from entities.order import Order, OrderCreate, OrderUpdate


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order_data: OrderCreate) -> Order:
        pass
    
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        pass
    
    @abstractmethod
    def update(self, order_id: str, order_data: OrderUpdate) -> Optional[Order]:
        pass
    
    @abstractmethod
    def delete(self, order_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[Order]:
        pass
    
    @abstractmethod
    def get_by_customer_email(self, email: str) -> List[Order]:
        pass 