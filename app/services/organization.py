from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from app.api.schemas import OrganizationCreateSchema
from app.db.models.users import DynamicBase
import settings


async def create_org_database(data: OrganizationCreateSchema):
    """
    Creates a new organization's database and initializes the required tables.

    Args:
    - data (OrganizationCreateSchema): Contains organization name, email, and password.

    Steps:
    1. Create a new database for the organization.
    2. Retrieve the organization's database URL.
    3. Create necessary tables in the new database.
    """
    email = data.email
    password = data.password
    organization_name = data.organization_name.lower()

    # creating dynamic database
    await create_new_database(organization_name)

    # Creating tables in the dynamic database
    org_db_url = await get_org_db_url(organization_name)
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


async def get_org_db_url(org_name: str):
    """
    Constructs the organization's specific database URL.

    Args:
    - org_name (str): The name of the organization, used to form the database URL.

    Returns:
    - str: The constructed database URL for the organization's database.
    """
    org_db_url = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_INSTANCE_HOST}:{settings.DB_PORT}/{org_name}"
    return org_db_url
