"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";

import type { Project } from "@/api/projects/project";

function lines(value: FormDataEntryValue | null) { return String(value ?? "").split("\n").map((item) => item.trim()).filter(Boolean); }

export function ProjectsEditor({ initialProjects }: Readonly<{ initialProjects: Project[] }>) {
  const router = useRouter();
  const [projects, setProjects] = useState(initialProjects);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(null); setIsSaving(true);
    const formElement = event.currentTarget;
    const form = new FormData(formElement); const id = String(form.get("id") || "");
    const payload = { title: form.get("title"), description: form.get("description"), url: form.get("url"), repository_url: form.get("repository_url") || null, stack: lines(form.get("stack")), featured: form.get("featured") === "on", sort_order: Number(form.get("sort_order") || 0) };
    const response = await fetch(id ? `/api/projects/${id}` : "/api/projects", { method: id ? "PATCH" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
    setIsSaving(false); if (!response.ok) { setError("Не удалось сохранить проект. Проверьте обязательные поля и ссылки."); return; }
    const project = await response.json() as Project; setProjects((items) => id ? items.map((item) => item.id === id ? project : item) : [...items, project]); setEditingProject(null); formElement.reset(); router.refresh();
  }

  async function remove(id: string) {
    if (!window.confirm("Удалить этот проект?")) return;
    const response = await fetch(`/api/projects/${id}`, { method: "DELETE" }); if (!response.ok) { setError("Не удалось удалить проект."); return; }
    setProjects((items) => items.filter((item) => item.id !== id)); router.refresh();
  }

  return <section className="mt-8 rounded-lg border p-6 shadow-sm"><h2 className="text-xl font-semibold">Проекты</h2><p className="mt-2 text-sm text-muted-foreground">Сначала добавь портфолио и ссылку на GitHub. Карточки выводятся по возрастанию порядка.</p><div className="mt-5 grid gap-3">{projects.map((project) => <div className="flex items-center justify-between gap-4 rounded-md border p-4" key={project.id}><div><p className="font-medium">{project.title}</p><p className="text-sm text-muted-foreground">Порядок: {project.sort_order}</p></div><div className="flex gap-3"><button className="text-sm text-sky-700" onClick={() => setEditingProject(project)} type="button">Изменить</button><button className="text-sm text-red-700" onClick={() => remove(project.id)} type="button">Удалить</button></div></div>)}</div><form className="mt-6 grid gap-4 border-t pt-6" key={editingProject?.id ?? "new"} onSubmit={save}><input name="id" type="hidden" value={editingProject?.id ?? ""} readOnly /><label className="grid gap-2 text-sm font-medium">Название<input className="rounded-md border bg-background px-3 py-2" defaultValue={editingProject?.title ?? ""} name="title" required /></label><label className="grid gap-2 text-sm font-medium">Описание<textarea className="min-h-24 rounded-md border bg-background px-3 py-2" defaultValue={editingProject?.description ?? ""} name="description" required /></label><div className="grid gap-4 sm:grid-cols-2"><label className="grid gap-2 text-sm font-medium">Ссылка на проект<input className="rounded-md border bg-background px-3 py-2" defaultValue={editingProject?.url ?? ""} name="url" placeholder="https://github.com/..." required type="url" /></label><label className="grid gap-2 text-sm font-medium">Ссылка на исходники<input className="rounded-md border bg-background px-3 py-2" defaultValue={editingProject?.repository_url ?? ""} name="repository_url" placeholder="https://github.com/..." type="url" /></label></div><label className="grid gap-2 text-sm font-medium">Стек (по одному на строку)<textarea className="min-h-20 rounded-md border bg-background px-3 py-2" defaultValue={editingProject?.stack?.join("\n") ?? ""} name="stack" /></label><div className="flex flex-wrap gap-4"><label className="flex items-center gap-2 text-sm font-medium"><input defaultChecked={editingProject?.featured ?? false} name="featured" type="checkbox" /> Избранный проект</label><label className="flex items-center gap-2 text-sm font-medium">Порядок<input className="w-20 rounded-md border bg-background px-2 py-1" defaultValue={editingProject?.sort_order ?? 0} min="0" name="sort_order" type="number" /></label></div>{error ? <p className="text-sm text-red-600">{error}</p> : null}<div className="flex gap-3"><button className="w-fit rounded-md bg-foreground px-4 py-2 font-medium text-background disabled:opacity-60" disabled={isSaving} type="submit">{isSaving ? "Сохраняем..." : editingProject ? "Сохранить проект" : "Добавить проект"}</button>{editingProject ? <button className="rounded-md border px-4 py-2" onClick={() => setEditingProject(null)} type="button">Отмена</button> : null}</div></form></section>;
}
