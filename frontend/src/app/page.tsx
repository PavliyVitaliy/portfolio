import Link from "next/link";

import type { WorkExperience } from "@/api/experience/experience";
import { getExperience } from "@/api/experience/getExperience";

export const dynamic = "force-dynamic";

function Section({
  children,
  id,
  title,
}: Readonly<{ children: React.ReactNode; id: string; title: string }>) {
  return (
    <section className="scroll-mt-8 border-t border-slate-200 py-12" id={id}>
      <h2 className="text-2xl font-semibold tracking-tight text-slate-900">{title}</h2>
      <div className="mt-6">{children}</div>
    </section>
  );
}

function DetailList({ items }: Readonly<{ items?: string[] }>) {
  if (!items?.length) {
    return null;
  }

  return (
    <ul className="grid gap-2 text-slate-600">
      {items.map((item, index) => (
        <li className="flex gap-3" key={`${item}-${index}`}>
          <span aria-hidden className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-sky-600" />
          {item}
        </li>
      ))}
    </ul>
  );
}

function WorkCard({ item }: Readonly<{ item: WorkExperience }>) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">{item.position}</h3>
          <p className="mt-1 font-medium text-sky-700">{item.company_name}</p>
        </div>
        <div className="text-sm text-slate-500 sm:text-right">
          {item.start_date || item.end_date ? (
            <p>{[item.start_date, item.end_date].filter(Boolean).join(" — ")}</p>
          ) : null}
          {item.location ? <p>{item.location}</p> : null}
          {item.Type ? <p>{item.Type}</p> : null}
        </div>
      </div>
      {item.company_description ? (
        <p className="mt-4 leading-7 text-slate-600">{item.company_description}</p>
      ) : null}
      {item.achievements?.length ? (
        <div className="mt-4">
          <p className="text-sm font-medium text-slate-900">Достижения</p>
          <div className="mt-2">
            <DetailList items={item.achievements} />
          </div>
        </div>
      ) : null}
    </article>
  );
}

export default async function Home() {
  const experience = await getExperience();
  const contact = experience.contact_information;
  const fullName = [contact?.first_name, contact?.last_name].filter(Boolean).join(" ");
  const contactLinks = [
    contact?.email ? { href: `mailto:${contact.email}`, label: contact.email } : null,
    contact?.website ? { href: contact.website, label: "Сайт" } : null,
    contact?.linkedin ? { href: contact.linkedin, label: "LinkedIn" } : null,
  ].filter(Boolean) as { href: string; label: string }[];

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-6 py-6 sm:px-10">
        <header className="flex items-center justify-between gap-6 border-b border-slate-200 pb-5">
          <Link className="text-base font-semibold tracking-tight" href="#top">
            {fullName || "Portfolio"}
          </Link>
          <nav aria-label="Основная навигация" className="hidden items-center gap-5 text-sm text-slate-600 sm:flex">
            <a className="transition hover:text-slate-950" href="#experience">Опыт</a>
            {experience.skills?.length ? <a className="transition hover:text-slate-950" href="#skills">Навыки</a> : null}
            {contactLinks.length ? <a className="transition hover:text-slate-950" href="#contact">Контакты</a> : null}
            <Link className="transition hover:text-slate-950" href="/admin">Админ</Link>
          </nav>
        </header>

        <section className="grid gap-10 py-16 sm:py-24" id="top">
          <div className="max-w-3xl">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-sky-700">Портфолио</p>
            <h1 className="mt-5 text-4xl font-semibold tracking-tight text-slate-950 sm:text-6xl">
              {fullName || experience.title}
            </h1>
            {experience.title ? <p className="mt-5 text-xl text-slate-600 sm:text-2xl">{experience.title}</p> : null}
            {experience.professional_summary ? (
              <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-600">{experience.professional_summary}</p>
            ) : null}
          </div>
          {contactLinks.length || contact?.phone_number ? (
            <div className="flex flex-wrap gap-3 text-sm">
              {contactLinks.map((link) => (
                <a className="rounded-full border border-slate-300 bg-white px-4 py-2 transition hover:border-sky-600 hover:text-sky-700" href={link.href} key={`${link.label}-${link.href}`} rel="noreferrer" target={link.href.startsWith("mailto:") ? undefined : "_blank"}>
                  {link.label}
                </a>
              ))}
              {contact?.phone_number ? <a className="rounded-full border border-slate-300 bg-white px-4 py-2 transition hover:border-sky-600 hover:text-sky-700" href={`tel:${contact.phone_number}`}>{contact.phone_number}</a> : null}
            </div>
          ) : null}
        </section>

        {experience.work_experience?.length ? (
          <Section id="experience" title="Опыт работы">
            <div className="grid gap-5">
              {experience.work_experience.map((item, index) => <WorkCard item={item} key={`${item.company_name}-${index}`} />)}
            </div>
          </Section>
        ) : null}

        {experience.skills?.length ? (
          <Section id="skills" title="Навыки">
            <div className="flex flex-wrap gap-2">
              {experience.skills.map((skill, index) => <span className="rounded-full bg-sky-100 px-3 py-1.5 text-sm font-medium text-sky-900" key={`${skill}-${index}`}>{skill}</span>)}
            </div>
          </Section>
        ) : null}

        {experience.education?.length || experience.certifications?.length || experience.publications?.length ? (
          <section className="grid gap-10 border-t border-slate-200 py-12 md:grid-cols-3">
            {experience.education?.length ? <div><h2 className="text-xl font-semibold">Образование</h2><div className="mt-5"><DetailList items={experience.education} /></div></div> : null}
            {experience.certifications?.length ? <div><h2 className="text-xl font-semibold">Сертификаты</h2><div className="mt-5"><DetailList items={experience.certifications} /></div></div> : null}
            {experience.publications?.length ? <div><h2 className="text-xl font-semibold">Публикации</h2><div className="mt-5"><DetailList items={experience.publications} /></div></div> : null}
          </section>
        ) : null}

        {contactLinks.length || contact?.phone_number || contact?.city ? (
          <Section id="contact" title="Контакты">
            <div className="grid gap-2 text-slate-600">
              {contactLinks.map((link) => <a className="w-fit transition hover:text-sky-700" href={link.href} key={`${link.label}-${link.href}`} rel="noreferrer" target={link.href.startsWith("mailto:") ? undefined : "_blank"}>{link.label}</a>)}
              {contact?.phone_number ? <a className="w-fit transition hover:text-sky-700" href={`tel:${contact.phone_number}`}>{contact.phone_number}</a> : null}
              {[contact?.city, contact?.state, contact?.address].filter(Boolean).join(", ")}
            </div>
          </Section>
        ) : null}

        <footer className="border-t border-slate-200 py-8 text-sm text-slate-500">© {new Date().getFullYear()} {fullName || "Portfolio"}</footer>
      </div>
    </main>
  );
}
