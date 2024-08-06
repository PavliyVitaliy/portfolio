from typing import List, Optional
from odmantic import (
    Model,
    Field,
    EmbeddedModel,
)


class WorkExperience(EmbeddedModel):
    company_name: str = Field(...)
    company_description: str = Field(...)
    position: str = Field(...)
    location: Optional[str] = None
    Type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: Optional[List[str]] = None


class ContactInformation(EmbeddedModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    phone_number: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    website: Optional[str] = None


class Experience(Model):
    user_id: str = Field(unique=True)
    title: str = Field(...)  # "Senior Full-Stack Software Engineer"
    contact_information: ContactInformation
    professional_summary: str = Field(...)
    work_experience: List[WorkExperience]
    education: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    interests: Optional[List[str]] = None
