from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime


class BaseEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class UserRole(str, Enum):
    ADMIN = "admin"
    DISPATCHER = "dispatcher"
    DRIVER = "driver"
    CLIENT = "client"


class User(BaseEntity):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    hashed_password: str
    role: UserRole = UserRole.CLIENT
    is_active: bool = True
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.CLIENT
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] 