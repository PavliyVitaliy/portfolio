import pytest

from httpx import AsyncClient
from fastapi import FastAPI
from core.config import settings

from starlette.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


class TestUsers:
    @pytest.mark.asyncio
    async def test_is_superuser_exist(self, client: AsyncClient):
        response = await client.get(
            f"/{settings.api}/{settings.api.v1}/{settings.api.v1.experience}/free"
        )
        assert response.status_code == HTTP_200_OK
        print("response")
        print(response)
