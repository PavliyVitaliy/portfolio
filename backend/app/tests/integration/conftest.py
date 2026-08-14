from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.api_v1.experience import router as experience_router
from core.models import User, db_helper


@pytest.fixture
def user() -> User:
    return User(
        id=uuid4(),
        email="admin@example.com",
        hashed_password="not-used-in-api-tests",
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )


@pytest.fixture
def api_app() -> AsyncIterator[FastAPI]:
    app = FastAPI()
    app.include_router(experience_router, prefix="/api/v1")

    async def get_test_session() -> AsyncIterator[object]:
        yield object()

    app.dependency_overrides[db_helper.session_getter] = get_test_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(api_app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=api_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
