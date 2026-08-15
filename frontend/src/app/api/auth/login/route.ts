import { NextResponse } from "next/server";

import {
  AUTH_COOKIE_NAME,
  authCookieOptions,
  loginToBackend,
} from "@/lib/auth";

type LoginRequest = {
  email?: unknown;
  password?: unknown;
};

type LoginResponse = {
  access_token?: unknown;
};

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as LoginRequest | null;
  const email = typeof body?.email === "string" ? body.email.trim() : "";
  const password = typeof body?.password === "string" ? body.password : "";

  if (!email || !password) {
    return NextResponse.json(
      { detail: "Email and password are required." },
      { status: 400 },
    );
  }

  const backendResponse = await loginToBackend(email, password);
  if (!backendResponse.ok) {
    return NextResponse.json(
      { detail: "Invalid email or password." },
      { status: backendResponse.status === 400 ? 401 : backendResponse.status },
    );
  }

  const payload = (await backendResponse.json()) as LoginResponse;
  if (typeof payload.access_token !== "string" || !payload.access_token) {
    return NextResponse.json(
      { detail: "Authentication service returned an invalid response." },
      { status: 502 },
    );
  }

  const response = new NextResponse(null, { status: 204 });
  response.cookies.set(AUTH_COOKIE_NAME, payload.access_token, authCookieOptions);
  return response;
}
