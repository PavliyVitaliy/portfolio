import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from api.api_v1.fastapi_users import current_active_superuser


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_unauthenticated_user_is_rejected(client: AsyncClient):
    response = await client.patch("/api/v1/experience", json={"title": "Updated"})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_non_superuser_is_rejected(api_app, client: AsyncClient):
    def reject_request():
        raise HTTPException(status_code=403, detail="Superuser required")

    api_app.dependency_overrides[current_active_superuser] = reject_request

    response = await client.patch("/api/v1/experience", json={"title": "Updated"})

    assert response.status_code == 403
