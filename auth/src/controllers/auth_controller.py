from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from entities.user import UserCreate, UserResponse
from entities.token import Token
from use_cases.register_user_use_case import RegisterUserUseCase, RegisterUserRequest
from use_cases.authenticate_user_use_case import AuthenticateUserUseCase, AuthenticateUserRequest
from repositories.user_repository import UserRepository
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    register_use_case = RegisterUserUseCase(user_repository)
    
    try:
        request = RegisterUserRequest(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        response = register_use_case.execute(request)
        return UserResponse(
            id=response.id,
            email=response.email,
            username=response.username,
            role=response.role,
            is_active=response.is_active,
            first_name=response.first_name,
            last_name=response.last_name
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    authenticate_use_case = AuthenticateUserUseCase(user_repository)
    
    try:
        request = AuthenticateUserRequest(email=email, password=password)
        response = authenticate_use_case.execute(request)
        return Token(
            access_token=response.access_token,
            token_type=response.token_type
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) 