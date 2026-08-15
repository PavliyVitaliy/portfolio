import "server-only";

export const AUTH_COOKIE_NAME = "portfolio_access_token";

const apiBaseUrl = process.env.API_BASE_URL;

if (!apiBaseUrl) {
  throw new Error("API_BASE_URL is not configured");
}

export const managementExperienceUrl = `${apiBaseUrl}/experience`;

export async function loginToBackend(email: string, password: string) {
  return fetch(`${apiBaseUrl}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password }),
    cache: "no-store",
  });
}

export function authHeaders(accessToken: string) {
  return { Authorization: `Bearer ${accessToken}` };
}

export const authCookieOptions = {
  httpOnly: true,
  sameSite: "lax" as const,
  secure: process.env.NODE_ENV === "production",
  path: "/",
  maxAge: 60 * 60,
};
