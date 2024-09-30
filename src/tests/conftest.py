from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.models import Base
from core.config import settings
from db.session import DatabaseHelper, db_helper
from main import app

test_db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=False,
    echo_pool=False,
    pool_size=5,
    max_overflow=10
)

url = str(settings.db.url)
engine_test = create_async_engine(url, echo=True)
session_factory = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
Base.metadata.bind = engine_test


async def override_session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


app.dependency_overrides[db_helper.session_getter] = override_session_getter


@pytest.fixture(autouse=True, scope="session")
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope="function")
async def db_session(setup_database) -> AsyncSession:
    async with session_factory() as session:
        async with session.begin():
            yield session
        await session.rollback()
