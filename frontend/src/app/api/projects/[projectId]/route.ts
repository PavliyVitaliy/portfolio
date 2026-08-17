import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { AUTH_COOKIE_NAME, authCookieOptions, authHeaders, managementProjectsUrl } from "@/lib/auth";

async function proxy(method: string, request: Request, projectId: string) {
  const token = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!token) return NextResponse.json({ detail: "Authentication required." }, { status: 401 });
  const body = method === "DELETE" ? undefined : await request.text();
  const backendResponse = await fetch(`${managementProjectsUrl}/${encodeURIComponent(projectId)}`, {
    method,
    headers: { ...authHeaders(token), ...(body ? { "Content-Type": "application/json" } : {}) },
    body,
    cache: "no-store",
  });
  const response = new NextResponse(await backendResponse.text(), { status: backendResponse.status });
  if (backendResponse.status === 401 || backendResponse.status === 403) response.cookies.set(AUTH_COOKIE_NAME, "", { ...authCookieOptions, maxAge: 0 });
  return response;
}

export async function PATCH(request: Request, context: RouteContext<"/api/projects/[projectId]">) {
  return proxy("PATCH", request, (await context.params).projectId);
}
export async function DELETE(request: Request, context: RouteContext<"/api/projects/[projectId]">) {
  return proxy("DELETE", request, (await context.params).projectId);
}
