from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import get_settings
from fastapi import Depends
import httpx
from shared.utils.auth_utils import (
    get_current_user as shared_get_current_user,
    require_role as shared_require_role,
    require_any_role as shared_require_any_role,
    AuthServiceClient as SharedAuthServiceClient
)

settings = get_settings()
security = HTTPBearer()


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


async def get_user_from_auth_service(user_id: str) -> Optional[Dict[str, Any]]:
    """Получает информацию о пользователе из auth сервиса"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:8000/users/{user_id}",
                timeout=5.0
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return None


# Создаем функции с настройками fleet сервиса
def get_current_user():
    return shared_get_current_user(settings.secret_key, settings.algorithm)

def require_role(required_role: str):
    return shared_require_role(required_role, settings.secret_key, settings.algorithm)

def require_any_role(required_roles: list[str]):
    return shared_require_any_role(required_roles, settings.secret_key, settings.algorithm)

# Создаем клиент для auth сервиса
def get_auth_service_client() -> SharedAuthServiceClient:
    return SharedAuthServiceClient(settings.auth_service_url) 