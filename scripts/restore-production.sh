#!/usr/bin/env bash

# Restore a backup created by backup-production.sh. This intentionally stops
# the public application and overwrites database and uploaded-media contents.
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd -- "$SCRIPT_DIR/.." && pwd)}"
ENV_FILE="${ENV_FILE:-$PROJECT_DIR/.env.production}"
COMPOSE_FILE="${COMPOSE_FILE:-$PROJECT_DIR/docker-compose.production.yaml}"
BACKUP_PATH="${1:-}"

fail() {
    echo "Restore failed: $*" >&2
    exit 1
}

[[ -n "$BACKUP_PATH" ]] || fail "usage: $0 /path/to/backup"
[[ -d "$BACKUP_PATH" ]] || fail "backup directory not found: $BACKUP_PATH"
[[ -f "$ENV_FILE" ]] || fail "environment file not found: $ENV_FILE"
[[ -f "$COMPOSE_FILE" ]] || fail "Compose file not found: $COMPOSE_FILE"

for archive in postgres.dump mongo.archive.gz uploads.tar.gz checksums.sha256; do
    [[ -f "$BACKUP_PATH/$archive" ]] || fail "missing $archive in backup directory"
done

(
    cd "$BACKUP_PATH"
    sha256sum --check checksums.sha256
) || fail "backup checksum verification failed"

read -r -p "This stops the site and overwrites production data. Type RESTORE to continue: " confirmation
[[ "$confirmation" == "RESTORE" ]] || fail "restore cancelled"

COMPOSE=(docker compose --project-directory "$PROJECT_DIR" --env-file "$ENV_FILE" -f "$COMPOSE_FILE")

echo "Stopping application containers..."
"${COMPOSE[@]}" stop portfolio-proxy portfolio-frontend portfolio-backend

echo "Restoring PostgreSQL..."
"${COMPOSE[@]}" exec -T portfolio-postgres-db sh -ceu \
    'exec pg_restore --clean --if-exists --no-owner -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
    < "$BACKUP_PATH/postgres.dump"

echo "Restoring MongoDB..."
"${COMPOSE[@]}" exec -T portfolio-mongo-db sh -ceu \
    'exec mongorestore --drop --gzip --archive --db "$MONGO_DB_NAME" --username "$MONGO_DB_USER" --password "$MONGO_DB_PASSWORD" --authenticationDatabase "$MONGO_DB_NAME"' \
    < "$BACKUP_PATH/mongo.archive.gz"

echo "Restoring uploaded media..."
"${COMPOSE[@]}" run --rm --no-deps --entrypoint python portfolio-backend -c \
    'import pathlib, shutil, sys, tarfile; target = pathlib.Path("/code/backend/app/files").resolve(); shutil.rmtree(target, ignore_errors=True); target.mkdir(parents=True, exist_ok=True); archive = tarfile.open(fileobj=sys.stdin.buffer, mode="r:gz"); members = archive.getmembers(); root = target.parent; [(_ for _ in ()).throw(ValueError(f"unsafe archive path: {member.name}")) for member in members if not (root / member.name).resolve().is_relative_to(root)]; archive.extractall(root, members=members); archive.close()' \
    < "$BACKUP_PATH/uploads.tar.gz"

echo "Starting application containers..."
"${COMPOSE[@]}" up --detach

echo "Restore completed. Verify service health with: ${COMPOSE[*]} ps"
