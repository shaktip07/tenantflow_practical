from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import User

# from app.db.models.admin import AdminPanel
from app.api.schemas import AdminCreate, AdminLogin
from app.db.models import Organization, AdminUser
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_db
from sqlalchemy.future import select
from app.base.response import (
    success_response,
    success_response_with_data,
    error_response,
)

router = APIRouter()


async def get_org_db_session(org_details):
    org_details = org_details.lower()
    """Creates a dynamic connection to the organization's specific database."""
    DATABASE_URL = (
        f"postgresql+asyncpg://postgres:Patel1234@localhost:5432/{org_details}"
    )
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session


@router.post("/user/create", tags=["admin"])
async def create_user(
    request: Request,
    user: AdminCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        org = request.state.org
        organization = await db.execute(
            select(Organization).where(Organization.id == int(org))
        )
        organization = organization.scalars().first()
        if not organization:
            raise HTTPException(status_code=400, detail="Organization not found")

        # Create the session dynamically based on the organization's DB details
        async_session = await get_org_db_session(organization.name)
        print(async_session, "async_session")

        async with async_session() as session:
            # Create user instance for the org database
            new_user = User(
                email=user.email,
                password=hash_password(user.password),
                organization_id=int(org),
            )

            session.add(new_user)
            await session.commit()

        return success_response("User created successfully")
    except Exception as e:
        print(f"Error in creating user: {e}")


@router.post("/register")
async def register_superadmin(data: AdminCreate, db: AsyncSession = Depends(get_db)):
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
async def login_superadmin(data: AdminLogin, db: AsyncSession = Depends(get_db)):
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
