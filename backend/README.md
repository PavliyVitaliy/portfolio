# Backend

The FastAPI service is documented in the repository [README](../README.md).

The API serves public portfolio reads under `/api/v1/*` and restricts content
management routes to an authenticated active superuser. Apply Alembic
migrations before creating the first superuser.
