# Portfolio

A full-stack personal portfolio with a public experience/projects page and a
private admin area for managing content and a profile portrait.

## Stack

- Frontend: Next.js 16, React 19, Tailwind CSS 4
- Backend: FastAPI, FastAPI Users, SQLAlchemy and Alembic
- Data: PostgreSQL for users/authentication; MongoDB for public portfolio data
- Infrastructure: Docker Compose, Nginx for local development, and Caddy for
  production HTTPS

## Prerequisites

- Docker Desktop with Docker Compose v2
- Node.js 20+ and npm for the local frontend development server

Python and Poetry are only required when running backend commands outside
Docker.

## Local development

The local stack runs PostgreSQL, MongoDB, FastAPI, and Nginx in Docker. Next.js
runs separately in development mode so that it supports fast refresh.

### 1. Create local environment files

PowerShell:

```powershell
Copy-Item backend/app/.env.example backend/app/.env
Copy-Item frontend/.env.example frontend/.env
```

macOS/Linux:

```bash
cp backend/app/.env.example backend/app/.env
cp frontend/.env.example frontend/.env
```

The example credentials are suitable only for local development. Do not use
them in production.

### 2. Start backend services

```bash
docker compose up --detach --build
```

Useful endpoints:

- Public API: `http://localhost:8000/api/v1/experience/free`
- Backend docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/ping`
- Nginx proxy health: `http://localhost/ping`

### 3. Apply migrations and create the first administrator

Run these once after the databases start:

```bash
docker compose exec portfolio-backend alembic upgrade head
docker compose exec portfolio-backend python actions/create_superuser.py
```

The administrator email and password come from `backend/app/.env`. Creating
the same administrator twice returns an error; this is expected.

### 4. Start the frontend

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:3000`. The private content editor is at
`http://localhost:3000/admin`.

Sign in with the administrator credentials from `backend/app/.env`, then create
the first experience record. The public home page needs this record before it
can render portfolio content.

### Stop local services

```bash
docker compose stop
```

This keeps the local database volumes. Use `docker compose down` to remove
containers and networks while retaining named volumes. Do not add `--volumes`
unless intentionally deleting local data.

## Tests

Backend integration tests use an isolated MongoDB volume and do not touch the
development database:

```bash
docker compose -f docker-compose.test.yaml up --detach portfolio-mongo-db-test
docker compose -f docker-compose.test.yaml run --rm --no-deps --build portfolio-backend-test pytest
docker compose -f docker-compose.test.yaml stop portfolio-mongo-db-test
```

Build the frontend as it will run in production:

```bash
cd frontend
npm run build
```

## Production container stack

`docker-compose.production.yaml` builds the standalone Next.js image, FastAPI,
PostgreSQL, MongoDB, and Caddy. Caddy is the only public service: it exposes
ports 80/443, obtains and renews Let's Encrypt certificates for
`vitaliipavlii.com` and `www.vitaliipavlii.com`, and redirects `www` to the
canonical domain. Databases, backend, and frontend remain on the internal
Docker network.

```bash
cp .env.production.example .env.production
cp backend/app/.env.production.example backend/app/.env.production
# Set a real email address in .env.production. Replace every change-me value
# with a unique secret in backend/app/.env.production before continuing.
docker compose --env-file .env.production -f docker-compose.production.yaml up --detach --build
docker compose --env-file .env.production -f docker-compose.production.yaml exec portfolio-backend alembic upgrade head
docker compose --env-file .env.production -f docker-compose.production.yaml exec portfolio-backend python actions/create_superuser.py
```

PowerShell:

```powershell
Copy-Item .env.production.example .env.production
Copy-Item backend/app/.env.production.example backend/app/.env.production
# Set a real email address in .env.production. Replace every change-me value
# with a unique secret in backend/app/.env.production before continuing.
docker compose --env-file .env.production -f docker-compose.production.yaml up --detach --build
docker compose --env-file .env.production -f docker-compose.production.yaml exec portfolio-backend alembic upgrade head
docker compose --env-file .env.production -f docker-compose.production.yaml exec portfolio-backend python actions/create_superuser.py
```

The production stack persists PostgreSQL, MongoDB, and uploaded portrait files
in named Docker volumes. Back up all three before upgrades or server changes.

Caddy automatically requests certificates when DNS for both domains resolves to
the VPS and ports 80/443 are reachable. Do not enable HSTS until the first
HTTPS deployment has been verified.

## Configuration and security

- Never commit `backend/app/.env` or `backend/app/.env.production`.
- Generate production secrets with, for example:

  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

- User-uploaded portraits are stored in a persistent volume and intentionally
  excluded from Git.
- The frontend stores the backend access token only in an HttpOnly cookie; do
  not replace this with local storage.

## Optional Make targets

On systems with GNU Make, `make up`, `make stop`, `make test`,
`make frontend-build`, and `make production-up` provide short equivalents of
the documented Docker/npm commands. The README commands remain the canonical
cross-platform instructions.

## Project layout

```text
backend/       FastAPI app, migrations, tests, and environment templates
frontend/      Next.js app and admin UI
nginx/         Development and production reverse-proxy configs
docker-compose.yaml             Local development backend stack
docker-compose.test.yaml        Isolated backend test stack
docker-compose.production.yaml  Production container stack
```
