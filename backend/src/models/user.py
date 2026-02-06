from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID, uuid4


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str  # In a real implementation, this would be hashed


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class User(UserInDB):
    pass