import pytest
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app import config
from app.database import engine, async_session
from app.models.base import Base


async def create_test_database_if_needed():
    database_url = (
        f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}"
        f"@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/postgres"
    )
    engine = create_async_engine(
        database_url,
        echo=True,
        poolclass=NullPool,
    )
    async with engine.begin() as conn:
        await conn.execute(text("commit"))
        try:
            await conn.execute(text(f"CREATE DATABASE {config.POSTGRES_DB}"))
        except ProgrammingError:
            pass


@pytest.fixture
async def setup_database():
    await create_test_database_if_needed()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(setup_database):
    session = async_session()
    yield session
    await session.close()
