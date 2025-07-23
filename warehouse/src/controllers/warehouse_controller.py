from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from entities.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseResponse
from use_cases.create_warehouse_use_case import CreateWarehouseUseCase
from repositories.warehouse_repository import WarehouseRepository
from config.database import get_db
from utils.auth_utils import get_current_user, require_any_role

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.post("/", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    warehouse_repository = WarehouseRepository(db)
    create_use_case = CreateWarehouseUseCase(warehouse_repository)
    
    try:
        response = create_use_case.execute(warehouse_data)
        return WarehouseResponse(
            id=response.id,
            name=response.name,
            warehouse_type=response.warehouse_type,
            address=response.address,
            city=response.city,
            country=response.country,
            postal_code=response.postal_code,
            phone=response.phone,
            email=response.email,
            total_capacity_weight=response.total_capacity_weight,
            total_capacity_volume=response.total_capacity_volume,
            available_capacity_weight=response.available_capacity_weight,
            available_capacity_volume=response.available_capacity_volume,
            temperature_controlled=response.temperature_controlled,
            hazardous_materials_allowed=response.hazardous_materials_allowed,
            operating_hours=response.operating_hours,
            status=response.status,
            created_at=response.created_at,
            updated_at=response.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[WarehouseResponse])
def get_all_warehouses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    warehouse_repository = WarehouseRepository(db)
    warehouses = warehouse_repository.get_all(skip=skip, limit=limit)
    
    return [
        WarehouseResponse(
            id=warehouse.id,
            name=warehouse.name,
            warehouse_type=warehouse.warehouse_type,
            address=warehouse.address,
            city=warehouse.city,
            country=warehouse.country,
            postal_code=warehouse.postal_code,
            phone=warehouse.phone,
            email=warehouse.email,
            total_capacity_weight=warehouse.total_capacity_weight,
            total_capacity_volume=warehouse.total_capacity_volume,
            available_capacity_weight=warehouse.available_capacity_weight,
            available_capacity_volume=warehouse.available_capacity_volume,
            temperature_controlled=warehouse.temperature_controlled,
            hazardous_materials_allowed=warehouse.hazardous_materials_allowed,
            operating_hours=warehouse.operating_hours,
            status=warehouse.status,
            created_at=warehouse.created_at,
            updated_at=warehouse.updated_at
        ) for warehouse in warehouses
    ]


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    warehouse_repository = WarehouseRepository(db)
    warehouse = warehouse_repository.get_by_id(warehouse_id)
    
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    
    return WarehouseResponse(
        id=warehouse.id,
        name=warehouse.name,
        warehouse_type=warehouse.warehouse_type,
        address=warehouse.address,
        city=warehouse.city,
        country=warehouse.country,
        postal_code=warehouse.postal_code,
        phone=warehouse.phone,
        email=warehouse.email,
        total_capacity_weight=warehouse.total_capacity_weight,
        total_capacity_volume=warehouse.total_capacity_volume,
        available_capacity_weight=warehouse.available_capacity_weight,
        available_capacity_volume=warehouse.available_capacity_volume,
        temperature_controlled=warehouse.temperature_controlled,
        hazardous_materials_allowed=warehouse.hazardous_materials_allowed,
        operating_hours=warehouse.operating_hours,
        status=warehouse.status,
        created_at=warehouse.created_at,
        updated_at=warehouse.updated_at
    )


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: str,
    warehouse_update: WarehouseUpdate,
    db: Session = Depends(get_db)
):
    warehouse_repository = WarehouseRepository(db)
    updated_warehouse = warehouse_repository.update(warehouse_id, warehouse_update)
    
    if not updated_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    
    return WarehouseResponse(
        id=updated_warehouse.id,
        name=updated_warehouse.name,
        warehouse_type=updated_warehouse.warehouse_type,
        address=updated_warehouse.address,
        city=updated_warehouse.city,
        country=updated_warehouse.country,
        postal_code=updated_warehouse.postal_code,
        phone=updated_warehouse.phone,
        email=updated_warehouse.email,
        total_capacity_weight=updated_warehouse.total_capacity_weight,
        total_capacity_volume=updated_warehouse.total_capacity_volume,
        available_capacity_weight=updated_warehouse.available_capacity_weight,
        available_capacity_volume=updated_warehouse.available_capacity_volume,
        temperature_controlled=updated_warehouse.temperature_controlled,
        hazardous_materials_allowed=updated_warehouse.hazardous_materials_allowed,
        operating_hours=updated_warehouse.operating_hours,
        status=updated_warehouse.status,
        created_at=updated_warehouse.created_at,
        updated_at=updated_warehouse.updated_at
    )


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db)
):
    warehouse_repository = WarehouseRepository(db)
    success = warehouse_repository.delete(warehouse_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        ) 