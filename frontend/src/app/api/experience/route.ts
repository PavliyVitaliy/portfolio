import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import {
  AUTH_COOKIE_NAME,
  authCookieOptions,
  authHeaders,
  managementExperienceUrl,
} from "@/lib/auth";

async function proxyExperienceRequest(method: string, request?: Request) {
  const accessToken = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!accessToken) {
    return NextResponse.json({ detail: "Authentication required." }, { status: 401 });
  }

  const body = request ? await request.text() : undefined;
  const backendResponse = await fetch(managementExperienceUrl, {
    method,
    headers: {
      ...authHeaders(accessToken),
      ...(body ? { "Content-Type": "application/json" } : {}),
    },
    body,
    cache: "no-store",
  });
  const responseBody = await backendResponse.text();
  const response = new NextResponse(responseBody || null, {
    status: backendResponse.status,
    headers: {
      "Content-Type": backendResponse.headers.get("Content-Type") ?? "application/json",
    },
  });

  if (backendResponse.status === 401 || backendResponse.status === 403) {
    response.cookies.set(AUTH_COOKIE_NAME, "", { ...authCookieOptions, maxAge: 0 });
  }

  return response;
}

export async function GET() {
  return proxyExperienceRequest("GET");
}

export async function PUT(request: Request) {
  return proxyExperienceRequest("PUT", request);
}

export async function PATCH(request: Request) {
  return proxyExperienceRequest("PATCH", request);
}

export async function DELETE() {
  return proxyExperienceRequest("DELETE");
}
