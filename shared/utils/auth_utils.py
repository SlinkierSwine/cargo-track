from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import httpx
import os
import structlog

logger = structlog.get_logger(__name__)
security = HTTPBearer()


def create_access_token(data: Dict[str, Any], secret_key: str, algorithm: str = "HS256", expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_token(token: str, secret_key: str, algorithm: str = "HS256") -> Optional[Dict[str, Any]]:
    try:
        logger.info("Attempting to verify token", token_length=len(token), secret_key_length=len(secret_key), algorithm=algorithm)
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        logger.info("Token verified successfully", payload_keys=list(payload.keys()))
        return payload
    except JWTError as e:
        logger.error("JWT verification failed", error=str(e), token_length=len(token))
        return None
    except Exception as e:
        logger.error("Unexpected error during token verification", error=str(e), token_length=len(token))
        return None


async def get_user_from_auth_service(user_id: str, auth_service_url: str) -> Optional[Dict[str, Any]]:
    """Получает информацию о пользователе из auth сервиса"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{auth_service_url}/users/{user_id}",
                timeout=5.0
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return None


def get_current_user(secret_key: str, algorithm: str = "HS256"):
    def _get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        token = credentials.credentials
        logger.info("Processing token in get_current_user", token_length=len(token))
        payload = verify_token(token, secret_key, algorithm)
        if payload is None or payload.get("role") is None:
            logger.error("Token validation failed", has_payload=payload is not None, has_role=payload.get("role") if payload else None)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.info("Token validated successfully", user_role=payload.get("role"))
        return payload
    return _get_current_user


def require_role(required_role: str, secret_key: str, algorithm: str = "HS256"):
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user(secret_key, algorithm))) -> Dict[str, Any]:
        user_role = current_user.get("role")
        logger.info("Checking role requirement", user_role=user_role, required_role=required_role)
        if user_role != required_role:
            logger.error("Role check failed", user_role=user_role, required_role=required_role)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        return current_user
    return role_checker


def require_any_role(required_roles: list[str], secret_key: str, algorithm: str = "HS256"):
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user(secret_key, algorithm))) -> Dict[str, Any]:
        user_role = current_user.get("role")
        logger.info("Checking any role requirement", user_role=user_role, required_roles=required_roles)
        if user_role not in required_roles:
            logger.error("Any role check failed", user_role=user_role, required_roles=required_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(required_roles)}"
            )
        return current_user
    return role_checker


class AuthServiceClient:
    """Клиент для взаимодействия с auth сервисом"""
    
    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получает информацию о пользователе"""
        return await get_user_from_auth_service(user_id, self.auth_service_url)
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Проверяет токен через auth сервис"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.auth_service_url}/auth/verify",
                    json={"token": token},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception:
            pass
        return None 