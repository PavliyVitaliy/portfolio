import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { AUTH_COOKIE_NAME, authCookieOptions, authHeaders, managementProfileImageUrl } from "@/lib/auth";

export async function POST(request: Request) {
  const token = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!token) return NextResponse.json({ detail: "Authentication required." }, { status: 401 });
  const backendResponse = await fetch(managementProfileImageUrl, {
    method: "POST",
    headers: authHeaders(token),
    body: await request.formData(),
    cache: "no-store",
  });
  const response = new NextResponse(await backendResponse.text(), { status: backendResponse.status });
  if (backendResponse.status === 401 || backendResponse.status === 403) {
    response.cookies.set(AUTH_COOKIE_NAME, "", { ...authCookieOptions, maxAge: 0 });
  }
  return response;
}
