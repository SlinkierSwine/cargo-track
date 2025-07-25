from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from entities.user import User, UserCreate, UserUpdate


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user_data: UserCreate) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def update(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        pass
    
    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        pass
    
    @abstractmethod
    def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        pass 