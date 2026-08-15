import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import {
  AUTH_COOKIE_NAME,
  authHeaders,
  managementExperienceUrl,
} from "@/lib/auth";
import type { Experience } from "@/api/experience/experience";

import { ExperienceEditor } from "./experience-editor";
import { LogoutButton } from "./logout-button";

export const dynamic = "force-dynamic";

export default async function AdminPage() {
  const accessToken = (await cookies()).get(AUTH_COOKIE_NAME)?.value;
  if (!accessToken) {
    redirect("/login");
  }

  const backendResponse = await fetch(managementExperienceUrl, {
    headers: authHeaders(accessToken),
    cache: "no-store",
  });

  if (backendResponse.status === 401) {
    redirect("/login");
  }

  if (backendResponse.status === 403) {
    return (
      <main className="mx-auto grid min-h-screen max-w-2xl content-center px-6 py-12">
        <h1 className="text-2xl font-semibold">Доступ запрещён</h1>
        <p className="mt-2 text-muted-foreground">Требуются права администратора.</p>
      </main>
    );
  }

  if (!backendResponse.ok && backendResponse.status !== 404) {
    return (
      <main className="mx-auto grid min-h-screen max-w-2xl content-center px-6 py-12">
        <h1 className="text-2xl font-semibold">Не удалось загрузить профиль</h1>
        <p className="mt-2 text-muted-foreground">Повторите попытку позже.</p>
      </main>
    );
  }

  const experience = backendResponse.ok
    ? ((await backendResponse.json()) as Experience)
    : null;
  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <header className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Админ-панель</h1>
          <p className="mt-1 text-muted-foreground">
            {experience
              ? "Опыт загружен и готов к редактированию."
              : "Запись опыта ещё не создана."}
          </p>
        </div>
        <LogoutButton />
      </header>
      <ExperienceEditor initialExperience={experience} />
    </main>
  );
}
