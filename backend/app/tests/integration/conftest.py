import asyncio
import pytest
import pytest_asyncio
import alembic
from alembic.config import Config
from typing import AsyncIterator, Generator
from httpx import AsyncClient
from fastapi.testclient import TestClient

from actions.create_superuser import create_superuser
from main import app
from core.config import settings
from core.models.mongo_helper import mongo_database, _MongoClientSingleton


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app, base_url="http://test-server") as client:
        yield client


# @pytest.fixture(scope="session")
# def client(db) -> Generator:
#     with TestClient(app) as test_client:
#         yield test_client


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_db() -> Generator:
    mongo_db = mongo_database()
    _MongoClientSingleton.instance.mongo_client.get_io_loop = asyncio.get_event_loop
    # await init_db(db)  # TODO
    yield mongo_db


@pytest_asyncio.fixture(scope="session")
async def postgres_db() -> Generator:
    print(postgres_db)
    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    await create_superuser()
    yield
    alembic.command.downgrade(config, "base")
