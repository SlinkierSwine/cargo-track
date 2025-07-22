from typing import Optional
from entities.user import User
from entities.token import Token
from repositories.user_repository import UserRepository
from shared.use_cases.base_use_case import BaseUseCase
from utils.password_utils import verify_password
from utils.token_utils import create_access_token


class AuthenticateUserUseCase(BaseUseCase[Token]):
    def __init__(self, user_repository: UserRepository):
        super().__init__()
        self.user_repository = user_repository
    
    async def execute(self, email: str, password: str) -> Token:
        # Find user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is deactivated")
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id), "username": user.username, "role": user.role.value})
        
        return Token(access_token=access_token, token_type="bearer") 