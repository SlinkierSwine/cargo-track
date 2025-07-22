from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from entities.user import User, UserRole, UserCreate
from repositories.interfaces.user_repository import IUserRepository
from utils.password_utils import hash_password


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CLIENT
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class RegisterUserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class RegisterUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        existing_user = self.user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        existing_username = self.user_repository.get_by_username(request.username)
        if existing_username:
            raise ValueError("User with this username already exists")
        
        user_data = UserCreate(
            email=request.email,
            username=request.username,
            password=request.password,
            role=request.role,
            first_name=request.first_name,
            last_name=request.last_name
        )
        
        user = self.user_repository.create(user_data)
        
        return RegisterUserResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
            first_name=user.first_name,
            last_name=user.last_name
        ) 