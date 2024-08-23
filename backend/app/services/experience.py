from typing import List
from fastapi import HTTPException
from odmantic import AIOEngine

from core.models import (
    ExperienceModel,
    ContactInformationModel,
    WorkExperienceModel,
    mongo_helper,
)
from core.schemas.experience import (
    ExperienceCreateSchema,
    ExperienceReadSchema,
    ContactInformationSchema,
    WorkExperienceSchema,
    ExperienceUpdateSchema,
)
from core.types.experience_id import ExperienceId
from utils import singleton


@singleton
class ExperienceService:

    def __init__(self):
        self.__engine: AIOEngine = mongo_helper.get_engine()

    async def get_experience(self, user_id: str) -> ExperienceReadSchema:
        db_experience: ExperienceModel = await self.__engine.find_one(
            ExperienceModel,
            ExperienceModel.user_id == user_id,
        )
        if db_experience is None:
            raise HTTPException(404, "Experience not found by user id")
        return self.__return_experience_schema(db_experience)

    async def create_experience(
        self,
        user_id: str,
        experience_create: ExperienceCreateSchema,
    ) -> ExperienceId:
        experience_model: ExperienceModel = self.__return_experience_model(
            user_id,
            experience_create,
        )
        db_experience = await self.__engine.save(experience_model)
        return str(db_experience.id)

    async def delete_experience(
        self,
        user_id: str,
    ) -> ExperienceId:
        db_experience = await self.__engine.find_one(
            ExperienceModel,
            ExperienceModel.user_id == user_id,
        )
        if db_experience is None:
            raise HTTPException(404)
        await self.__engine.delete(db_experience)
        return str(db_experience.id)

    async def update_experience(
        self,
        user_id: str,
        patch: ExperienceUpdateSchema,
    ) -> ExperienceId:
        db_experience = await self.__engine.find_one(
            ExperienceModel,
            ExperienceModel.user_id == user_id,
        )
        if db_experience is None:
            raise HTTPException(404)
        db_experience.model_update(patch)
        db_experience = await self.__engine.save(db_experience)
        return str(db_experience.id)

    @staticmethod
    def __return_experience_model(
        user_id: str,
        experience_create: ExperienceCreateSchema,
    ) -> ExperienceModel:
        contact_information_model: ContactInformationModel = ContactInformationModel(
            first_name=experience_create.contact_information.first_name,
            last_name=experience_create.contact_information.last_name,
            email=experience_create.contact_information.email,
        )
        work_experience_model: List[WorkExperienceModel] = [
            WorkExperienceModel(
                company_name=item.company_name,
                company_description=item.company_description,
                position=item.position,
            )
            for item in experience_create.work_experience
        ]
        experience_model: ExperienceModel = ExperienceModel(
            user_id=user_id,
            title=experience_create.title,
            contact_information=contact_information_model,
            professional_summary=experience_create.professional_summary,
            work_experience=work_experience_model,
        )
        return experience_model

    @staticmethod
    def __return_experience_schema(
        db_experience: ExperienceModel,
    ) -> ExperienceReadSchema:
        contact_information: ContactInformationSchema = ContactInformationSchema(
            first_name=db_experience.contact_information.first_name,
            last_name=db_experience.contact_information.first_name,
            email=db_experience.contact_information.email,
        )
        work_experience: List[WorkExperienceSchema] = [
            WorkExperienceSchema(
                company_name=item.company_name,
                company_description=item.company_description,
                position=item.position,
            )
            for item in db_experience.work_experience
        ]
        experience_read: ExperienceReadSchema = ExperienceReadSchema(
            id=str(db_experience.id),
            user_id=db_experience.user_id,
            title=db_experience.title,
            contact_information=contact_information,
            professional_summary=db_experience.professional_summary,
            work_experience=work_experience,
            education=db_experience.education,
            certifications=db_experience.certifications,
            publications=db_experience.publications,
            skills=db_experience.skills,
            interests=db_experience.interests,
        )
        return experience_read
