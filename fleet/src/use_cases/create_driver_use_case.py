from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from entities.driver import Driver, DriverCreate
from repositories.interfaces.driver_repository import IDriverRepository


class CreateDriverRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    license_number: str = Field(..., min_length=5, max_length=20)
    license_class: str = Field(..., min_length=1, max_length=10)
    license_expiry: datetime
    medical_certificate_expiry: datetime
    experience_years: int = Field(..., ge=0, le=50)
    emergency_contact_name: str = Field(..., min_length=1, max_length=100)
    emergency_contact_phone: str = Field(..., min_length=10, max_length=20)


class CreateDriverResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    license_number: str
    license_class: str
    license_expiry: datetime
    medical_certificate_expiry: datetime
    experience_years: int
    status: str
    emergency_contact_name: str
    emergency_contact_phone: str
    created_at: datetime
    updated_at: datetime


class CreateDriverUseCase:
    def __init__(self, driver_repository: IDriverRepository):
        self.driver_repository = driver_repository
    
    def execute(self, request: CreateDriverRequest) -> CreateDriverResponse:
        # Check if driver with same email already exists
        existing_driver = self.driver_repository.get_by_email(request.email)
        if existing_driver:
            raise ValueError("Driver with this email already exists")
        
        # Check if driver with same license number already exists
        existing_license = self.driver_repository.get_by_license_number(request.license_number)
        if existing_license:
            raise ValueError("Driver with this license number already exists")
        
        # Validate driver data
        if request.experience_years < 0:
            raise ValueError("Experience years cannot be negative")
        
        if request.license_expiry <= datetime.now():
            raise ValueError("License expiry date must be in the future")
        
        if request.medical_certificate_expiry <= datetime.now():
            raise ValueError("Medical certificate expiry date must be in the future")
        
        # Create driver
        driver_data = DriverCreate(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            license_number=request.license_number,
            license_class=request.license_class,
            license_expiry=request.license_expiry,
            medical_certificate_expiry=request.medical_certificate_expiry,
            experience_years=request.experience_years,
            emergency_contact_name=request.emergency_contact_name,
            emergency_contact_phone=request.emergency_contact_phone
        )
        
        driver = self.driver_repository.create(driver_data)
        
        return CreateDriverResponse(
            id=str(driver.id),
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