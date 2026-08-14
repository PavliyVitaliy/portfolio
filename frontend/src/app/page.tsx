import { WorkExperience } from "@/api/experience/experience";
import { getExperience } from "@/api/experience/getExperience";
import Image from "next/image";

export const dynamic = "force-dynamic";

export default async function Home() {
  let experience = await getExperience()
  let workExperience = experience.work_experience
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>
        Portfolio
      </h1>
      <div>
        {experience.id}
      </div>
      <ul>
        {workExperience && workExperience.map((item: WorkExperience, index: number) => (
          <li key={index}>{item.position}</li>
      ))}
      </ul>
    </main>
  );
}
