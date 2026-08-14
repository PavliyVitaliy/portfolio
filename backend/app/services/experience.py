from fastapi import HTTPException
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from core.models import EXPERIENCE_COLLECTION, mongo_database
from core.schemas.experience import ExperienceCreateSchema, ExperienceReadSchema, ExperienceUpdateSchema
from core.types.experience_id import ExperienceId
from utils import singleton


@singleton
class ExperienceService:
    @property
    def collection(self):
        return mongo_database()[EXPERIENCE_COLLECTION]

    async def get_experience(self, user_id: str) -> ExperienceReadSchema:
        document = await self.collection.find_one({"user_id": user_id})
        if document is None:
            raise HTTPException(404, "Experience not found by user id")
        return self._to_schema(document)

    async def create_experience(
        self, user_id: str, experience_create: ExperienceCreateSchema
    ) -> ExperienceId:
        document = experience_create.model_dump(mode="json")
        document["user_id"] = user_id
        try:
            result = await self.collection.insert_one(document)
        except DuplicateKeyError as error:
            raise HTTPException(409, "Experience already exists for this user") from error
        return str(result.inserted_id)

    async def delete_experience(self, user_id: str) -> ExperienceId:
        document = await self.collection.find_one_and_delete({"user_id": user_id})
        if document is None:
            raise HTTPException(404, "Experience not found by user id")
        return str(document["_id"])

    async def update_experience(
        self, user_id: str, patch: ExperienceUpdateSchema
    ) -> ExperienceId:
        update = patch.model_dump(exclude_unset=True, exclude={"user_id"})
        if not update:
            document = await self.collection.find_one({"user_id": user_id})
        else:
            document = await self.collection.find_one_and_update(
                {"user_id": user_id},
                {"$set": update},
                return_document=ReturnDocument.AFTER,
            )
        if document is None:
            raise HTTPException(404, "Experience not found by user id")
        return str(document["_id"])

    @staticmethod
    def _to_schema(document: dict) -> ExperienceReadSchema:
        document = dict(document)
        document["id"] = str(document.pop("_id"))
        return ExperienceReadSchema.model_validate(document)
