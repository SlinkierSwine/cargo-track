from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class DriverStatus:
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"


class Driver(BaseModel):
    id: UUID
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    license_number: str = Field(..., min_length=5, max_length=20)
    license_class: str = Field(..., min_length=1, max_length=10)
    license_expiry: datetime
    medical_certificate_expiry: datetime
    experience_years: int = Field(..., ge=0, le=50)
    status: str = Field(default=DriverStatus.ACTIVE)
    emergency_contact_name: str = Field(..., min_length=1, max_length=100)
    emergency_contact_phone: str = Field(..., min_length=10, max_length=20)
    created_at: datetime
    updated_at: datetime


class DriverCreate(BaseModel):
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


class DriverUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    license_number: Optional[str] = Field(None, min_length=5, max_length=20)
    license_class: Optional[str] = Field(None, min_length=1, max_length=10)
    license_expiry: Optional[datetime] = None
    medical_certificate_expiry: Optional[datetime] = None
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    status: Optional[str] = None
    emergency_contact_name: Optional[str] = Field(None, min_length=1, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, min_length=10, max_length=20) 