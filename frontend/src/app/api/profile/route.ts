import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { AUTH_COOKIE_NAME, authCookieOptions, authHeaders, managementProfileUrl } from "@/lib/auth";

async function proxy(method: string, request?: Request) {
  const token = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!token) return NextResponse.json({ detail: "Authentication required." }, { status: 401 });
  const body = request ? await request.text() : undefined;
  const backendResponse = await fetch(managementProfileUrl, {
    method,
    headers: { ...authHeaders(token), ...(body ? { "Content-Type": "application/json" } : {}) },
    body,
    cache: "no-store",
  });
  const response = new NextResponse(await backendResponse.text(), { status: backendResponse.status });
  if (backendResponse.status === 401 || backendResponse.status === 403) {
    response.cookies.set(AUTH_COOKIE_NAME, "", { ...authCookieOptions, maxAge: 0 });
  }
  return response;
}

export async function GET() { return proxy("GET"); }
export async function PUT(request: Request) { return proxy("PUT", request); }
export async function PATCH(request: Request) { return proxy("PATCH", request); }
