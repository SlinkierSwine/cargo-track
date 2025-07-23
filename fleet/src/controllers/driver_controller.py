from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from config.database import get_db
from entities.driver import Driver, DriverCreate, DriverUpdate
from use_cases.create_driver_use_case import CreateDriverUseCase
from repositories.driver_repository import DriverRepository
from utils.auth_utils import get_current_user, require_any_role


router = APIRouter(prefix="/drivers", tags=["drivers"])


def get_driver_repository(db: Session = Depends(get_db)) -> DriverRepository:
    return DriverRepository(db)


def get_create_driver_use_case(driver_repository: DriverRepository = Depends(get_driver_repository)) -> CreateDriverUseCase:
    return CreateDriverUseCase(driver_repository)


@router.post("/", response_model=Driver, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver_data: DriverCreate,
    use_case: CreateDriverUseCase = Depends(get_create_driver_use_case),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        result = use_case.execute(driver_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/", response_model=List[Driver])
async def get_all_drivers(
    driver_repository: DriverRepository = Depends(get_driver_repository),
    current_user: dict = Depends(get_current_user)
):
    try:
        return driver_repository.get_all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{driver_id}", response_model=Driver)
async def get_driver_by_id(
    driver_id: UUID,
    driver_repository: DriverRepository = Depends(get_driver_repository),
    current_user: dict = Depends(get_current_user)
):
    try:
        driver = driver_repository.get_by_id(driver_id)
        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{driver_id}", response_model=Driver)
async def update_driver(
    driver_id: UUID,
    driver_data: DriverUpdate,
    driver_repository: DriverRepository = Depends(get_driver_repository),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    try:
        driver = driver_repository.update(driver_id, driver_data)
        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: UUID,
    driver_repository: DriverRepository = Depends(get_driver_repository),
    current_user: dict = Depends(require_any_role(["admin"]))
):
    try:
        success = driver_repository.delete(driver_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/by-email/{email}", response_model=Driver)
async def get_driver_by_email(
    email: str,
    driver_repository: DriverRepository = Depends(get_driver_repository)
):
    try:
        driver = driver_repository.get_by_email(email)
        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/by-license/{license_number}", response_model=Driver)
async def get_driver_by_license_number(
    license_number: str,
    driver_repository: DriverRepository = Depends(get_driver_repository)
):
    try:
        driver = driver_repository.get_by_license_number(license_number)
        if not driver:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found")
        return driver
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/status/{status}", response_model=List[Driver])
async def get_drivers_by_status(
    status: str,
    driver_repository: DriverRepository = Depends(get_driver_repository)
):
    try:
        return driver_repository.get_by_status(status)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/available/", response_model=List[Driver])
async def get_available_drivers(
    driver_repository: DriverRepository = Depends(get_driver_repository)
):
    try:
        return driver_repository.get_available_drivers()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 