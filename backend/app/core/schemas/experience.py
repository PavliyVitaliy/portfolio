from pydantic import BaseModel
from typing import List, Optional


class ContactInformation(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None


class WorkExperience(BaseModel):
    company_name: str
    company_description: str
    position: str
    location: Optional[str] = None
    Type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: Optional[List[str]] = None


class ExperienceBase(BaseModel):
    user_id: str
    title: str  # "Senior Full-Stack Software Engineer"
    contact_information: ContactInformation
    professional_summary: str
    work_experience: List[WorkExperience]
    education: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceRead(ExperienceBase):
    id: str
