from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import HTTPException

from core.models import (
    EXPERIENCE_COLLECTION,
    mongo_close,
    mongo_configure_database,
    mongo_database,
)
from core.schemas.experience import ExperienceCreateSchema, ExperienceUpdateSchema
from services.experience import ExperienceService


@pytest.fixture
def experience_payload() -> dict:
    return {
        "user_id": str(uuid4()),
        "title": "Python Developer",
        "contact_information": {
            "first_name": "Vitalii",
            "last_name": "Developer",
            "email": "vitalii@example.com",
        },
        "professional_summary": "Backend developer",
        "work_experience": [
            {
                "company_name": "Example",
                "company_description": "Example company",
                "position": "Python Developer",
            }
        ],
    }


@pytest_asyncio.fixture
async def mongo_collection():
    await mongo_close()
    collection = mongo_database()[EXPERIENCE_COLLECTION]
    await mongo_configure_database()
    try:
        yield collection
    finally:
        await mongo_close()


@pytest.mark.asyncio
async def test_mongo_experience_crud(experience_payload, mongo_collection):
    user_id = str(uuid4())
    service = ExperienceService()

    try:
        experience_id = await service.create_experience(
            user_id, ExperienceCreateSchema(**experience_payload)
        )

        experience = await service.get_experience(user_id)
        assert experience.id == experience_id
        assert experience.title == "Python Developer"

        updated_id = await service.update_experience(
            user_id, ExperienceUpdateSchema(title="Senior Python Developer")
        )
        assert updated_id == experience_id
        assert (await service.get_experience(user_id)).title == "Senior Python Developer"

        deleted_id = await service.delete_experience(user_id)
        assert deleted_id == experience_id

        with pytest.raises(HTTPException, match="Experience not found") as error:
            await service.get_experience(user_id)
        assert error.value.status_code == 404
    finally:
        await mongo_collection.delete_many({"user_id": user_id})


@pytest.mark.asyncio
async def test_mongo_rejects_duplicate_user_experience(
    experience_payload, mongo_collection
):
    user_id = str(uuid4())
    service = ExperienceService()

    try:
        payload = ExperienceCreateSchema(**experience_payload)
        await service.create_experience(user_id, payload)

        with pytest.raises(HTTPException, match="Experience already exists") as error:
            await service.create_experience(user_id, payload)
        assert error.value.status_code == 409
    finally:
        await mongo_collection.delete_many({"user_id": user_id})
