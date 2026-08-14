import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from api.api_v1.fastapi_users import current_active_superuser, current_active_user


@pytest.mark.asyncio
async def test_authenticated_user_can_read_private_experience(
    api_app, client: AsyncClient, user
):
    api_app.dependency_overrides[current_active_user] = lambda: user

    response = await client.get("/api/v1/experience")

    assert response.status_code == 200
    assert response.json()["user"]["email"] == user.email


@pytest.mark.asyncio
async def test_superuser_can_read_secret_experience(api_app, client: AsyncClient, user):
    api_app.dependency_overrides[current_active_superuser] = lambda: user

    response = await client.get("/api/v1/experience/secrets")

    assert response.status_code == 200
    assert response.json()["experience"] == ["secret-exp1", "secret-exp2", "secret-exp3"]


@pytest.mark.asyncio
async def test_unauthenticated_user_is_rejected(api_app, client: AsyncClient):
    def reject_request():
        raise HTTPException(status_code=401, detail="Unauthorized")

    api_app.dependency_overrides[current_active_user] = reject_request

    response = await client.get("/api/v1/experience")

    assert response.status_code == 401
