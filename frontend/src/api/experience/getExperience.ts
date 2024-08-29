import { notFound } from 'next/navigation';
import type { Experience } from './experience';

const API_BASE_URL = process.env.API_BASE_URL;

export async function getExperience() {
    let res = await fetch(`${API_BASE_URL}/experience/free`);
    
    if (!res.ok) {
        throw new Error('Something went wrong!');
    }

    const experience = (await res.json()) as Experience;

    if (!experience) {
        notFound();
    }

    return experience;
}
