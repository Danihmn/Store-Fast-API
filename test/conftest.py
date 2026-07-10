import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import app
from infrastructure.data.database import session_scope
from settings import Settings


@pytest.fixture
def client():
    with TestClient(app) as client:
        app.dependency_overrides[session_scope] = session
        yield client
        app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(Settings().DATABASE_URL)  # type: ignore
    connection = await engine.connect()
    transaction = await connection.begin()

    Session = async_sessionmaker(bind=connection, expire_on_commit=False)
    session = Session()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()
    await engine.dispose()
