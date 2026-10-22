# Nour · نور

A responsive English/Arabic nutrition diary for Jordan and Saudi Arabia. This foundation includes accounts, profile restrictions, traceable food search, meal review/confirmation, saved history, daily totals and illustrative local recipes. Arabic includes RTL layouts and Arabic numeric input.

Built with Next.js/TypeScript, FastAPI, SQLAlchemy, Alembic and PostgreSQL. Clinical AI recommendations, nutritionist review screens, personal recipe editing and photo analysis are subsequent milestones; their database boundaries are prepared, but those features are inactive.

## Run from a fresh environment

Clone [Nutrition-project](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project), open its directory in a terminal, then run:

```bash
bash scripts/setup.sh
```

Open **http://localhost:3000** and create an account. No demo account or default password is created. API documentation is at http://localhost:8000/docs.

The script installs Docker Engine/Compose automatically on Debian/Ubuntu when missing (administrator privileges and network access are required). On macOS/Windows, install Docker Desktop first and run the script in Bash/WSL. Other Linux distributions need Docker Engine and its Compose plugin. No host Node, Python, PostgreSQL or package-manager installation is needed. Initial image/package downloads can take several minutes.

Setup generates private random secrets in an ignored, permission-restricted `.env`, builds the containers, creates separate migration/runtime database roles, runs the 28-table migration, seeds 19 original USDA food records and three local example recipes, and starts the application. Running it again preserves existing secrets and database records. `.env.example` documents the settings; do not copy its placeholder credentials into a real environment.

All published ports bind to loopback. Database data live in a Docker volume. `docker compose down` stops the stack while preserving that volume. `docker compose up -d --wait` starts existing images; rerun setup after code changes to rebuild/migrate. **Do not use `down --volumes` on a database you want to keep.**

## Verify the application

With the application running:

```bash
bash scripts/test.sh
```

The backend suite runs against a separate disposable PostgreSQL test service; it refuses to use a database whose name does not end in `_test`. Browser checks create synthetic accounts in the running app, exercise English desktop and Arabic mobile flows, then delete those accounts. Playwright installs its browsers in a test container; no host browser tooling is needed. Screenshots/traces are ignored under `apps/web/test-results/` and can contain entered data.

The web production image includes TypeScript checking and an optimized build. GitHub Actions runs setup and the integration/browser checks on PRs to `main` and updates to `main` after merging, including documentation changes.

## Development workflow

Use one feature branch per milestone, verify locally before pushing, and open a PR to `main` with the change summary and test evidence. Merge through GitHub only after current checks pass, the branch is up to date and review conversations are resolved. The project uses a solo-developer policy without a required second reviewer. See the [feature-branch workflow](docs/github-workflow.md) and [agent instructions](AGENTS.md).

## Project layout

```text
apps/web/       responsive application, translations, API gateway, browser tests
services/api/   API, domain models, migration, retained USDA sources, integration tests
infra/          database roles and privileges
scripts/        setup, environment generation, verification, backup, source import
docs/           architecture, food provenance, operations, verification evidence
```

For local UI development, use Node 22+, run `npm ci` and `npm run dev` in `apps/web`, and set `API_INTERNAL_URL=http://127.0.0.1:8000`. Keep the Compose API/database running. The browser always uses the same-origin gateway; database credentials and JWT signing keys never enter client bundles. Backend package versions/hashes are in `services/api/requirements*.lock`; schema changes must be explicit Alembic migrations, not `create_all()`.

## Data and security

- Nutrients use deterministic decimal calculations from retained food versions. Meal snapshots preserve sources, portions and results; missing nutrients remain unavailable rather than becoming zero.
- Recipes are labeled illustrative examples, with visible ingredients and cooked yields. They are not measured household standards or clinical recommendations. See [food sources](docs/food-sources.md).
- Passwords use Argon2id. Short-lived JWT access and rotating refresh sessions use HttpOnly cookies, session-bound CSRF, explicit origins, server-side revocation and account ownership checks. Health data are not cached in localStorage.
- Confirmed allergies, intolerances and dislikes are distinct. Ingredient checks retain conflict/unknown states and do not establish absence of cross-contact. Logging actual intake remains possible.
- Users can export their implemented profile/diary records and delete their account. No real health records or credentials belong in this public repository.

This is a tested local foundation. Public production operation still needs HTTPS ingress, accepted hosting/data region, secret management, monitored backups/restore, email recovery, operational/privacy review and clinical sign-off for any later clinical feature. See the [architecture](docs/architecture.md) and [operations guide](docs/operations.md).

## Progress and next milestone

The [progress report and TODO checklist](nutrition-app-progress-report.md) is the completion resource. [Owner decisions](nutrition-app-project-decisions.md), [MVP plan](nutrition-app-mvp-plan.md) and [clinical review plan](nutrition-app-clinical-review-plan.md) preserve scope and unresolved decisions. Original resources remain in [the handoff](nutrition-app-codex-handoff.md) and [expanded scope](nutrition-resources-and-expanded-scope-en.md).

The [next milestone plan](docs/next-milestone.md) covers target-aware meal suggestions, an individual nutritionist approval queue and the inputs needed before clinical/provider work. Every clinical plan/warning must be approved before user publication. Personal Recipe Memory and photo assistance follow through the same source-backed calculation pipeline.
