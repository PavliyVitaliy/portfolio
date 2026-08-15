import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import {
  AUTH_COOKIE_NAME,
  authCookieOptions,
  authHeaders,
  managementExperienceUrl,
} from "@/lib/auth";

export async function GET() {
  const accessToken = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!accessToken) {
    return NextResponse.json({ authenticated: false });
  }

  const backendResponse = await fetch(managementExperienceUrl, {
    headers: authHeaders(accessToken),
    cache: "no-store",
  });

  if (backendResponse.status === 401 || backendResponse.status === 403) {
    const response = NextResponse.json({ authenticated: false });
    response.cookies.set(AUTH_COOKIE_NAME, "", { ...authCookieOptions, maxAge: 0 });
    return response;
  }

  return NextResponse.json({ authenticated: true });
}
