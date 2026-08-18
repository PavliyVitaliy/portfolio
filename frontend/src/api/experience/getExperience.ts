import type { Experience } from './experience';

const API_BASE_URL = process.env.API_BASE_URL;

export async function getExperience(): Promise<Experience | null> {
    let res = await fetch(`${API_BASE_URL}/experience/free`);

    if (res.status === 404) {
        return null;
    }

    if (!res.ok) {
        throw new Error('Something went wrong!');
    }

    return (await res.json()) as Experience;
}
