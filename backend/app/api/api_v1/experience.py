from typing import Annotated

from fastapi import APIRouter, Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)
from core.config import settings
from core.models import User
from core.schemas.user import UserRead

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
