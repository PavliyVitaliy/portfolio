export type WorkExperience = {
    company_name?: string;
    company_description?: string;
    position?: string;
    location?: string;
    Type?: string;
    start_date?: string;
    end_date?: string;
    achievements?: string[];
}

export type ContactInformation = {
    first_name?: string;
    last_name?: string;
    email?: string;
    phone_number?: string;
    linkedin?: string;
    twitter?: string;
    address?: string;
    city?: string;
    state?: string;
    website?: string;
}

export type Experience = {
    id: string;
    user_id: string;
    title?: string;
    contact_information?: ContactInformation;
    professional_summary?: string;
    work_experience?: WorkExperience[];
    education?: string[];
    certifications?: string[];
    publications?: string[];
    skills?: string[];
    interests?: string[];
};
