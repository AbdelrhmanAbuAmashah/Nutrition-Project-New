#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
umask 077
mkdir -p local-data/backups
BACKUP_PATH="local-data/backups/nour-$(date -u +%Y%m%dT%H%M%SZ).dump"
DOCKER=(docker)
if ! docker info >/dev/null 2>&1; then DOCKER=(sudo docker); fi
"${DOCKER[@]}" compose exec -T db pg_dump -U postgres -d nour --format=custom > "$BACKUP_PATH"
echo "Database backup saved to $BACKUP_PATH (ignored by Git)."
