from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from entities.compatibility import CompatibilityCheckRequest, CompatibilityCheckResponse
from use_cases.check_compatibility_use_case import CheckCompatibilityUseCase
from repositories.cargo_repository import CargoRepository
from config.database import get_db
from utils.auth_utils import get_current_user, require_any_role

router = APIRouter(prefix="/compatibility", tags=["compatibility"])


@router.post("/check", response_model=CompatibilityCheckResponse)
def check_compatibility(
    request: CompatibilityCheckRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"])),
    authorization: Optional[str] = Header(None)
):
    cargo_repository = CargoRepository(db)
    check_use_case = CheckCompatibilityUseCase(cargo_repository)
    
    # Извлекаем токен из заголовка Authorization
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]  # Убираем "Bearer " префикс
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token required for fleet service integration"
        )
    
    try:
        response = check_use_case.execute(request, token)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 