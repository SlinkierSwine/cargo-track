from pydantic import BaseModel, EmailStr, Field
from entities.user import User
from entities.token import Token
from repositories.interfaces.user_repository import IUserRepository
from utils.password_utils import verify_password
from utils.token_utils import create_access_token


class AuthenticateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class AuthenticateUserResponse(BaseModel):
    access_token: str
    token_type: str


class AuthenticateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, request: AuthenticateUserRequest) -> AuthenticateUserResponse:
        user = self.user_repository.get_by_email(request.email)
        if not user:
            raise ValueError("Invalid email or password")
        
        if not verify_password(request.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        if not user.is_active:
            raise ValueError("User account is disabled")
        
        # Включаем роль пользователя в токен
        access_token = create_access_token(data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        })
        token = Token(access_token=access_token, token_type="bearer")
        
        return AuthenticateUserResponse(
            access_token=token.access_token,
            token_type=token.token_type
        ) 