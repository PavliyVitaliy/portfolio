from uuid import uuid4

import pytest
import pytest_asyncio

from core.models import mongo_close, mongo_configure_database, mongo_database
from core.schemas.profile import ProfileCreateSchema, ProfileUpdateSchema
from core.schemas.project import ProjectCreateSchema, ProjectUpdateSchema
from services.profile import ProfileService
from services.projects import ProjectsService


@pytest_asyncio.fixture
async def portfolio_database():
    await mongo_close()
    database = mongo_database()
    await mongo_configure_database()
    try:
        yield database
    finally:
        await mongo_close()


@pytest.mark.asyncio
async def test_mongo_profile_create_update_and_photo(portfolio_database):
    user_id = str(uuid4())
    service = ProfileService()
    try:
        profile = await service.create_profile(
            user_id,
            ProfileCreateSchema(
                availability="Open to opportunities",
                github_url="https://github.com/example",
            ),
        )
        assert profile.availability == "Open to opportunities"

        updated = await service.update_profile(
            user_id, ProfileUpdateSchema(availability="Available for interviews")
        )
        assert updated.github_url == "https://github.com/example"

        with_photo = await service.upsert_photo(user_id, "portrait.webp")
        assert with_photo.photo_filename == "portrait.webp"
    finally:
        await portfolio_database.profile.delete_many({"user_id": user_id})


@pytest.mark.asyncio
async def test_mongo_projects_crud(portfolio_database):
    user_id = str(uuid4())
    service = ProjectsService()
    try:
        project = await service.create_project(
            user_id,
            ProjectCreateSchema(
                title="Portfolio",
                description="A personal portfolio site",
                url="https://example.com",
                repository_url="https://github.com/example/portfolio",
                stack=["Next.js", "FastAPI"],
                featured=True,
            ),
        )
        assert (await service.list_projects(user_id))[0].title == "Portfolio"

        updated = await service.update_project(
            user_id, project.id, ProjectUpdateSchema(sort_order=2)
        )
        assert updated.sort_order == 2

        assert await service.delete_project(user_id, project.id) == project.id
        assert await service.list_projects(user_id) == []
    finally:
        await portfolio_database.projects.delete_many({"user_id": user_id})
