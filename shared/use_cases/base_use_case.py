from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
import structlog

T = TypeVar('T')


class BaseUseCase(ABC, Generic[T]):
    def __init__(self) -> None:
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> T:
        pass 