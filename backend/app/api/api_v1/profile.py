from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_superuser
from core.models import User, db_helper
from core.schemas.profile import ProfileCreateSchema, ProfileReadSchema, ProfileUpdateSchema
from services.profile import ProfileService
from services.users import get_super_user


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/free", response_model=ProfileReadSchema)
async def get_free_profile(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    super_user: User | None = await get_super_user(session=session)
    if super_user is None:
        raise HTTPException(404, "Superuser not found")
    return await ProfileService().get_profile(str(super_user.id))


@router.get("", response_model=ProfileReadSchema)
async def get_profile(user: Annotated[User, Depends(current_active_superuser)]):
    return await ProfileService().get_profile(str(user.id))


@router.put("", response_model=ProfileReadSchema)
async def create_profile(
    profile: ProfileCreateSchema,
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ProfileService().create_profile(str(user.id), profile)


@router.patch("", response_model=ProfileReadSchema)
async def update_profile(
    patch: ProfileUpdateSchema,
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ProfileService().update_profile(str(user.id), patch)
