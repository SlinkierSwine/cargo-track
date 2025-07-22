from typing import Optional
from uuid import UUID
from shared.use_cases.base_use_case import BaseUseCase
from entities.user import User, UserCreate, UserResponse
from repositories.user_repository import UserRepository


class RegisterUserUseCase(BaseUseCase[UserResponse]):
    def __init__(self, user_repository: UserRepository):
        super().__init__()
        self.user_repository = user_repository
    
    async def execute(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        existing_username = await self.user_repository.get_by_username(user_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        # Create new user
        user = await self.user_repository.create(user_data)
        
        return UserResponse.from_orm(user) 