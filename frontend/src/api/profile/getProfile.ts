import type { Profile } from "./profile";

const API_BASE_URL = process.env.API_BASE_URL;

export async function getProfile(): Promise<Profile | null> {
  const response = await fetch(`${API_BASE_URL}/profile/free`, { cache: "no-store" });
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error("Unable to load profile");
  }
  return response.json() as Promise<Profile>;
}

export function profileImageUrl(filename?: string | null) {
  return filename ? `${API_BASE_URL}/file/profile/${encodeURIComponent(filename)}` : null;
}
