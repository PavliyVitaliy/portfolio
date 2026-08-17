from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import current_active_superuser
from core.models import User, db_helper
from core.schemas.project import ProjectCreateSchema, ProjectReadSchema, ProjectUpdateSchema
from services.projects import ProjectsService
from services.users import get_super_user


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/free", response_model=list[ProjectReadSchema])
async def list_free_projects(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    super_user: User | None = await get_super_user(session=session)
    if super_user is None:
        raise HTTPException(404, "Superuser not found")
    return await ProjectsService().list_projects(str(super_user.id))


@router.get("", response_model=list[ProjectReadSchema])
async def list_projects(user: Annotated[User, Depends(current_active_superuser)]):
    return await ProjectsService().list_projects(str(user.id))


@router.post("", response_model=ProjectReadSchema)
async def create_project(
    project: ProjectCreateSchema,
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ProjectsService().create_project(str(user.id), project)


@router.patch("/{project_id}", response_model=ProjectReadSchema)
async def update_project(
    project_id: str,
    patch: ProjectUpdateSchema,
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ProjectsService().update_project(str(user.id), project_id, patch)


@router.delete("/{project_id}", response_model=str)
async def delete_project(
    project_id: str,
    user: Annotated[User, Depends(current_active_superuser)],
):
    return await ProjectsService().delete_project(str(user.id), project_id)
