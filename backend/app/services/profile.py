from fastapi import HTTPException

from core.models import PROFILE_COLLECTION, ProfileModel, mongo_database
from core.schemas.profile import ProfileCreateSchema, ProfileReadSchema, ProfileUpdateSchema
from utils import singleton


@singleton
class ProfileService:
    @property
    def collection(self):
        return mongo_database()[PROFILE_COLLECTION]

    async def get_profile(self, user_id: str) -> ProfileReadSchema:
        document = await self.collection.find_one({"user_id": user_id})
        if document is None:
            raise HTTPException(404, "Profile not found by user id")
        return ProfileModel.from_document(document).to_read_schema()

    async def create_profile(self, user_id: str, profile: ProfileCreateSchema) -> ProfileReadSchema:
        result = await self.collection.insert_one(ProfileModel.from_create(user_id, profile).to_document())
        return await self.get_profile_by_id(result.inserted_id)

    async def update_profile(self, user_id: str, patch: ProfileUpdateSchema) -> ProfileReadSchema:
        update = patch.model_dump(exclude_unset=True)
        if update:
            await self.collection.update_one({"user_id": user_id}, {"$set": update})
        return await self.get_profile(user_id)

    async def upsert_photo(self, user_id: str, filename: str) -> ProfileReadSchema:
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"photo_filename": filename}, "$setOnInsert": {"user_id": user_id}},
            upsert=True,
        )
        return await self.get_profile(user_id)

    async def get_profile_by_id(self, profile_id) -> ProfileReadSchema:
        document = await self.collection.find_one({"_id": profile_id})
        if document is None:
            raise HTTPException(404, "Profile not found")
        return ProfileModel.from_document(document).to_read_schema()
