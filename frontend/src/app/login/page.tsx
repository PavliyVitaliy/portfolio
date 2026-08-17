import { LoginForm } from "./login-form";

export const metadata = {
  title: "Sign in | Portfolio",
};

export default function LoginPage() {
  return (
    <main className="mx-auto grid min-h-screen max-w-md content-center px-6 py-12">
      <section className="rounded-lg border p-6 shadow-sm">
        <h1 className="text-2xl font-semibold">Admin sign in</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Use your portfolio administrator credentials.
        </p>
        <div className="mt-6">
          <LoginForm />
        </div>
      </section>
    </main>
  );
}
