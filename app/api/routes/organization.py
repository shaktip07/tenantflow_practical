from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Organization
from app.api.schemas import OrganizationCreateSchema, OrganizationListingSchema
from app.core.dependencies import get_db
from app.base.response import (
    success_response,
    success_response_with_data,
    error_response,
)
from app.services.organization import create_org_database
from app.core.security import hash_password

# from app.security import hash_password
from app.db.models import AdminUser
from sqlalchemy.future import select

router = APIRouter()


@router.post("/create", tags=["organization"])
async def create_organization(
    data: OrganizationCreateSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    try:
        stmt = select(Organization).filter(Organization.name == data.organization_name)
        existing_org = await db.execute(stmt)
        if existing_org.scalars().first():
            raise HTTPException(status_code=400, detail="Organization already exists")

        # Create organization entry in the main DB
        new_org = Organization(
            name=data.organization_name,
            password="Admin1234",
        )
        db.add(new_org)
        await db.commit()

        # Create an admin user in the new organization database
        admin_hashed_password = hash_password(data.password)
        new_user = AdminUser(
            email=data.email,
            password=admin_hashed_password,
            is_admin=True,
            organization_id=new_org.id,
        )
        db.add(new_user)
        await db.commit()

        background_tasks.add_task(create_org_database, data)

        return success_response("Organization created successfully")
    except Exception as e:
        print(f"Error in creating organization: {e}")
        return error_response(f"Error in creating organization: {e}")


@router.get("/", response_model=List[OrganizationListingSchema], tags=["organization"])
async def get_organizations(
    org_name: Optional[str] = None, db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(Organization)

        if org_name:
            stmt = stmt.filter(Organization.name.ilike(f"%{org_name}%"))

        result = await db.execute(stmt)
        organizations = result.scalars().all()

        if organizations:
            return success_response_with_data(
                message="Organization listed successfully",
                data=[
                    OrganizationListingSchema.model_validate(org).model_dump()
                    for org in organizations
                ],
            )
        else:
            return error_response("Organization not found")
    except Exception as e:
        print(f"Error in getting organization: {e}")
        return error_response(f"Error in getting organization: {e}")
