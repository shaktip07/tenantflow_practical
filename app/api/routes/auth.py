from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import AdminUser

# from app.db.models.admin import AdminPanel
from app.api.schemas import SuperAdminRegister, SuperAdminLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_db
from sqlalchemy.future import select
from app.base.response import (
    success_response,
    success_response_with_data,
    error_response,
)

router = APIRouter()


@router.post("/superadmin/register")
async def register_superadmin(
    data: SuperAdminRegister, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(AdminUser).where(AdminUser.email == data.email))
    existing_admin = result.scalars().first()

    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_admin = AdminUser(
        email=data.email, password=hash_password(data.password), is_superadmin=True
    )
    db.add(new_admin)
    await db.commit()

    # await db.merge(AdminPanel(username=data.email, password=data.password))

    return success_response("Super Admin registered successfully")


@router.post("/login")
async def login_superadmin(data: SuperAdminLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AdminUser).where(AdminUser.email == data.email))
    admin = result.scalars().first()

    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "id": admin.id,
        "email": admin.email,
        "is_superadmin": admin.is_superadmin,
        "is_admin": admin.is_admin,
        "organization_id": admin.organization_id if admin.organization_id else None,
    }
    token = create_access_token(payload)

    return success_response_with_data(
        "Login successful", {"access_token": token, "token_type": "JWT"}
    )
