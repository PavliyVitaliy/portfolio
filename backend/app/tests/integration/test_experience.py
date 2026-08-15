from uuid import uuid4
from types import SimpleNamespace

import pytest
from httpx import AsyncClient

from api.api_v1 import experience as experience_api
from api.api_v1.fastapi_users import current_active_superuser
from core.models import ExperienceModel
from core.schemas.experience import ExperienceCreateSchema
from core.schemas.experience import ExperienceReadSchema
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


def test_mongo_document_is_mapped_to_api_schema(experience_payload):
    document = {"_id": "experience-id", **experience_payload}

    experience = ExperienceService()._to_schema(document)

    assert experience.id == "experience-id"
    assert experience.contact_information.last_name == "Developer"


def test_domain_model_creates_mongo_document(experience_payload):
    experience = ExperienceModel.from_create(
        "actual-user-id", ExperienceCreateSchema(**experience_payload)
    )

    document = experience.to_document()

    assert "id" not in document
    assert document["user_id"] == "actual-user-id"
    assert document["work_experience"][0]["position"] == "Python Developer"


@pytest.fixture
def mock_superuser(api_app, user):
    api_app.dependency_overrides[current_active_superuser] = lambda: user
    return user


@pytest.mark.asyncio
async def test_create_experience(client: AsyncClient, mock_superuser, experience_payload, monkeypatch):
    async def create_experience(user_id, experience):
        assert user_id == str(mock_superuser.id)
        assert experience.title == experience_payload["title"]
        return "experience-id"

    monkeypatch.setattr(
        experience_api,
        "ExperienceService",
        lambda: SimpleNamespace(create_experience=create_experience),
    )

    response = await client.put("/api/v1/experience", json=experience_payload)

    assert response.status_code == 200
    assert response.json() == "experience-id"


@pytest.mark.asyncio
async def test_read_update_and_delete_experience(
    client: AsyncClient, mock_superuser, experience_payload, monkeypatch
):
    experience = ExperienceReadSchema(id="experience-id", **experience_payload)

    async def get_experience(user_id):
        assert user_id == str(mock_superuser.id)
        return experience

    async def update_experience(user_id, patch):
        assert user_id == str(mock_superuser.id)
        assert patch.title == "Senior Python Developer"
        return "experience-id"

    async def delete_experience(user_id):
        assert user_id == str(mock_superuser.id)
        return "experience-id"

    monkeypatch.setattr(
        experience_api,
        "ExperienceService",
        lambda: SimpleNamespace(
            get_experience=get_experience,
            update_experience=update_experience,
            delete_experience=delete_experience,
        ),
    )

    read_response = await client.get("/api/v1/experience")
    update_response = await client.patch(
        "/api/v1/experience", json={"title": "Senior Python Developer"}
    )
    forbidden_update_response = await client.patch(
        "/api/v1/experience", json={"user_id": str(uuid4())}
    )
    delete_response = await client.delete("/api/v1/experience")

    assert read_response.status_code == 200
    assert read_response.json()["id"] == "experience-id"
    assert update_response.status_code == 200
    assert update_response.json() == "experience-id"
    assert forbidden_update_response.status_code == 403
    assert delete_response.status_code == 200
    assert delete_response.json() == "experience-id"
