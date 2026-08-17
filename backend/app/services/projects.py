from bson import ObjectId
from fastapi import HTTPException

from core.models import PROJECTS_COLLECTION, ProjectModel, mongo_database
from core.schemas.project import ProjectCreateSchema, ProjectReadSchema, ProjectUpdateSchema
from utils import singleton


@singleton
class ProjectsService:
    @property
    def collection(self):
        return mongo_database()[PROJECTS_COLLECTION]

    async def list_projects(self, user_id: str) -> list[ProjectReadSchema]:
        cursor = self.collection.find({"user_id": user_id}).sort([("sort_order", 1), ("_id", 1)])
        return [ProjectModel.from_document(document).to_read_schema() async for document in cursor]

    async def create_project(self, user_id: str, project: ProjectCreateSchema) -> ProjectReadSchema:
        result = await self.collection.insert_one(ProjectModel.from_create(user_id, project).to_document())
        return await self._get_project(user_id, result.inserted_id)

    async def update_project(self, user_id: str, project_id: str, patch: ProjectUpdateSchema) -> ProjectReadSchema:
        object_id = self._object_id(project_id)
        update = patch.model_dump(exclude_unset=True, mode="json")
        document = await self.collection.find_one_and_update(
            {"_id": object_id, "user_id": user_id},
            {"$set": update},
            return_document=True,
        )
        if document is None:
            raise HTTPException(404, "Project not found")
        return ProjectModel.from_document(document).to_read_schema()

    async def delete_project(self, user_id: str, project_id: str) -> str:
        result = await self.collection.delete_one({"_id": self._object_id(project_id), "user_id": user_id})
        if not result.deleted_count:
            raise HTTPException(404, "Project not found")
        return project_id

    async def _get_project(self, user_id: str, project_id: ObjectId) -> ProjectReadSchema:
        document = await self.collection.find_one({"_id": project_id, "user_id": user_id})
        if document is None:
            raise HTTPException(404, "Project not found")
        return ProjectModel.from_document(document).to_read_schema()

    @staticmethod
    def _object_id(project_id: str) -> ObjectId:
        if not ObjectId.is_valid(project_id):
            raise HTTPException(404, "Project not found")
        return ObjectId(project_id)
