from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from core.schemas.profile import ProfileCreateSchema, ProfileReadSchema


PROFILE_COLLECTION = "profile"


class ProfileModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = Field(default=None)
    user_id: str
    photo_filename: str | None = None
    availability: str | None = None
    github_url: str | None = None

    @classmethod
    def from_create(cls, user_id: str, profile: ProfileCreateSchema) -> "ProfileModel":
        return cls(user_id=user_id, **profile.model_dump())

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "ProfileModel":
        data = dict(document)
        data["id"] = str(data.pop("_id"))
        return cls.model_validate(data)

    def to_document(self) -> dict[str, Any]:
        return self.model_dump(exclude={"id"}, mode="json")

    def to_read_schema(self) -> ProfileReadSchema:
        if self.id is None:
            raise ValueError("Profile id is required for an API response")
        return ProfileReadSchema.model_validate(
            {"id": self.id, **self.model_dump(exclude={"id"}, mode="json")}
        )
