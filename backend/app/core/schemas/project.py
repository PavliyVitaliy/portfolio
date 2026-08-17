from pydantic import BaseModel, HttpUrl


class ProjectBaseSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    url: HttpUrl | None = None
    repository_url: HttpUrl | None = None
    stack: list[str] | None = None
    featured: bool | None = None
    sort_order: int | None = None


class ProjectCreateSchema(ProjectBaseSchema):
    title: str
    description: str
    url: HttpUrl
    featured: bool = False
    sort_order: int = 0


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectReadSchema(ProjectCreateSchema):
    id: str
    user_id: str
