# Foundation verification evidence

Recorded 22 October 2026. Scope: the approved bilingual manual logging foundation, not the complete clinical/AI MVP.

## Completed checks

| Check | Command / evidence | Result |
| --- | --- | --- |
| Automatic local setup | `bash scripts/setup.sh` | Database, migration/seed, API and web start successfully; repeated setup preserves secrets/data. |
| Documented complete verification | `bash scripts/test.sh` | Passes: migration drift check, Ruff, 36 PostgreSQL API tests and all four browser journeys. |
| Production web compilation | `docker compose build web` (also run by setup/browser verification) | Prettier, TypeScript and optimized Next.js build pass. |
| PostgreSQL migration | `alembic upgrade head` / `alembic check` inside the API container | Initial 28-table migration applies; no new upgrade operations detected. |
| Backend integration | `docker compose --profile test run --build --rm api-test` | 36 tests pass against isolated PostgreSQL. |
| Bilingual browser journeys | `docker compose --profile test run --build --rm e2e npx playwright test --retries=0` | Four pass: desktop English, desktop Arabic, mobile English, mobile Arabic. |
| Visual review | Generated desktop/mobile screenshots inspected locally | RTL layout, populated actual diary, language switching and responsive layout verified; no horizontal document overflow in browser checks. |
| Static Python checks | `services/api/.venv/bin/ruff check services/api scripts/import_usda_seed.py scripts/configure_env.py` | Pass. Container check uses `--no-cache` for the non-root filesystem. |
| Backup/restore | `bash scripts/backup.sh`, restore with `pg_restore` into a newly created scratch database | Restored 19 food versions, three recipe versions, 28 domain tables; scratch database removed after verification. Live database preserved. |
| Runtime privileges | PostgreSQL role and schema-privilege query | Runtime role is not superuser, cannot create databases/roles, and cannot create schema objects. |
| Published application CI | [Active-repository run 39726433154](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New/actions/runs/39726433154), revision `68ac7d0850521f63fc38273a8c36bcaccfbeebd7` | Completed/success; read back again during repository cleanup. Includes the foundation and owner-only repository documentation. Subsequent PR revisions require their own fresh checks. |

The backend suite covers authentication/Argon2 hashes, localized validation, JWT tampering/audience, refresh rotation/replay, logout/session expiry, CORS/origin/CSRF, rate limiting, password whitespace, production security configuration, source records, deterministic portions, missing nutrients, draft/confirmation, sequential and simultaneous duplicate saves, immutable history, ownership, profile revisions/restrictions, timezone midnight/DST, recipe yield, export/deletion and inactive clinical publication boundaries.

Each browser journey creates a synthetic account, completes onboarding, searches the verified catalog, logs 150 g of cooked rice (195 kcal), confirms it, reloads and inspects the preserved source link, checks cookie/CSRF behavior, views a sample local recipe, and deletes the account. Arabic journeys enter Arabic digits. Failed-test cleanup uses only the synthetic account created by that test.

Initial checks exposed and corrected a test selector mismatch, non-root test import/cache configuration, and a browser compatibility issue with `crypto.randomUUID` on HTTP container hostnames. Final client retry keys use cryptographically random bytes; no weak random fallback was added. Captured screenshots/traces are local ignored artifacts, not repository data.

## Limits and outstanding verification

- The Docker-installation branch has not been executed on a completely clean OS. Container/package installation, migration, seed and startup have been exercised in the supplied environment.
- Browser coverage uses Chromium at desktop/mobile viewports. It does not establish full Safari/Firefox, assistive-technology, load-test or complete accessibility compliance.
- One upstream Starlette TestClient deprecation warning remains about its current HTTPX adapter; it does not fail tests.
- `npm audit --omit=dev --audit-level=high --prefix apps/web` could not complete: the npm security audit endpoint returned HTTP 503. No clean dependency vulnerability scan is claimed. Locked packages/builds are not a substitute for an advisory scan.
- Clinical AI, therapeutic rules, reviewer workflows, Personal Recipe Memory editing, photo/voice, paid services and public hosting are inactive/unimplemented. Preparatory schema/guard tests do not establish clinical readiness.
- The active-repository CI run is linked above. Legacy revision `ae28042266bf7966c428c0b26a16cefb144f80fd` and run `39713405773` passed when originally observed, but their hosted pages were removed with `Nutrition-project` at the owner's request. Local Git metadata preserves commits, not GitHub-hosted PR/check logs. Every PR, including documentation-only changes, requires CI; see [workflow](github-workflow.md).

The [operations guide](operations.md) records remaining deployment and public-pilot dependencies.

## Feature-branch workflow adoption

On `feature/github-feature-branch-workflow`, the complete local `bash scripts/setup.sh` → `bash scripts/test.sh` sequence passed again before publication: production build, migration drift/lint, 36 API tests and four EN/AR desktop/mobile browser journeys. YAML/JSON configuration checks and diff checks passed. No application behavior, schema or package version changed in this maintenance milestone.

The GitHub protection API was read before and after the authorized change. Read-back confirms PR enforcement, administrator enforcement, strict GitHub Actions `verify`, resolved conversations, linear history and blocked force-push/deletion. A duplicate legacy status-check field was rejected by the API before application; the corrected payload uses the explicit provider-bound `checks` field. The [workflow guide](github-workflow.md) and progress-report W1–W4 track the new delivery policy and its PR evidence.

The original delivery used legacy `Nutrition-project` PR #1 from `feature/github-feature-branch-workflow`; its hosted page was removed during the authorized cleanup. The active repository's [PR #1](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New/pull/1) delivered the owner-only repository documentation through the protected path, with successful PR and post-merge CI. The [cleanup record](repository-cleanup.md) records the later deletions and preserved local history. Documentation-only bookkeeping still triggers fresh PR CI and must pass before merging.
