from pydantic import BaseModel
from typing import List, Optional


class ContactInformationBaseSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None


class ContactInformationSchema(ContactInformationBaseSchema):
    first_name: str
    last_name: str
    email: str


class WorkExperienceBaseSchema(BaseModel):
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    Type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: Optional[List[str]] = None


class WorkExperienceSchema(WorkExperienceBaseSchema):
    company_name: str
    company_description: str
    position: str


class ExperienceBaseSchema(BaseModel):
    user_id: Optional[str] = None
    title: Optional[str] = None
    contact_information: Optional[ContactInformationBaseSchema] = None
    professional_summary: Optional[str] = None
    work_experience: Optional[List[WorkExperienceBaseSchema]]
    education: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class ExperienceSchema(ExperienceBaseSchema):
    user_id: str
    title: str
    contact_information: ContactInformationSchema
    professional_summary: str
    work_experience: List[WorkExperienceSchema]


class ExperienceCreateSchema(ExperienceSchema):
    pass


class ExperienceReadSchema(ExperienceSchema):
    id: str


class ExperienceUpdateSchema(ExperienceBaseSchema):
    pass
