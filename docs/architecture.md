# Application foundation

The current phase is a responsive English/Arabic nutrition diary. Clinical recommendations and photo/voice AI are not enabled. The implementation keeps their versioned records and approval boundaries ready for later increments.

## Components

- `apps/web`: Next.js 16, React, TypeScript, local fonts, accessible Radix dialogs and responsive logical CSS. Language preference is a non-sensitive cookie; health data and tokens are not stored in localStorage.
- `apps/web/app/api/v1/[...path]/route.ts`: same-origin server gateway, bounded request body, explicit forwarded headers, timeout, cookie preservation and localized unavailable responses. It selects the API upstream from runtime configuration.
- `services/api`: FastAPI, Pydantic input validation, SQLAlchemy 2, deterministic decimal arithmetic, ownership checks, explicit CORS/host policy and localized structured errors.
- PostgreSQL 17: durable records; a migration owner and separate non-superuser runtime role. Alembic is the only schema-change path. The API does not create tables on startup.
- Docker Compose: database health → one-shot migrations/seed → API health → web. Library lockfiles and hashes make package installation reproducible. Node/Python run inside containers; no host language runtimes are required by setup.

## Database boundaries

The initial migration defines 28 tables:

| Area | Tables / purpose |
| --- | --- |
| Identity | users, profiles, auth_sessions, auth_attempts, consents |
| Health profile | substances, substance_aliases, user_restrictions, health_conditions, user_conditions, medication_records |
| Food provenance | reference_resources, food_records, food_versions |
| Recipe versions | recipes, recipe_versions, recipe_ingredients |
| Diary | meals, meal_items, immutable source/nutrient snapshots |
| Later AI/media | media_assets, analysis_runs |
| Later clinical workflows | clinical_rules, clinical_drafts, clinical_approvals, reviewer_assignments, lab_observations |
| Operations | subscriptions, audit_events |

UUID primary keys, timezone-aware timestamps, numeric nutrient/quantity fields, foreign keys, checks, unique recipe/food versions and per-user idempotency are explicit. Diary indexes start with user/status and consumed time. A partial unique index permits one current food version per food. Meal items have a composite owner/meal foreign key. API ownership is enforced for every exposed private-record operation; PostgreSQL row-level-security policies are not claimed.

Future clinical schemas are preparatory, not evidence of clinical support. Their endpoints are disabled. The publication guard binds approval to content/version/profile revision; the later review service must additionally enforce reviewer role, assignment, consent and source/rule freshness before publishing anything. Reviewer credentials and applicable clinical rules still need project-specific review.

## Calculations and history

Food values are stored on their recorded 100 g basis, along with the original USDA payload. Contributions use decimal `grams × nutrient / basis`. Recipe batches sum their ingredient contributions and allocate by explicit sample cooked yield. There is no intermediate floating-point or LLM arithmetic.

Round at the meal output boundary to two decimals using half-up rounding. Daily totals sum the saved meal snapshots. Missing constituent nutrient values produce a null total, a missing-field list and a separately labeled known subtotal. Null is not zero. The UI displays unavailable values as a dash.

Creating a meal saves a draft with source/quantity/calculation snapshots. Only explicit confirmation enters diary totals. The idempotency key is unique per user; a changed payload with the same key is rejected. Confirming twice returns the same meal. Changes to food/recipe data never recalculate previously confirmed meals. Actual consumed quantities remain user-entered or weighed evidence, distinct from source nutrient composition.

Each diary date is bounded in the user's IANA timezone, converted to UTC before querying. This handles timezone midnight and 23/25-hour dates. Only dates/quantities needed for the current view are rendered; server-side records are the authority.

## Restriction foundation

Allergies, intolerances and dislikes are distinct user-confirmed records. Not-provided allergy information is distinct from no known reported allergies. Current checks match known ingredient identities, retain conflict/unknown states and never claim that a meal is safe or free of cross-contact. A conflict does not prevent accurately recording what the person actually ate.

The initial catalog records ingredient identities and explicit preparation states. The substance list is a starting set, not complete allergen coverage. Therapeutic modules, clinician-approved mappings and automated meal recommendations remain inactive. Future AI drafts must pass the same hard constraints and individual nutritionist approval before publication.

## Security choices

- Argon2id password hashes; password whitespace preserved; no seeded user/admin accounts.
- Short-lived, issuer/audience/type-checked JWTs in HttpOnly cookies. Refresh tokens are random, hash-only in PostgreSQL and rotated; server-side sessions permit immediate logout revocation.
- SameSite cookies, session-bound double-submit CSRF for authenticated mutations, explicit Origin validation, explicit CORS origins and trusted host names. Production configuration rejects insecure cookies and HTTP origins.
- Per-identity and per-network authentication limits stored in PostgreSQL. Transaction advisory locks serialize counter checks across workers. The broader network limit accommodates shared connections/proxies. Client-supplied forwarded-IP headers are not trusted; a deployment must configure its actual trusted edge and tune limits for observed usage.
- Non-root API/web processes, generated local secrets, private database credentials, loopback-only published ports and limited application database privileges.
- Per-request script nonces and CSP, clickjacking/content-type/referrer/permissions headers, no third-party trackers, no sensitive body/SQL-parameter exception logging.
- Localized errors include an opaque request reference and sanitized field paths; passwords and submitted health values are excluded from validation errors.

The phase supplies application security controls and meaningful tests. Public production operation additionally needs an accepted hosting/data region, HTTPS ingress, external secret management, backup/restore policy, monitoring, email/account recovery setup, retention review and market-specific assessment. Those deployment/clinical approvals are not implied by a successful local build.

Targets marked as professional-provided are recorded from the user's declaration; that field is not authenticated clinician approval. Reviewer assignment, professional identity verification and clinical sign-off are separate later workflows.
