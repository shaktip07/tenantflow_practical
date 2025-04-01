from app.db.session import async_session
from contextlib import asynccontextmanager


async def get_db():
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
