export type NavigationItem = {
    name: string;
    slug: string;
    description?: string;
};
  
export const navigationData: { name: string; items: NavigationItem[] }[] = [
    {
        name: 'Summary',
        items: [
            {
                name: 'About Me',
                slug: 'summary',
                description: 'Professional Summary',
            },
        ],
    },
    {
        name: 'Experience',
        items: [
            {
                name: 'Work Experience',
                slug: 'work-experience',
                description: 'Work Experience',
            },
            {
                name: 'Self Experience',
                slug: 'self-experience',
                description: 'Self Experience',
            },
        ],
    },
    {
        name: 'Education',
        items: [
            {
                name: 'Education',
                slug: 'education',
                description: 'Education, certifications',
            },
        ],
    },
    {
        name: 'Skills',
        items: [
            {
                name: 'Skills',
                slug: 'skills',
                description: 'Skills',
            },
        ],
    },
    {
        name: 'Interests',
        items: [
            {
                name: 'Interests',
                slug: 'interests',
                description: 'Interests, hobby',
            },
        ],
    },
];