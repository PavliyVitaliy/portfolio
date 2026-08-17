export type Project = {
  id: string;
  user_id: string;
  title: string;
  description: string;
  url: string;
  repository_url?: string | null;
  stack?: string[] | null;
  featured: boolean;
  sort_order: number;
};
