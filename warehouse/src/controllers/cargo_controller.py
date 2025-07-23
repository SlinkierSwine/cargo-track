from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from entities.cargo import CargoCreate, CargoUpdate, CargoResponse
from use_cases.create_cargo_use_case import CreateCargoUseCase
from repositories.cargo_repository import CargoRepository
from config.database import get_db
from utils.auth_utils import get_current_user, require_any_role

router = APIRouter(prefix="/cargo", tags=["cargo"])


@router.post("/", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def create_cargo(
    cargo_data: CargoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher", "driver"]))
):
    cargo_repository = CargoRepository(db)
    create_use_case = CreateCargoUseCase(cargo_repository)
    
    try:
        response = create_use_case.execute(cargo_data)
        return CargoResponse(
            id=response.id,
            tracking_number=response.tracking_number,
            name=response.name,
            description=response.description,
            weight=response.weight,
            volume=response.volume,
            dimensions=response.dimensions,
            value=response.value,
            insurance_amount=response.insurance_amount,
            cargo_type=response.cargo_type,
            temperature_requirements=response.temperature_requirements,
            humidity_requirements=response.humidity_requirements,
            hazardous_material=response.hazardous_material,
            hazardous_class=response.hazardous_class,
            special_handling=response.special_handling,
            fragility_level=response.fragility_level,
            storage_duration=response.storage_duration,
            expiration_date=response.expiration_date,
            status=response.status,
            warehouse_id=response.warehouse_id,
            location_in_warehouse=response.location_in_warehouse,
            created_at=response.created_at,
            updated_at=response.updated_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CargoResponse])
def get_all_cargo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    cargo_repository = CargoRepository(db)
    cargo_list = cargo_repository.list_cargo(skip=skip, limit=limit)
    
    return [
        CargoResponse(
            id=cargo.id,
            tracking_number=cargo.tracking_number,
            name=cargo.name,
            description=cargo.description,
            weight=cargo.weight,
            volume=cargo.volume,
            dimensions=cargo.dimensions,
            value=cargo.value,
            insurance_amount=cargo.insurance_amount,
            cargo_type=cargo.cargo_type,
            temperature_requirements=cargo.temperature_requirements,
            humidity_requirements=cargo.humidity_requirements,
            hazardous_material=cargo.hazardous_material,
            hazardous_class=cargo.hazardous_class,
            special_handling=cargo.special_handling,
            fragility_level=cargo.fragility_level,
            storage_duration=cargo.storage_duration,
            expiration_date=cargo.expiration_date,
            status=cargo.status,
            warehouse_id=cargo.warehouse_id,
            location_in_warehouse=cargo.location_in_warehouse,
            created_at=cargo.created_at,
            updated_at=cargo.updated_at
        ) for cargo in cargo_list
    ]


@router.get("/{cargo_id}", response_model=CargoResponse)
def get_cargo(
    cargo_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    cargo_repository = CargoRepository(db)
    cargo = cargo_repository.get_by_id(cargo_id)
    
    if not cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo not found"
        )
    
    return CargoResponse(
        id=cargo.id,
        tracking_number=cargo.tracking_number,
        name=cargo.name,
        description=cargo.description,
        weight=cargo.weight,
        volume=cargo.volume,
        dimensions=cargo.dimensions,
        value=cargo.value,
        insurance_amount=cargo.insurance_amount,
        cargo_type=cargo.cargo_type,
        temperature_requirements=cargo.temperature_requirements,
        humidity_requirements=cargo.humidity_requirements,
        hazardous_material=cargo.hazardous_material,
        hazardous_class=cargo.hazardous_class,
        special_handling=cargo.special_handling,
        fragility_level=cargo.fragility_level,
        storage_duration=cargo.storage_duration,
        expiration_date=cargo.expiration_date,
        status=cargo.status,
        warehouse_id=cargo.warehouse_id,
        location_in_warehouse=cargo.location_in_warehouse,
        created_at=cargo.created_at,
        updated_at=cargo.updated_at
    )


@router.get("/tracking/{tracking_number}", response_model=CargoResponse)
def get_cargo_by_tracking(
    tracking_number: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    cargo_repository = CargoRepository(db)
    cargo = cargo_repository.get_by_tracking_number(tracking_number)
    
    if not cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo not found"
        )
    
    return CargoResponse(
        id=cargo.id,
        tracking_number=cargo.tracking_number,
        cargo_type=cargo.cargo_type,
        name=cargo.name,
        description=cargo.description,
        weight=cargo.weight,
        volume=cargo.volume,
        dimensions=cargo.dimensions,
        value=cargo.value,
        insurance_amount=cargo.insurance_amount,
        temperature_requirements=cargo.temperature_requirements,
        humidity_requirements=cargo.humidity_requirements,
        hazardous_material=cargo.hazardous_material,
        hazardous_class=cargo.hazardous_class,
        special_handling=cargo.special_handling,
        fragility_level=cargo.fragility_level,
        storage_duration=cargo.storage_duration,
        expiration_date=cargo.expiration_date,
        status=cargo.status,
        warehouse_id=cargo.warehouse_id,
        location_in_warehouse=cargo.location_in_warehouse,
        created_at=cargo.created_at,
        updated_at=cargo.updated_at
    )


@router.get("/warehouse/{warehouse_id}", response_model=List[CargoResponse])
def list_cargo_by_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user())
):
    cargo_repository = CargoRepository(db)
    cargos = cargo_repository.get_by_warehouse_id(warehouse_id)
    
    return [
        CargoResponse(
            id=cargo.id,
            tracking_number=cargo.tracking_number,
            cargo_type=cargo.cargo_type,
            name=cargo.name,
            description=cargo.description,
            weight=cargo.weight,
            volume=cargo.volume,
            dimensions=cargo.dimensions,
            value=cargo.value,
            insurance_amount=cargo.insurance_amount,
            temperature_requirements=cargo.temperature_requirements,
            humidity_requirements=cargo.humidity_requirements,
            hazardous_material=cargo.hazardous_material,
            hazardous_class=cargo.hazardous_class,
            special_handling=cargo.special_handling,
            fragility_level=cargo.fragility_level,
            storage_duration=cargo.storage_duration,
            expiration_date=cargo.expiration_date,
            status=cargo.status,
            warehouse_id=cargo.warehouse_id,
            location_in_warehouse=cargo.location_in_warehouse,
            created_at=cargo.created_at,
            updated_at=cargo.updated_at
        )
        for cargo in cargos
    ]


@router.put("/{cargo_id}", response_model=CargoResponse)
def update_cargo(
    cargo_id: str,
    cargo_update: CargoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_role(["admin", "dispatcher"]))
):
    cargo_repository = CargoRepository(db)
    updated_cargo = cargo_repository.update(cargo_id, cargo_update)
    
    if not updated_cargo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo not found"
        )
    
    return CargoResponse(
        id=updated_cargo.id,
        tracking_number=updated_cargo.tracking_number,
        cargo_type=updated_cargo.cargo_type,
        name=updated_cargo.name,
        description=updated_cargo.description,
        weight=updated_cargo.weight,
        volume=updated_cargo.volume,
        dimensions=updated_cargo.dimensions,
        value=updated_cargo.value,
        insurance_amount=updated_cargo.insurance_amount,
        temperature_requirements=updated_cargo.temperature_requirements,
        humidity_requirements=updated_cargo.humidity_requirements,
        hazardous_material=updated_cargo.hazardous_material,
        hazardous_class=updated_cargo.hazardous_class,
        special_handling=updated_cargo.special_handling,
        fragility_level=updated_cargo.fragility_level,
        storage_duration=updated_cargo.storage_duration,
        expiration_date=updated_cargo.expiration_date,
        status=updated_cargo.status,
        warehouse_id=updated_cargo.warehouse_id,
        location_in_warehouse=updated_cargo.location_in_warehouse,
        created_at=updated_cargo.created_at,
        updated_at=updated_cargo.updated_at
    )


@router.delete("/{cargo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cargo(
    cargo_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_any_role(["admin"]))
):
    cargo_repository = CargoRepository(db)
    success = cargo_repository.delete(cargo_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo not found"
        ) 