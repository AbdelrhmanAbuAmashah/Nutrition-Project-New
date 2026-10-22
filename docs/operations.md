# Local operations and deployment boundaries

## Setup, restart and updates

Run `bash scripts/setup.sh` from the repository. It generates missing environment settings without printing secrets or replacing existing values, then builds and starts the stack. Docker is the host prerequisite; Debian/Ubuntu installation is automated when needed. That OS-installation branch still needs validation on a clean machine; the complete container setup has been exercised locally.

Use `docker compose ps --all` to inspect services. `migrate` is expected to exit successfully after applying migrations and seed data. `db` and `api` have health checks. `web` serves port 3000; the backend OpenAPI documentation serves port 8000. All published ports bind to `127.0.0.1`.

Run setup again to rebuild after changes. Avoid running two different migration revisions concurrently. Keep `.env` with the database volume: changing a generated database password in `.env` does not change an existing PostgreSQL role password. Rotate roles explicitly and update their clients together. Do not delete the volume to fix authentication on a database containing records you need.

If your user cannot access the Docker socket, setup uses `sudo docker`; the test and backup scripts use the same fallback. Start Docker first if its daemon is stopped. The scripts do not add users to the Docker group automatically.

## Backups and restore exercises

Run `bash scripts/backup.sh`. It writes a PostgreSQL custom-format dump under ignored `local-data/backups/` with restrictive permissions. Dumps include account and health records; keep them outside Git and protect copies/retention appropriately. Encryption, off-machine storage and scheduled backups belong to the deployment configuration.

Validate a dump without overwriting the live database:

```bash
docker compose exec -T db createdb -U postgres nour_restore_check
docker compose exec -T db pg_restore -U postgres --no-owner --dbname=nour_restore_check < local-data/backups/YOUR_BACKUP.dump
docker compose exec -T db psql -U postgres -d nour_restore_check -c 'SELECT count(*) FROM food_versions;'
```

Choose a new scratch database name for each exercise. Restore into an isolated environment first and verify accounts, source versions, meal snapshots and migrations before any live cutover. The repository does not provide an automatic command that destroys/replaces the live database. Removing scratch databases is an explicit operator action.

## Tests and logs

`bash scripts/test.sh` runs PostgreSQL integration tests in the isolated test database and bilingual browser flows against the running app. Browser fixtures use their own accounts and delete them on success. A failed/interrupted browser run may leave a synthetic `nour-qa-…@example.com` account; remove that test account through its authenticated delete flow if necessary. Never bulk-delete accounts in a real environment.

Errors expose a localized message, stable code and request reference. Application exception logs exclude request bodies and SQL parameters. Container/platform access logs still need access restrictions and retention policy. Do not enable HTTP/body or SQL echo logging on health data.

## Before a public pilot

- Choose the deployment account, data-processing region, allowed providers and numeric spending cap.
- Configure HTTPS ingress, exact `ALLOWED_ORIGINS`/`ALLOWED_HOSTS`, `COOKIE_SECURE=true`, `ENVIRONMENT=production`, secret storage and database network isolation. Production security validation rejects HTTP origins/insecure cookies. Remove the internal browser-test origin from deployed configuration.
- Configure the trusted proxy/client-IP boundary and tune authentication limits; arbitrary forwarded headers are not trusted by the application. Add edge rate limiting/monitoring appropriate to actual traffic.
- Configure email ownership verification and secure account recovery before a public consumer launch. Password changes, staff administration and MFA are additional account lifecycle work.
- Establish backup scheduling, protected off-machine copies, a tested restore process, monitoring/alerts, incident ownership and a retention/deletion policy.
- Review dependencies and deployment images, content, accessibility, supported populations, consent and applicable market-specific obligations with the responsible people.
- Before enabling clinical AI, implement reviewer role/assignment enforcement, source/rule applicability and freshness checks, the review UI and per-output approval gate. No current route publishes a clinical draft.

These are operational release dependencies, not completed work implied by the local foundation.
