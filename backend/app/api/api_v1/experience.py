from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import (
    current_active_superuser,
)
from core.config import settings
from core.models import User, db_helper
from core.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceReadSchema,
    ExperienceUpdateSchema,
)
from core.types.experience_id import ExperienceId
from services.users import get_super_user
from services.experience import ExperienceService

router = APIRouter(
    prefix=settings.api.v1.experience,
    tags=["Experience"],
)


@router.get("/free", response_model=ExperienceReadSchema)
async def get_free_experience(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    super_user: User = await get_super_user(session=session)
    if super_user is None:
        raise HTTPException(404, "Superuser not found")
    experience: ExperienceReadSchema = await ExperienceService().get_experience(
        str(super_user.id),
    )
    return experience


@router.get("", response_model=ExperienceReadSchema)
async def get_experience(
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ExperienceService().get_experience(str(user.id))


@router.put("", response_model=ExperienceId)
async def create_experience(
    user: Annotated[User, Depends(current_active_superuser)],
    experience_create: ExperienceCreateSchema,
):
    experience_id: ExperienceId = await ExperienceService().create_experience(
        str(user.id),
        experience_create,
    )
    return experience_id


@router.delete("", response_model=ExperienceId)
async def delete_experience(
    user: Annotated[User, Depends(current_active_superuser)],
):
    experience_id: ExperienceId = await ExperienceService().delete_experience(str(user.id))
    return experience_id


@router.patch("", response_model=ExperienceId)
async def update_experience(
    user: Annotated[User, Depends(current_active_superuser)],
    patch: ExperienceUpdateSchema,
):
    if patch.user_id is not None and str(user.id) != patch.user_id:
        raise HTTPException(403, "Changing user id is forbidden!")
    experience_id: ExperienceId = await ExperienceService().update_experience(
        str(user.id),
        patch,
    )
    return experience_id
