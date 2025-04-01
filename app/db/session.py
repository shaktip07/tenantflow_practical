from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager
import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=100,
    max_overflow=100,
    pool_timeout=60,
    pool_recycle=3600,
    pool_pre_ping=True,
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    """Dependency to get async DB session"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_context_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
