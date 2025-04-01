from pydantic import BaseModel, EmailStr


class SuperAdminRegister(BaseModel):
    email: EmailStr
    password: str


class SuperAdminLogin(BaseModel):
    email: EmailStr
    password: str
