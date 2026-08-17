import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import {
  AUTH_COOKIE_NAME,
  authHeaders,
  managementExperienceUrl,
  managementProfileUrl,
  managementProjectsUrl,
} from "@/lib/auth";
import type { Experience } from "@/api/experience/experience";
import type { Profile } from "@/api/profile/profile";
import type { Project } from "@/api/projects/project";

import { ExperienceEditor } from "./experience-editor";
import { LogoutButton } from "./logout-button";
import { ProfileEditor } from "./profile-editor";
import { ProjectsEditor } from "./projects-editor";

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
        <h1 className="text-2xl font-semibold">Access denied</h1>
        <p className="mt-2 text-muted-foreground">Administrator access is required.</p>
      </main>
    );
  }

  if (!backendResponse.ok && backendResponse.status !== 404) {
    return (
      <main className="mx-auto grid min-h-screen max-w-2xl content-center px-6 py-12">
        <h1 className="text-2xl font-semibold">Unable to load profile</h1>
        <p className="mt-2 text-muted-foreground">Please try again later.</p>
      </main>
    );
  }

  const experience = backendResponse.ok
    ? ((await backendResponse.json()) as Experience)
    : null;
  const [profileResponse, projectsResponse] = await Promise.all([
    fetch(managementProfileUrl, { headers: authHeaders(accessToken), cache: "no-store" }),
    fetch(managementProjectsUrl, { headers: authHeaders(accessToken), cache: "no-store" }),
  ]);
  const profile = profileResponse.ok ? (await profileResponse.json()) as Profile : null;
  const projects = projectsResponse.ok ? (await projectsResponse.json()) as Project[] : [];
  return (
    <main className="mx-auto max-w-2xl px-6 py-12">
      <header className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Admin panel</h1>
          <p className="mt-1 text-muted-foreground">
            {experience
              ? "Experience is loaded and ready to edit."
              : "No experience record has been created yet."}
          </p>
        </div>
        <LogoutButton />
      </header>
      <ProfileEditor initialProfile={profile} />
      <ProjectsEditor initialProjects={projects} />
      <ExperienceEditor initialExperience={experience} />
    </main>
  );
}
