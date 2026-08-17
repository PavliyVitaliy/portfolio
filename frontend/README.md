# Frontend

The Next.js frontend is documented in the repository [README](../README.md).

For local development on PowerShell:

```powershell
Copy-Item .env.example .env
npm ci
npm run dev
```

On macOS/Linux:

```bash
cp .env.example .env
npm ci
npm run dev
```

The app is available at `http://localhost:3000`. `API_BASE_URL` is server-only;
do not add a `NEXT_PUBLIC_` prefix because the access token must remain inside
the Next.js BFF.
