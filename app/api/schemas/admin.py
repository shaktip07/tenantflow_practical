from pydantic import BaseModel, EmailStr
from typing import Optional


class AdminCreate(BaseModel):
    email: EmailStr
    password: str


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class UserListingSchema(BaseModel):
    id: int
    email: str
    organization_id: Optional[int]

    class Config:
        from_attributes = True
