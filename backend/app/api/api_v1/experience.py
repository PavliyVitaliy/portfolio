from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)
from core.config import settings
from core.models import User, db_helper
from core.schemas.user import UserRead
from services.users import get_super_user
from services.experience import get_experience

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


@router.get("/free")
async def get_free_experience(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter)
    ],
):
    super_user = await get_super_user(session=session)
    experience = await get_experience(str(super_user.id))
    return experience
