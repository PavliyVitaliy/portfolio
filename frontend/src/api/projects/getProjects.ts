import type { Project } from "./project";

const API_BASE_URL = process.env.API_BASE_URL;

export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${API_BASE_URL}/projects/free`, { cache: "no-store" });
  if (response.status === 404) {
    return [];
  }
  if (!response.ok) {
    throw new Error("Unable to load projects");
  }
  return response.json() as Promise<Project[]>;
}
