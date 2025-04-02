from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import User, Organization, AdminUser
from app.api.schemas import AdminCreate, AdminLogin, UserListingSchema
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_db
from app.base.response import (
    success_response,
    success_response_with_data,
    error_response,
)
from app.helper import get_org_db_session

router = APIRouter()


@router.post("/user/create", tags=["admin"])
async def create_user(
    request: Request,
    user: AdminCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint to create a new user for a specific organization.

    Args:
    - request: The request object containing the organization info in state.
    - user (AdminCreate): The user data used for creating a new user.
    - db (AsyncSession): The main database session for fetching organization details.

    Returns:
    - success_response: JSON response indicating successful user creation.
    """
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
        return error_response(f"Error in creating user: {e}")


@router.post("/register", tags=["admin"])
async def register_superadmin(data: AdminCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(AdminUser).where(AdminUser.email == data.email)
        )
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
    except Exception as e:
        print(f"Error in registering superadmin: {e}")
        return error_response(f"Error in registering superadmin: {e}")


@router.post("/login", tags=["admin"])
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

    # Generate JWT access token
    token = create_access_token(payload)

    return success_response_with_data(
        "Login successful", {"access_token": token, "token_type": "JWT"}
    )


@router.get("/user/list", response_model=List[UserListingSchema], tags=["admin"])
async def create_user(
    request: Request,
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

        async_session = await get_org_db_session(organization.name)

        async with async_session() as session:
            results = await session.execute(
                select(User).where(User.organization_id == int(org))
            )
            users = results.scalars().all()

            if users:
                return success_response_with_data(
                    message="Users listed successfully",
                    data=[
                        UserListingSchema.model_validate(user).model_dump()
                        for user in users
                    ],
                )

        return error_response("No users found")
    except Exception as e:
        print(f"Error in creating user: {e}")
        return error_response(f"Error in creating user: {e}")
