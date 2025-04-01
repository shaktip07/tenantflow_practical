from app.api.schemas import OrganizationCreateSchema
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.db.session import Base
from app.db.models.users import DynamicBase
from sqlalchemy.sql import text
from app.db.models import Organization, User
from app.core.security import hash_password
import settings


async def create_org_database(data: OrganizationCreateSchema):
    email = data.email
    password = data.password
    organization_name = data.organization_name.lower()

    # creating dynamic database
    await create_new_database(organization_name)

    org_db_url = await get_org_db_url(organization_name, email, password)
    org_engine = create_async_engine(org_db_url, echo=True)

    async with org_engine.begin() as conn:
        await conn.run_sync(DynamicBase.metadata.create_all)

    await org_engine.dispose()


async def create_new_database(org_name: str):
    main_engine = create_async_engine(
        settings.DATABASE_URL, isolation_level="AUTOCOMMIT", echo=True
    )
    async with main_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE {org_name};"))
    await main_engine.dispose()


async def get_org_db_url(org_name: str, email: str, password: str):
    org_db_url = f"postgresql+asyncpg://postgres:Patel1234@localhost:5432/{org_name}"
    return org_db_url
