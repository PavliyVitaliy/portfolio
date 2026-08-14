from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from core.schemas.experience import ExperienceCreateSchema, ExperienceReadSchema


EXPERIENCE_COLLECTION = "experience"


class WorkExperienceModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    company_name: str
    company_description: str
    position: str
    location: str | None = None
    Type: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    achievements: list[str] | None = None


class ContactInformationModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    first_name: str
    last_name: str
    email: str
    phone_number: str | None = None
    linkedin: str | None = None
    twitter: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    website: str | None = None


class ExperienceModel(BaseModel):
    """Validated domain representation of an experience MongoDB document."""

    model_config = ConfigDict(extra="ignore")

    id: str | None = Field(default=None)
    user_id: str
    title: str
    contact_information: ContactInformationModel
    professional_summary: str
    work_experience: list[WorkExperienceModel]
    education: list[str] | None = None
    certifications: list[str] | None = None
    publications: list[str] | None = None
    skills: list[str] | None = None
    interests: list[str] | None = None

    @classmethod
    def from_create(cls, user_id: str, experience: ExperienceCreateSchema) -> "ExperienceModel":
        data = experience.model_dump(exclude={"user_id"})
        return cls(user_id=user_id, **data)

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "ExperienceModel":
        data = dict(document)
        data["id"] = str(data.pop("_id"))
        return cls.model_validate(data)

    def to_document(self) -> dict[str, Any]:
        """Return a MongoDB-ready document without its database-generated id."""
        return self.model_dump(exclude={"id"}, mode="json")

    def to_read_schema(self) -> ExperienceReadSchema:
        if self.id is None:
            raise ValueError("Experience id is required for an API response")
        return ExperienceReadSchema.model_validate(
            {"id": self.id, **self.model_dump(exclude={"id"}, mode="json")}
        )
