from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import settings


async def get_org_db_session(org_details: str) -> sessionmaker:
    """
    Creates a dynamic database session connected to the organization's specific database.

    Args:
    - org_details (str): The organization name, used to create a dynamic database URL.

    Returns:
    - sessionmaker: A SQLAlchemy session factory for the specific organization's database.
    """
    org_details = org_details.lower()
    DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_INSTANCE_HOST}:{settings.DB_PORT}/{org_details}"

    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    return async_session
