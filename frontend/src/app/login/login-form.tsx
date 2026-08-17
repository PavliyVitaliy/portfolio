"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

export function LoginForm() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    const formData = new FormData(event.currentTarget);
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: formData.get("email"),
        password: formData.get("password"),
      }),
    });

    setIsSubmitting(false);
    if (!response.ok) {
      setError("Unable to sign in. Check your email and password.");
      return;
    }

    router.replace("/admin");
    router.refresh();
  }

  return (
    <form className="grid gap-4" onSubmit={onSubmit}>
      <label className="grid gap-2 text-sm font-medium" htmlFor="email">
        Email
        <input
          autoComplete="email"
          className="rounded-md border bg-background px-3 py-2"
          id="email"
          name="email"
          required
          type="email"
        />
      </label>
      <label className="grid gap-2 text-sm font-medium" htmlFor="password">
        Password
        <input
          autoComplete="current-password"
          className="rounded-md border bg-background px-3 py-2"
          id="password"
          name="password"
          required
          type="password"
        />
      </label>
      {error ? <p className="text-sm text-red-600">{error}</p> : null}
      <button
        className="rounded-md bg-foreground px-3 py-2 font-medium text-background disabled:opacity-60"
        disabled={isSubmitting}
        type="submit"
      >
        {isSubmitting ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
