from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from entities.route_assignment import RouteAssignment, RouteAssignmentCreate, RouteAssignmentUpdate


class IRouteAssignmentRepository(ABC):
    @abstractmethod
    def create(self, assignment: RouteAssignmentCreate) -> RouteAssignment:
        pass
    
    @abstractmethod
    def get_by_id(self, assignment_id: UUID) -> Optional[RouteAssignment]:
        pass
    
    @abstractmethod
    def get_by_route_id(self, route_id: UUID) -> List[RouteAssignment]:
        pass
    
    @abstractmethod
    def get_by_vehicle_id(self, vehicle_id: UUID) -> List[RouteAssignment]:
        pass
    
    @abstractmethod
    def get_by_driver_id(self, driver_id: UUID) -> List[RouteAssignment]:
        pass
    
    @abstractmethod
    def update(self, assignment_id: UUID, assignment: RouteAssignmentUpdate) -> Optional[RouteAssignment]:
        pass
    
    @abstractmethod
    def delete(self, assignment_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def get_all(self) -> List[RouteAssignment]:
        pass
    
    @abstractmethod
    def get_by_status(self, status: str) -> List[RouteAssignment]:
        pass 