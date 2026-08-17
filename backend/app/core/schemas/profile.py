from pydantic import BaseModel


class ProfileBaseSchema(BaseModel):
    photo_filename: str | None = None
    availability: str | None = None
    github_url: str | None = None


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileUpdateSchema(ProfileBaseSchema):
    pass


class ProfileReadSchema(ProfileBaseSchema):
    id: str
    user_id: str
