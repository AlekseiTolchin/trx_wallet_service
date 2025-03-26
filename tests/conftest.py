from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.backend.db import Base
from app.config import TEST_DATABASE_URL


DATABASE_URL = TEST_DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope='session')
async def create_test_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.close()
