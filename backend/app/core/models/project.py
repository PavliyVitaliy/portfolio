from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from core.schemas.project import ProjectCreateSchema, ProjectReadSchema


PROJECTS_COLLECTION = "projects"


class ProjectModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str | None = Field(default=None)
    user_id: str
    title: str
    description: str
    url: HttpUrl
    repository_url: HttpUrl | None = None
    stack: list[str] | None = None
    featured: bool = False
    sort_order: int = 0

    @classmethod
    def from_create(cls, user_id: str, project: ProjectCreateSchema) -> "ProjectModel":
        return cls(user_id=user_id, **project.model_dump())

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> "ProjectModel":
        data = dict(document)
        data["id"] = str(data.pop("_id"))
        return cls.model_validate(data)

    def to_document(self) -> dict[str, Any]:
        return self.model_dump(exclude={"id"}, mode="json")

    def to_read_schema(self) -> ProjectReadSchema:
        if self.id is None:
            raise ValueError("Project id is required for an API response")
        return ProjectReadSchema.model_validate(
            {"id": self.id, **self.model_dump(exclude={"id"}, mode="json")}
        )
