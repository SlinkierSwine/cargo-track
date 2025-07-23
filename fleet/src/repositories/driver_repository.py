from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime

from entities.driver import Driver, DriverCreate, DriverUpdate, DriverStatus
from entities.database_models import Driver as DriverModel
from repositories.interfaces.driver_repository import IDriverRepository


class DriverRepository(IDriverRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, driver: DriverCreate) -> Driver:
        db_driver = DriverModel(
            first_name=driver.first_name,
            last_name=driver.last_name,
            email=driver.email,
            phone=driver.phone,
            license_number=driver.license_number,
            license_class=driver.license_class,
            license_expiry=driver.license_expiry,
            medical_certificate_expiry=driver.medical_certificate_expiry,
            experience_years=driver.experience_years,
            emergency_contact_name=driver.emergency_contact_name,
            emergency_contact_phone=driver.emergency_contact_phone
        )
        
        self.db_session.add(db_driver)
        self.db_session.commit()
        self.db_session.refresh(db_driver)
        
        return Driver(
            id=db_driver.id,
            first_name=db_driver.first_name,
            last_name=db_driver.last_name,
            email=db_driver.email,
            phone=db_driver.phone,
            license_number=db_driver.license_number,
            license_class=db_driver.license_class,
            license_expiry=db_driver.license_expiry,
            medical_certificate_expiry=db_driver.medical_certificate_expiry,
            experience_years=db_driver.experience_years,
            status=db_driver.status,
            emergency_contact_name=db_driver.emergency_contact_name,
            emergency_contact_phone=db_driver.emergency_contact_phone,
            created_at=db_driver.created_at,
            updated_at=db_driver.updated_at
        )
    
    def get_by_id(self, driver_id: UUID) -> Optional[Driver]:
        db_driver = self.db_session.query(DriverModel).filter(DriverModel.id == driver_id).first()
        if not db_driver:
            return None
        
        return Driver(
            id=db_driver.id,
            first_name=db_driver.first_name,
            last_name=db_driver.last_name,
            email=db_driver.email,
            phone=db_driver.phone,
            license_number=db_driver.license_number,
            license_class=db_driver.license_class,
            license_expiry=db_driver.license_expiry,
            medical_certificate_expiry=db_driver.medical_certificate_expiry,
            experience_years=db_driver.experience_years,
            status=db_driver.status,
            emergency_contact_name=db_driver.emergency_contact_name,
            emergency_contact_phone=db_driver.emergency_contact_phone,
            created_at=db_driver.created_at,
            updated_at=db_driver.updated_at
        )
    
    def get_by_email(self, email: str) -> Optional[Driver]:
        db_driver = self.db_session.query(DriverModel).filter(DriverModel.email == email).first()
        if not db_driver:
            return None
        
        return Driver(
            id=db_driver.id,
            first_name=db_driver.first_name,
            last_name=db_driver.last_name,
            email=db_driver.email,
            phone=db_driver.phone,
            license_number=db_driver.license_number,
            license_class=db_driver.license_class,
            license_expiry=db_driver.license_expiry,
            medical_certificate_expiry=db_driver.medical_certificate_expiry,
            experience_years=db_driver.experience_years,
            status=db_driver.status,
            emergency_contact_name=db_driver.emergency_contact_name,
            emergency_contact_phone=db_driver.emergency_contact_phone,
            created_at=db_driver.created_at,
            updated_at=db_driver.updated_at
        )
    
    def get_by_license_number(self, license_number: str) -> Optional[Driver]:
        db_driver = self.db_session.query(DriverModel).filter(DriverModel.license_number == license_number).first()
        if not db_driver:
            return None
        
        return Driver(
            id=db_driver.id,
            first_name=db_driver.first_name,
            last_name=db_driver.last_name,
            email=db_driver.email,
            phone=db_driver.phone,
            license_number=db_driver.license_number,
            license_class=db_driver.license_class,
            license_expiry=db_driver.license_expiry,
            medical_certificate_expiry=db_driver.medical_certificate_expiry,
            experience_years=db_driver.experience_years,
            status=db_driver.status,
            emergency_contact_name=db_driver.emergency_contact_name,
            emergency_contact_phone=db_driver.emergency_contact_phone,
            created_at=db_driver.created_at,
            updated_at=db_driver.updated_at
        )
    
    def update(self, driver_id: UUID, driver: DriverUpdate) -> Optional[Driver]:
        db_driver = self.db_session.query(DriverModel).filter(DriverModel.id == driver_id).first()
        if not db_driver:
            return None
        
        update_data = driver.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_driver, field, value)
        
        db_driver.updated_at = datetime.utcnow()
        self.db_session.commit()
        self.db_session.refresh(db_driver)
        
        return Driver(
            id=db_driver.id,
            first_name=db_driver.first_name,
            last_name=db_driver.last_name,
            email=db_driver.email,
            phone=db_driver.phone,
            license_number=db_driver.license_number,
            license_class=db_driver.license_class,
            license_expiry=db_driver.license_expiry,
            medical_certificate_expiry=db_driver.medical_certificate_expiry,
            experience_years=db_driver.experience_years,
            status=db_driver.status,
            emergency_contact_name=db_driver.emergency_contact_name,
            emergency_contact_phone=db_driver.emergency_contact_phone,
            created_at=db_driver.created_at,
            updated_at=db_driver.updated_at
        )
    
    def delete(self, driver_id: UUID) -> bool:
        db_driver = self.db_session.query(DriverModel).filter(DriverModel.id == driver_id).first()
        if not db_driver:
            return False
        
        self.db_session.delete(db_driver)
        self.db_session.commit()
        return True
    
    def get_all(self) -> List[Driver]:
        db_drivers = self.db_session.query(DriverModel).all()
        return [
            Driver(
                id=driver.id,
                first_name=driver.first_name,
                last_name=driver.last_name,
                email=driver.email,
                phone=driver.phone,
                license_number=driver.license_number,
                license_class=driver.license_class,
                license_expiry=driver.license_expiry,
                medical_certificate_expiry=driver.medical_certificate_expiry,
                experience_years=driver.experience_years,
                status=driver.status,
                emergency_contact_name=driver.emergency_contact_name,
                emergency_contact_phone=driver.emergency_contact_phone,
                created_at=driver.created_at,
                updated_at=driver.updated_at
            )
            for driver in db_drivers
        ]
    
    def get_by_status(self, status: str) -> List[Driver]:
        db_drivers = self.db_session.query(DriverModel).filter(DriverModel.status == status).all()
        return [
            Driver(
                id=driver.id,
                first_name=driver.first_name,
                last_name=driver.last_name,
                email=driver.email,
                phone=driver.phone,
                license_number=driver.license_number,
                license_class=driver.license_class,
                license_expiry=driver.license_expiry,
                medical_certificate_expiry=driver.medical_certificate_expiry,
                experience_years=driver.experience_years,
                status=driver.status,
                emergency_contact_name=driver.emergency_contact_name,
                emergency_contact_phone=driver.emergency_contact_phone,
                created_at=driver.created_at,
                updated_at=driver.updated_at
            )
            for driver in db_drivers
        ]
    
    def get_available_drivers(self) -> List[Driver]:
        # Get active drivers with valid licenses and medical certificates
        current_time = datetime.utcnow()
        db_drivers = self.db_session.query(DriverModel).filter(
            and_(
                DriverModel.status == DriverStatus.ACTIVE,
                DriverModel.license_expiry > current_time,
                DriverModel.medical_certificate_expiry > current_time
            )
        ).all()
        
        return [
            Driver(
                id=driver.id,
                first_name=driver.first_name,
                last_name=driver.last_name,
                email=driver.email,
                phone=driver.phone,
                license_number=driver.license_number,
                license_class=driver.license_class,
                license_expiry=driver.license_expiry,
                medical_certificate_expiry=driver.medical_certificate_expiry,
                experience_years=driver.experience_years,
                status=driver.status,
                emergency_contact_name=driver.emergency_contact_name,
                emergency_contact_phone=driver.emergency_contact_phone,
                created_at=driver.created_at,
                updated_at=driver.updated_at
            )
            for driver in db_drivers
        ] 