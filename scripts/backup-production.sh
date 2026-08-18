#!/usr/bin/env bash

# Create a consistent, restorable backup of the production application data.
# Run this script on the VPS from any directory; it resolves the project root
# from its own location and never stores secrets in the backup archive.
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${PROJECT_DIR:-$(cd -- "$SCRIPT_DIR/.." && pwd)}"
ENV_FILE="${ENV_FILE:-$PROJECT_DIR/.env.production}"
COMPOSE_FILE="${COMPOSE_FILE:-$PROJECT_DIR/docker-compose.production.yaml}"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_DIR/backups}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
BACKUP_PATH="$BACKUP_DIR/$TIMESTAMP"
STAGING_PATH="$BACKUP_DIR/.${TIMESTAMP}.partial.$$"

fail() {
    echo "Backup failed: $*" >&2
    exit 1
}

[[ -f "$ENV_FILE" ]] || fail "environment file not found: $ENV_FILE"
[[ -f "$COMPOSE_FILE" ]] || fail "Compose file not found: $COMPOSE_FILE"
[[ "$RETENTION_DAYS" =~ ^[0-9]+$ ]] || fail "RETENTION_DAYS must be a non-negative integer"

case "$BACKUP_DIR" in
    /|"$PROJECT_DIR") fail "BACKUP_DIR must not be / or the project directory" ;;
esac

[[ ! -e "$BACKUP_PATH" ]] || fail "backup path already exists: $BACKUP_PATH"
mkdir -p "$STAGING_PATH"
trap 'rm -rf -- "$STAGING_PATH"' ERR
COMPOSE=(docker compose --project-directory "$PROJECT_DIR" --env-file "$ENV_FILE" -f "$COMPOSE_FILE")

echo "Creating PostgreSQL backup..."
"${COMPOSE[@]}" exec -T portfolio-postgres-db sh -ceu \
    'exec pg_dump -Fc -U "$POSTGRES_USER" -d "$POSTGRES_DB"' \
    > "$STAGING_PATH/postgres.dump"

echo "Creating MongoDB backup..."
"${COMPOSE[@]}" exec -T portfolio-mongo-db sh -ceu \
    'exec mongodump --gzip --archive --db "$MONGO_DB_NAME" --username "$MONGO_DB_USER" --password "$MONGO_DB_PASSWORD" --authenticationDatabase "$MONGO_DB_NAME"' \
    > "$STAGING_PATH/mongo.archive.gz"

echo "Creating uploaded-media backup..."
"${COMPOSE[@]}" exec -T portfolio-backend python -c \
    'import sys, tarfile; archive = tarfile.open(fileobj=sys.stdout.buffer, mode="w:gz"); archive.add("/code/backend/app/files", arcname="files"); archive.close()' \
    > "$STAGING_PATH/uploads.tar.gz"

echo "Verifying backup archives..."
docker run --rm -i postgres:14 pg_restore --list < "$STAGING_PATH/postgres.dump" > /dev/null
gzip -t "$STAGING_PATH/mongo.archive.gz"
tar -tzf "$STAGING_PATH/uploads.tar.gz" > /dev/null

(
    cd "$STAGING_PATH"
    sha256sum postgres.dump mongo.archive.gz uploads.tar.gz > checksums.sha256
)

cat > "$STAGING_PATH/metadata.txt" <<EOF
created_at_utc=$TIMESTAMP
project_dir=$PROJECT_DIR
postgres_service=portfolio-postgres-db
mongo_service=portfolio-mongo-db
uploads_service=portfolio-backend
EOF

mv "$STAGING_PATH" "$BACKUP_PATH"
trap - ERR

find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d -name '????-??-??T??-??-??Z' -mtime "+$RETENTION_DAYS" -print -exec rm -rf {} +

echo "Backup completed: $BACKUP_PATH"
echo "Copy this directory to storage outside the VPS before relying on it for disaster recovery."
