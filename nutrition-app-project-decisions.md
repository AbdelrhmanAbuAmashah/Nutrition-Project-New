# Nutrition app: owner decisions and next delivery cycle

Updated 22 October 2026 from the owner's strategic/workflow message, repository/nutrition-expert/individual-approval answers, and explicit approval to implement this phase. Sources are SRC-06, SRC-11 and SRC-17 in the [progress report](nutrition-app-progress-report.md). Explicit owner decisions below supersede conflicting earlier proposals. The bilingual logging foundation is implemented, verified and published; N1–N7 are complete.

## Confirmed direction

| Topic | Owner decision | Engineering consequence |
| --- | --- | --- |
| Markets | Jordan and Saudi Arabia | Record country and user timezone; evaluate food/recipe coverage for both markets. Do not assume a generic dish name identifies its ingredients or portion. |
| Platform | Responsive web first; mobile later | Build one web frontend and a separate documented API. A future mobile client can use the API/database; its interface still requires implementation. |
| Languages | English and Arabic, including RTL | Both languages are first-release requirements. Design translation keys, direction, mixed-script content, forms, dates, units and errors from the beginning. |
| Personalization | Adapt to onboarding, profile, history and health constraints | Store confirmed facts separately from extracted drafts. Recompute recommendation eligibility when relevant confirmed information changes. |
| Allergy example | Automatically exclude reported allergen ingredients from daily meal/recipe recommendations | Implement server-side hard constraints, a reviewed ingredient/allergen mapping, and validation before recommendations reach the user. |
| Nutrition integrity | Manual entries use verified, traceable food sources | Production food records need source identity, version/retrieval snapshot, preparation state, units/basis and matching status. AI-generated nutrient numbers cannot become authoritative food records. |
| Capacity | Solo developer, beginning in Web/Mobile | Deliver small complete increments with clear setup/run instructions; keep a modular application and minimize services. |
| Budget | Low to medium | Prefer local development and measured provider usage. Numeric spending caps and services remain undecided; no purchases made. |
| Timeline | Continuous, measurable, iterative progress | No fixed date committed. Track acceptance evidence, defects, costs and completion per increment. |
| Version control | GitHub from day one; dedicated feature branches, local verification, PRs and checked merges into [Nutrition-project](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project) | One branch per milestone, no direct working pushes to main, exact local test evidence in PRs, required current CI/up-to-date checks and resolved conversations before normal protected merging. Current foundation history remains the baseline. See [workflow](docs/github-workflow.md). |
| Clinical reviewer and AI role | Certified nutritionist/dietitian on board; AI prepares evidence-grounded drafts first | Reviewer verifies/edits/approves rules, plans and warnings. Initial module-definition areas: food allergies, diabetes and hypertension; exact populations/subtypes remain open. |
| Clinical publication | Approve every clinical plan/warning before users see it | Implement a nutritionist queue and server-side version-specific publication gate; approved rules alone do not publish a personalized clinical draft. |
| Agent role | Technical assistant and co-pilot across architecture, development, debugging and planning | Maintain decisions/requirements/progress, explain meaningful tradeoffs and complete authorized increments with verification. |

Clinical adaptation, initial interest in diabetes/hypertension/allergies and nutritionist review are confirmed. Exact condition populations, permitted rules, target methods, named reviewer access and review availability remain to be defined. The [clinical review plan](nutrition-app-clinical-review-plan.md) records the agreed AI-first, individual-approval workflow and checked starting references. These remaining details do not prevent the manual logging foundation.

## Scope change from the previous MVP proposal

**Daily meal/recipe suggestions constrained by the user's profile and daily targets are now requested MVP functionality.** They move out of the earlier deferred “meal planning” bucket. Broader automated coaching, grocery planning and treatment workflows have not been requested as part of this increment.

Photo-assisted logging, basic Personal Recipe Memory, historical meal snapshots and data controls remain in the proposed full MVP. The new message does not explicitly resolve the flagship-feature choice, optional voice/barcodes/subscriptions, or every earlier deferral.

## How automatic adaptation will work

1. Collect and confirm allergies, intolerances, preferences, relevant health information, and daily target inputs. Preserve “unknown/not provided” separately from an explicit “none reported.” Keep allergies and intolerances distinct.
2. Normalize supported ingredient names and English/Arabic aliases to stable identifiers using reviewed mappings. Ambiguous or unsupported matches require clarification; an LLM cannot approve equivalences.
3. Retrieve candidate foods/recipes with traceable nutrient data and sufficient ingredient information. Evaluate nested ingredients, sauces and any known cross-contact statements where recorded.
4. Apply active hard restrictions before ranking. A missing ingredient list, unresolved allergen mapping, or relevant unsupported clinical rule must never silently count as compatible. Exclude or place the item in a separate verification state; do not present it as an eligible recommendation.
5. Use deterministic nutrient calculations to compare eligible portions/meals with accepted daily targets. Allergies and active clinical restrictions outrank target matching. If there are no eligible candidates, explain the limitation and request input; do not relax hard restrictions to meet calories/macros.
6. AI may help identify, rank or explain eligible candidates. Resolve its output back to approved food/recipe identifiers, calculate values in code, and validate the final output again. Any substitution or generated recipe must pass the same checks. Never trust prompt instructions alone to enforce restrictions.
7. Revalidate saved suggestions, candidate caches and plans after a profile/rule/recipe change. Preserve historical meals as records of what was eaten. Warn on a conflicting manually logged meal while retaining the ability to accurately record actual intake; recommendation exclusion and historical logging have different purposes.
8. Show the relevant restriction and the limits of available ingredient information. Ingredient matching does not establish absence of cross-contact. The [FDA food-allergy reference](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies) discusses undeclared allergens and cross-contact; it is a supporting reference, not a determination of Jordanian/Saudi regulatory requirements or a complete local allergen taxonomy.

For conditions beyond allergies, AI may draft proposed rules and personalized outputs from accepted evidence for nutritionist review. Activation requires an approved rule/source/version/applicability; every personalized clinical plan/warning then needs individual reviewer approval before publication. A diagnosis on file cannot silently activate an invented therapeutic diet. Conflicting or insufficient rules yield an explicit review/insufficient-information state. See the [clinical review workflow](nutrition-app-clinical-review-plan.md).

Daily targets initially need an explicit origin (user-entered, professional-entered or an approved reviewed calculation). The owner's input confirms target-based suggestions, but not the formula or clinical appropriateness of automatically generated targets. The profile schema can support all three origins while that decision is resolved.

## Technical starting recommendation

Implemented **Next.js with TypeScript** for the responsive bilingual client, **FastAPI** for one modular backend, and **PostgreSQL 17** for structured records. Package versions/hashes are locked. JWT/Argon2id authentication, Alembic migrations and container setup are implemented. Private object storage and hosting selection remain later deployment/media work. See the [architecture](docs/architecture.md) and [setup instructions](README.md).

Next.js documents local application setup in its [installation guide](https://nextjs.org/docs/app/getting-started/installation). FastAPI provides OpenAPI-based schemas and interactive API documentation, useful for defining contracts shared with a future mobile client. [FastAPI features](https://fastapi.tiangolo.com/features/)

Implemented repository structure:

```text
apps/web/          responsive client, translations, RTL layouts
services/api/      identity/profile, foods, calculations, meals, restrictions, recommendations
docs/              evolving decisions, source register, verification and handoff
.github/workflows/ automated checks
```

Keep authoritative calculation and restriction rules in the API. Browser checks improve feedback, while the backend enforces the same rules for every client. Use local development first; choose deployment providers and data-processing region after the actual constraints and costs are reviewed. No free-tier pricing or healthcare suitability is assumed.

## Next delivery cycle: foundation and first reliable meal flow

The owner approved this increment and authorized implementation, dependency installation, automatic setup, traceable seeds, robust security and a polished bilingual interface. Checkboxes reflect implementation and verification rather than planning alone.

- [x] **N1 — Initial repository and workflow baseline:** local Git initialized on `main`, origin configured, README/ignore rules prepared, and planning commits pushed using verified account `AbdelrhmanAbuAmashah`. Initial published checkpoint: [44015a0](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project/commit/44015a0). `main` tracks `origin/main`; application CI now passes for the foundation checkpoint under N7. The selected repository is public.
- [x] **N2 — Bilingual responsive shell:** English/Arabic switching, LTR/RTL navigation/forms, local fonts, keyboard-accessible dialogs, responsive dashboard/diary/recipes/profile. Four browser flows pass across both languages and desktop/mobile sizes; screenshots inspected. This is not a claim of a complete accessibility audit.
- [x] **N3 — Identity and onboarding foundation:** JWT/rotating sessions, ownership, country, locale, IANA timezone, preferences, separate confirmed restrictions and explicit target provenance. Metric grams are the current entry interface; the schema permits later unit expansion. Optional self-reported conditions do not activate clinical rules. Export/delete are implemented for current records.
- [x] **N4 — Verified food selection and manual meal entry:** 19 retained original USDA records, source IDs/type/date/payload, separate preparation states, explicit grams/evidence, decimal calculations, draft review and confirmation. Three local illustrative recipes expose ingredients and cooked yield. No model-generated nutrient values.
- [x] **N5 — Persisted diary and dashboard:** confirmed-only totals, saved source/quantity/result snapshots, history, seven-day summary, unavailable nutrient handling, owner checks and concurrent idempotency verification. Historical records remain unchanged after source edits.
- [x] **N6 — Restriction foundation:** confirmed ingredient identities, allergy/intolerance/dislike separation, known-conflict/unknown states and candidate eligibility checks verified after profile edits. Cross-contact remains unknown. Engineering seed mappings are explicit; a complete nutritionist-approved regional taxonomy and the live recommender remain subsequent work.
- [x] **N7 — Verify and record the checkpoint:** `bash scripts/test.sh` passes migration drift/lint, 36 PostgreSQL API tests and four bilingual desktop/mobile browser journeys. Production format/type/build and isolated backup/restore pass. Published code checkpoint [ae28042](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project/commit/ae28042266bf7966c428c0b26a16cefb144f80fd), authenticated as the requested owner; remote SHA matches. [GitHub Actions run 39713405773](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project/actions/runs/39713405773) completed successfully. Remaining limits are in [verification](docs/verification.md).

### Features added after this foundation

- [ ] **Daily suggestions and clinical review:** select/rank eligible meals from traceable recipes against accepted targets/preferences and produce evidence-linked AI drafts. Keep hard restrictions intact; implement nutritionist edit/approval and publication gating for each clinical plan/warning before release to users.
- [ ] **Personal Recipe Memory:** confirmed ingredients, cooked yield, versions and portion reuse; confirm recipe changes while preserving past meals.
- [ ] **Photo assistance:** private upload, food suggestions and targeted clarification, followed by review and confirmation; calculations use the same verified food pipeline. Provider failure preserves manual logging.
- [ ] **Pilot completeness:** remaining accepted health-record fields, data export/deletion/retention, summaries, reviewed content/wording and operational checks before a real-user pilot.

Voice, barcodes, payments, the full practitioner portal, lab interpretation and broad medication/herb/supplement interaction advice remain separately scheduled proposals. A minimal nutritionist approval queue is now required MVP scope. Clinical modules are added individually once their rules and reviews exist.

## Measurable acceptance for the next cycle

- [x] Both English and Arabic core flows work on phone and desktop widths, including mixed Arabic/English food names and Arabic numeric input.
- [x] A user signs in, updates profile restrictions, selects a source-backed food, enters a quantity, reviews/calculates, confirms and later retrieves the meal with matching totals.
- [x] Every confirmed food item has a traceable source ID, basis/units and preserved calculation inputs; unknown nutrient values are not turned into zero.
- [x] Repeated and simultaneous saves create one meal; exposed private-record operations enforce ownership. Personal recipe/media write routes are inactive and require their own checks when introduced.
- [x] Known allergy/intolerance conflicts fail candidate eligibility; incomplete ingredient evidence remains unknown. Profile revisions refresh checks and stale clinical drafts. Actual recommendation generation, target ranking and published-output revalidation are next-increment work.
- [x] Foundation progress records actual check commands/results, the verified remote code revision and a successful GitHub Actions run. At that checkpoint documentation-only follow-ups were excluded; the owner's subsequent feature-branch policy now requires CI on every PR, including documentation changes.

## Open dependencies and current evidence

The selected repository is `https://github.com/AbdelrhmanAbuAmashah/Nutrition-project.git`. The owner completed device sign-in as **AbdelrhmanAbuAmashah**. An authenticated identity request matched that exact username; repository metadata confirmed push/admin permission. `git push --set-upstream origin main` succeeded, publishing the local planning history through [44015a0](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project/commit/44015a0) and establishing upstream tracking. Earlier sandbox/authentication and other-account access failures are resolved. The repository is public. Current status documentation is maintained through follow-up commits. See the [GitHub repository setup guide](https://docs.github.com/en/get-started/start-your-journey/creating-a-repository-for-your-project-on-github).

Needed for affected work: exact clinical population/subtype/rule scope and named reviewer access/availability; target-setting method; numeric spending caps and provider/data-region constraints. GitHub setup/access, repository/account choice, nutritionist availability and individual clinical approval are resolved and must not be re-asked. Continue unaffected work.

## First milestone achieved and next work

**Achieved: the bilingual, source-backed manual logging foundation with profile restrictions and a published checkpoint (7/7 tasks).** The next proposed feature milestone is target-aware daily suggestions with individual clinical approval. See the [S1–S7 plan and remaining inputs](docs/next-milestone.md); Personal Recipe Memory and photo assistance follow in separate increments.
