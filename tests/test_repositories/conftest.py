import pytest

from app.database import engine, async_session
from app.models.base import Base


@pytest.fixture
async def setup_database():
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
