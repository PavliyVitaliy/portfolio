"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import type { Experience, WorkExperience } from "@/api/experience/experience";

type EditorProps = {
  initialExperience: Experience | null;
};

type WorkExperienceDraft = Required<
  Pick<WorkExperience, "company_name" | "company_description" | "position">
> &
  Omit<WorkExperience, "company_name" | "company_description" | "position" | "achievements"> & {
    achievements: string;
  };

const emptyWorkExperience: WorkExperienceDraft = {
  company_name: "",
  company_description: "",
  position: "",
  location: "",
  Type: "",
  start_date: "",
  end_date: "",
  achievements: "",
};

function value(value?: string) {
  return value ?? "";
}

function toLines(value: FormDataEntryValue | null) {
  return String(value ?? "")
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

function toWorkExperienceDraft(workExperience?: WorkExperience[]): WorkExperienceDraft[] {
  if (!workExperience?.length) {
    return [emptyWorkExperience];
  }

  return workExperience.map((item) => ({
    company_name: value(item.company_name),
    company_description: value(item.company_description),
    position: value(item.position),
    location: value(item.location),
    Type: value(item.Type),
    start_date: value(item.start_date),
    end_date: value(item.end_date),
    achievements: item.achievements?.join("\n") ?? "",
  }));
}

export function ExperienceEditor({ initialExperience }: EditorProps) {
  const router = useRouter();
  const [hasExperience, setHasExperience] = useState(Boolean(initialExperience));
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [workExperience, setWorkExperience] = useState(() =>
    toWorkExperienceDraft(initialExperience?.work_experience),
  );
  const experience = initialExperience;
  const contact = experience?.contact_information;

  function updateWorkExperience(
    index: number,
    field: keyof WorkExperienceDraft,
    nextValue: string,
  ) {
    setWorkExperience((items) =>
      items.map((item, itemIndex) =>
        itemIndex === index ? { ...item, [field]: nextValue } : item,
      ),
    );
  }

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSaving(true);

    const formData = new FormData(event.currentTarget);
    const payload = {
      title: formData.get("title"),
      contact_information: {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        phone_number: formData.get("phone_number") || null,
        linkedin: formData.get("linkedin") || null,
        twitter: formData.get("twitter") || null,
        address: formData.get("address") || null,
        city: formData.get("city") || null,
        state: formData.get("state") || null,
        website: formData.get("website") || null,
      },
      professional_summary: formData.get("professional_summary"),
      work_experience: workExperience.map((item) => ({
        ...item,
        location: item.location || null,
        Type: item.Type || null,
        start_date: item.start_date || null,
        end_date: item.end_date || null,
        achievements: toLines(item.achievements),
      })),
      education: toLines(formData.get("education")),
      certifications: toLines(formData.get("certifications")),
      publications: toLines(formData.get("publications")),
      skills: toLines(formData.get("skills")),
      interests: toLines(formData.get("interests")),
    };
    const response = await fetch("/api/experience", {
      method: hasExperience ? "PATCH" : "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    setIsSaving(false);
    if (response.ok) {
      setHasExperience(true);
      router.refresh();
      return;
    }

    if (response.status === 401) {
      router.replace("/login");
      return;
    }
    if (response.status === 403) {
      setError("You do not have permission to edit experience.");
      return;
    }
    if (response.status === 409) {
      setError("The record already exists. Refresh the page and try again.");
      return;
    }
    setError("Unable to save changes. Check the required fields.");
  }

  async function remove() {
    if (!window.confirm("Delete the entire experience record?")) {
      return;
    }

    setError(null);
    const response = await fetch("/api/experience", { method: "DELETE" });
    if (response.ok) {
      setHasExperience(false);
      setWorkExperience([emptyWorkExperience]);
      router.refresh();
      return;
    }
    setError("Unable to delete experience record.");
  }

  return (
    <section className="mt-8 rounded-lg border p-6 shadow-sm">
      <h2 className="text-xl font-semibold">Experience and profile</h2>
      <form className="mt-6 grid gap-5" onSubmit={save}>
        <label className="grid gap-2 text-sm font-medium" htmlFor="title">
          Professional headline
          <input className="rounded-md border bg-background px-3 py-2" defaultValue={value(experience?.title)} id="title" name="title" required />
        </label>

        <fieldset className="grid gap-4 rounded-md border p-4">
          <legend className="px-1 text-sm font-medium">Contact details</legend>
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="grid gap-2 text-sm font-medium" htmlFor="first_name">First name<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.first_name)} id="first_name" name="first_name" required /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="last_name">Last name<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.last_name)} id="last_name" name="last_name" required /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="email">Email<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.email)} id="email" name="email" required type="email" /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="phone_number">Phone<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.phone_number)} id="phone_number" name="phone_number" /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="linkedin">LinkedIn<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.linkedin)} id="linkedin" name="linkedin" /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="website">Website<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.website)} id="website" name="website" /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="twitter">Twitter / X<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.twitter)} id="twitter" name="twitter" /></label>
            <label className="grid gap-2 text-sm font-medium" htmlFor="city">City<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.city)} id="city" name="city" /></label>
          </div>
          <label className="grid gap-2 text-sm font-medium" htmlFor="address">Address<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.address)} id="address" name="address" /></label>
          <label className="grid gap-2 text-sm font-medium" htmlFor="state">State / region<input className="rounded-md border bg-background px-3 py-2" defaultValue={value(contact?.state)} id="state" name="state" /></label>
        </fieldset>

        <label className="grid gap-2 text-sm font-medium" htmlFor="professional_summary">
          About
          <textarea className="min-h-28 rounded-md border bg-background px-3 py-2" defaultValue={value(experience?.professional_summary)} id="professional_summary" name="professional_summary" required />
        </label>

        <fieldset className="grid gap-5 rounded-md border p-4">
          <legend className="px-1 text-sm font-medium">Work experience</legend>
          {workExperience.map((item, index) => (
            <div className="grid gap-4 rounded-md border p-4" key={`${item.company_name}-${index}`}>
              <div className="flex items-center justify-between gap-3">
                <h3 className="font-medium">Position {index + 1}</h3>
                {workExperience.length > 1 ? <button className="text-sm text-red-700" onClick={() => setWorkExperience((items) => items.filter((_, itemIndex) => itemIndex !== index))} type="button">Remove</button> : null}
              </div>
              <label className="grid gap-2 text-sm font-medium">Company<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "company_name", event.target.value)} required value={item.company_name} /></label>
              <label className="grid gap-2 text-sm font-medium">Role<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "position", event.target.value)} required value={item.position} /></label>
              <label className="grid gap-2 text-sm font-medium">Company description<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "company_description", event.target.value)} required value={item.company_description} /></label>
              <div className="grid gap-4 sm:grid-cols-2">
                <label className="grid gap-2 text-sm font-medium">Location<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "location", event.target.value)} value={item.location} /></label>
                <label className="grid gap-2 text-sm font-medium">Employment type<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "Type", event.target.value)} value={item.Type} /></label>
                <label className="grid gap-2 text-sm font-medium">Start date<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "start_date", event.target.value)} value={item.start_date} /></label>
                <label className="grid gap-2 text-sm font-medium">End date<input className="rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "end_date", event.target.value)} value={item.end_date} /></label>
              </div>
              <label className="grid gap-2 text-sm font-medium">Achievements (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" onChange={(event) => updateWorkExperience(index, "achievements", event.target.value)} value={item.achievements} /></label>
            </div>
          ))}
          <button className="w-fit rounded-md border px-3 py-2 text-sm" onClick={() => setWorkExperience((items) => [...items, { ...emptyWorkExperience }])} type="button">Add position</button>
        </fieldset>

        <fieldset className="grid gap-4 rounded-md border p-4">
          <legend className="px-1 text-sm font-medium">Additional information</legend>
          <label className="grid gap-2 text-sm font-medium">Skills (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={experience?.skills?.join("\n")} name="skills" /></label>
          <label className="grid gap-2 text-sm font-medium">Education (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={experience?.education?.join("\n")} name="education" /></label>
          <label className="grid gap-2 text-sm font-medium">Certifications (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={experience?.certifications?.join("\n")} name="certifications" /></label>
          <label className="grid gap-2 text-sm font-medium">Publications (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={experience?.publications?.join("\n")} name="publications" /></label>
          <label className="grid gap-2 text-sm font-medium">Interests (one per line)<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={experience?.interests?.join("\n")} name="interests" /></label>
        </fieldset>

        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        <div className="flex flex-wrap gap-3">
          <button className="rounded-md bg-foreground px-4 py-2 font-medium text-background disabled:opacity-60" disabled={isSaving} type="submit">{isSaving ? "Saving..." : hasExperience ? "Save" : "Create profile"}</button>
          {hasExperience ? <button className="rounded-md border border-red-300 px-4 py-2 text-red-700" onClick={remove} type="button">Delete</button> : null}
        </div>
      </form>
    </section>
  );
}
