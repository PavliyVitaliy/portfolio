"use client";

import { useRouter } from "next/navigation";
import { type ChangeEvent, type FormEvent, useState } from "react";

import type { Profile } from "@/api/profile/profile";

export function ProfileEditor({ initialProfile }: Readonly<{ initialProfile: Profile | null }>) {
  const router = useRouter();
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true); setError(null);
    const form = new FormData(event.currentTarget);
    const response = await fetch("/api/profile", { method: initialProfile ? "PATCH" : "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ availability: form.get("availability") || null, github_url: form.get("github_url") || null }) });
    setIsSaving(false);
    if (!response.ok) { setError("Unable to save profile."); return; }
    router.refresh();
  }

  async function uploadPhoto(event: ChangeEvent<HTMLInputElement>) {
    const image = event.target.files?.[0];
    if (!image) return;
    setIsSaving(true); setError(null);
    const data = new FormData(); data.set("image", image);
    const response = await fetch("/api/profile/photo", { method: "POST", body: data });
    setIsSaving(false);
    if (!response.ok) { setError("Unable to upload photo. Use a JPEG, PNG, or WebP file up to 5 MB."); return; }
    router.refresh();
  }

  return <section className="mt-8 rounded-lg border p-6 shadow-sm"><h2 className="text-xl font-semibold">Profile and portrait</h2><p className="mt-2 text-sm text-muted-foreground">Your photo appears on the public home page. JPEG, PNG, and WebP files up to 5 MB are supported.</p><form className="mt-5 grid gap-4" onSubmit={save}><label className="grid gap-2 text-sm font-medium">Availability status<input className="rounded-md border bg-background px-3 py-2" defaultValue={initialProfile?.availability ?? ""} name="availability" placeholder="Open to opportunities" /></label><label className="grid gap-2 text-sm font-medium">GitHub URL<input className="rounded-md border bg-background px-3 py-2" defaultValue={initialProfile?.github_url ?? ""} name="github_url" placeholder="https://github.com/username" type="url" /></label><label className="grid gap-2 text-sm font-medium">Portrait<input accept="image/jpeg,image/png,image/webp" className="rounded-md border bg-background px-3 py-2" disabled={isSaving} onChange={uploadPhoto} type="file" /></label>{error ? <p className="text-sm text-red-600">{error}</p> : null}<button className="w-fit rounded-md bg-foreground px-4 py-2 font-medium text-background disabled:opacity-60" disabled={isSaving} type="submit">{isSaving ? "Saving..." : "Save profile"}</button></form></section>;
}
