from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)
from core.config import settings
from core.models import User, db_helper
from core.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceReadSchema,
    ExperienceUpdateSchema,
)
from core.schemas.user import UserRead
from core.types.experience_id import ExperienceId
from services.users import get_super_user
from services.experience import ExperienceService

router = APIRouter(
    prefix=settings.api.v1.experience,
    tags=["Experience"],
)


@router.get("")
def get_user_experience(
        user: Annotated[
            User,
            Depends(current_active_user),
        ],
):
    return {
        "user": UserRead.model_validate(user),
        "experience": ["exp1", "exp2", "exp3"],
    }


@router.get("/secrets")
def get_superuser_experience(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return {
        "user": UserRead.model_validate(user),
        "experience": ["secret-exp1", "secret-exp2", "secret-exp3"],
    }


@router.get("/free", response_model=ExperienceReadSchema)
async def get_free_experience(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
):
    super_user: User = await get_super_user(session=session)
    experience: ExperienceReadSchema = await ExperienceService().get_experience(
        str(super_user.id),
    )
    return experience


@router.put("/free", response_model=ExperienceId)
async def create_free_experience(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    experience_create: ExperienceCreateSchema,
):
    super_user: User = await get_super_user(session=session)
    experience_id: ExperienceId = await ExperienceService().create_experience(
        str(super_user.id),
        experience_create,
    )
    return experience_id


@router.delete("/free", response_model=ExperienceId)
async def delete_free_experience(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
):
    super_user: User = await get_super_user(session=session)
    experience_id: ExperienceId = await ExperienceService().delete_experience(
        str(super_user.id),
    )
    return experience_id


@router.patch("/free", response_model=ExperienceId)
async def update_free_experience(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
    patch: ExperienceUpdateSchema,
):
    super_user: User = await get_super_user(session=session)
    if patch.user_id is not None and str(super_user.id) != patch.user_id:
        raise HTTPException(403, "Changing user id is forbidden!")
    experience_id: ExperienceId = await ExperienceService().update_experience(
        str(super_user.id),
        patch,
    )
    return experience_id
