import { LoginForm } from "./login-form";

export const metadata = {
  title: "Sign in | Portfolio",
};

export default async function LoginPage({
  searchParams,
}: Readonly<{ searchParams: Promise<{ reason?: string | string[] }> }>) {
  const reason = (await searchParams).reason;
  const sessionExpired = reason === "session-expired";

  return (
    <main className="mx-auto grid min-h-screen max-w-md content-center px-6 py-12">
      <section className="rounded-lg border p-6 shadow-sm">
        <h1 className="text-2xl font-semibold">Admin sign in</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Use your portfolio administrator credentials.
        </p>
        {sessionExpired ? (
          <p className="mt-4 rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-900">
            Your session has expired. Please sign in again.
          </p>
        ) : null}
        <div className="mt-6">
          <LoginForm />
        </div>
      </section>
    </main>
  );
}
