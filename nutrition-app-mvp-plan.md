# Nutrition app: MVP scope and development start

Updated 22 October 2026 with [owner decisions and the delivery checklist](nutrition-app-project-decisions.md) and the [clinical review workflow](nutrition-app-clinical-review-plan.md). Markets, web-first direction, bilingual support, dynamic restrictions, source integrity, repository target, nutritionist availability and individual clinical approval are confirmed. The owner approved implementation of the logging foundation, which now exists and is tested. Remaining MVP features and clinical activation still follow the staged plan. Also based on the [handoff](nutrition-app-codex-handoff.md), [expanded scope](nutrition-resources-and-expanded-scope-en.md), and [progress report](nutrition-app-progress-report.md).

The MVP means the first useful release for a private pilot. P1 in the progress report is the broader discovery phase. The first coding increment delivers a smaller working flow; completing it does not complete the MVP. Current completion evidence is maintained in N1–N7 and the [progress report](nutrition-app-progress-report.md); remaining checkboxes below describe the larger MVP.

## Product outcome

A user can log a meal, confirm the foods and portion quantities, see traceable nutrient estimates, save the meal, reuse a confirmed personal recipe, and receive meal suggestions constrained by confirmed profile restrictions and daily targets. Photo assistance helps create the draft. The app retains useful history and progressive user-confirmed health records.

Confirmed direction: Jordan and Saudi Arabia; responsive web first; English and Arabic with RTL; solo development; low-to-medium budget; iterative delivery without a fixed deadline. Clinical adaptation includes food-allergy exclusion, with diabetes and hypertension as initial module-definition areas. A certified nutritionist is available and must approve each clinical plan/warning after AI drafts it. Exact condition populations/subtypes, guideline/rule versions, reviewer access/availability and target-setting methods remain open. Adult-only eligibility remains a planning assumption.

## 1. Requirements and resources

| Resource | What is needed for this MVP | When needed |
| --- | --- | --- |
| Product decisions | Confirmed direction/reviewer/publication workflow above; resolve supported population, exact clinical rules/guideline versions, named reviewer access/availability, target method, quantitative budgets and remaining release priorities | Resolve only before affected work; record existing answers without re-asking |
| User flow and screens | Bilingual onboarding/profile, daily summary, add-meal/search, meal review/result, history, recipes, daily suggestions, optional health records, settings/data controls | Sketch the core flow in P1; detail remaining screens incrementally |
| Food-composition data | Traceable food IDs, descriptions, preparation state, nutrient units/basis, source type/version/date; a small relevant starting food set | Fixtures for the first local flow; live food-data access during feasibility |
| Example data | Synthetic calculation cases plus permissioned representative dishes, photos, ingredient quantities and cooked yields | Synthetic cases immediately; target dishes for photo/recipe feasibility |
| Engineering environment | Active public Nutrition-Project-New is the only remaining GitHub repository for this project; verified owner identity, clean owner-only baseline, protected main and feature-branch/PR delivery. Prior Git metadata remains in an ignored local backup; old hosted PR/CI pages were deleted with the two legacy repositories. See [cleanup](docs/repository-cleanup.md). | N1 baseline plus implemented web/API/PostgreSQL, migration/seed, setup and automated checks; see current verification evidence |
| Recommendation rules | Confirmed restrictions, reviewed bilingual ingredient mappings, candidate recipe coverage, accepted daily targets and per-condition approved rules | Design now; activate suggestions after the reliable logging/restriction foundation |
| Media and AI | Private photo storage, bounded uploads, structured analysis output, confirmation flow, provider failure handling; provider terms/cost/data review | Before connecting photo analysis; final provider not selected |
| Review and feedback | Owner-confirmed nutritionist; AI-first drafts; version-specific individual approval for every clinical plan/warning; rule review; representative pilot users | Build minimal queue before clinical publication; exact role/access/availability and source/rule review still need setup |
| Pilot operations | Hosting, access control, retention/deletion/export behavior, backups/restore, error monitoring, support owner | Before private pilot; local development can begin without purchasing services |

**Implemented initial food source:** 19 original USDA FoodData Central records have been retrieved and retained with complete source payloads. Normal setup seeds them without an API key or live provider dependency. The optional import script uses a backend-only data.gov key or the restricted public demo key. Data are CC0 with USDA attribution. See the [source manifest](docs/food-sources.md) and [USDA API guide](https://fdc.nal.usda.gov/api-guide/). This small catalog is not comprehensive Jordanian/Saudi food coverage.

Store the food data type as well as its ID: USDA distinguishes analytical, compiled, and manufacturer-label sources in its [data documentation](https://fdc.nal.usda.gov/data-documentation/). Local dishes can be represented through confirmed ingredients and recipe yields; target-market coverage still needs evaluation.

The implemented stack is Next.js/TypeScript, FastAPI and PostgreSQL, with locked dependency versions, JWT/Argon2id authentication, Alembic migrations and automatic container setup. Private media storage and hosting remain later selections. A mobile frontend is later work using documented backend contracts. Calculation and restriction rules are enforced in the API. See the [architecture](docs/architecture.md).

Budget needs to cover engineering, any design/review work, hosting/database/storage, AI usage, testing, and support. A reliable amount or delivery date requires the unresolved scope, team, usage, and provider decisions. No GPU purchase, custom model training, interactions database, or full food catalog is required to build the first local increment.

## 2. Proposed MVP scope

- [x] **Accounts and preferences:** authentication, owned profile, units/timezone, food preferences and recorded goals. Automated target-setting requires an accepted reviewed method; initially the app can display intake totals and user/professional-entered goals. Links to FR-01.
- [x] **Regional bilingual experience:** Jordan/Saudi country selection and relevant foods, English/Arabic language switching and full RTL-aware core screens, forms, errors, names, units and dates. Links to FR-01/EXT-01 and owner decisions.
- [x] **Manual logging and review:** search/select foods, enter grams or supported explicit portion conversions, correct a draft, confirm once, and save. Preserve drafts and provide clear errors. Links to FR-03/FR-05.
- [x] **Deterministic nutrition:** calculate calories, protein, carbohydrate and fat from traceable food records and quantities. Preserve unavailable values, calculation inputs, source snapshots, and consistent rounding. Label totals as incomplete when constituent values are missing. Links to FR-04/FR-05.
- [ ] **Photo-assisted draft creation:** upload/capture a meal photo, suggest food matches, ask focused quantity/ingredient questions, and require review before confirmation. Show uncertain/unsupported results; manual logging remains usable when analysis fails. No exact weight or allergen-absence claim from a photo. Links to FR-03/FR-05/FR-07.
- [ ] **Basic Personal Recipe Memory:** manually save confirmed ingredients, quantities, method, cooked yield and portions; retrieve/reuse a saved recipe; confirm changes and preserve versions. Historical meals retain the exact inputs/version used. Automatic recipe recognition and natural-language changes can follow later. Links to FR-06.
- [x] **History and summaries:** saved meals, their nutrient breakdowns, daily totals and a simple weekly view, respecting the user's timezone. Links to FR-09.
- [ ] **Progressive health records:** optional current/past medicine history, allergies and intolerances, with user confirmation and unknown fields preserved. No broad interaction or dosing advice. Supplement/herb recording remains an optional extension pending Q08/Q18. Links to FR-02/EXT-02.
- [ ] **Automatic restriction enforcement:** compare known ingredients, including nested ingredients and reviewed aliases, with confirmed allergies and any active reviewed clinical constraints. Exclude conflicting or unresolved candidates from eligible recommendations, preserve unknown states, and revalidate after profile/recipe/rule changes. A logging warning does not erase the ability to record what was actually eaten. Links to FR-07/FR-10 and owner decisions.
- [ ] **Target-aware daily meal/recipe suggestions:** retrieve traceable candidate recipes, apply hard restrictions, calculate portions/totals in code and rank eligible options against accepted goals/preferences. Validate any AI output/substitution again; insufficient coverage or conflicting requirements produce an explicit limitation rather than a relaxed restriction. This moves daily suggestions into the MVP from the previous deferred meal-planning proposal. Links to FR-10 and owner decisions.
- [ ] **Evidence-backed AI drafts and nutritionist approval:** register exact permitted reference versions, retrieve supporting evidence and generate proposed rules, personalized clinical plans and warnings for nutritionist verification. Implement a minimal edit/approve/reject queue and server-side publication gate. Every clinical plan/warning needs approval of its exact version before user access; changes trigger checks/review again. This focused reviewer capability is now MVP scope. See the [clinical review plan](nutrition-app-clinical-review-plan.md).
- [ ] **Data controls and operation:** record ownership, consent for relevant purposes, private media, export/deletion and stated retention behavior, minimal sensitive logging, error reporting and basic operational visibility. Links to FR-12 and the essential operational portion of FR-11.

The latest owner message supersedes earlier platform/market/language proposals and requests daily meal recommendations. Other proposed deferrals remain subject to release prioritization:

- [ ] Later backlog: barcode search, voice entry/conversation, broader automated coaching/grocery planning, billing/subscriptions and full administration/content tooling. Daily target-aware meal suggestions are included above. These defer FR-08 and parts of FR-03/FR-10/FR-11 beyond this proposed pilot MVP.
- [ ] Later backlog: labs/OCR, symptom follow-up, full practitioner portal/sharing, family accounts, wearables and partnerships. The minimal clinical approval queue above is required for the initial clinical workflow.
- [ ] Separately governed scope: specific therapeutic modules, medicine/supplement/herb interactions and interpretation or prescribing based on labs. The clinical adaptation framework is in scope; each clinical rule needs defined evidence, applicable context and review before activation. Catalog-size ambitions remain long-term proposals.

Source requirements stay in the progress register even when a feature is deferred. No original requirement is marked implemented by this proposal.

## 3. Where and how development starts

- [ ] **Step A — Complete P1:** strategic decisions, repository target, reviewer availability and individual approval requirement are recorded. Finish supported-population, exact clinical-rule/source and target-method boundaries, primary flow and acceptance agreement.
- [x] **Step B — Establish the application project:** GitHub repository/account/access and the planning-baseline push are complete. The web/API/PostgreSQL, migrations, checks and setup instructions now exist. Ownership, bilingual profile/restrictions, source-backed food versions, meal drafts/items and calculation snapshots are implemented. Use synthetic data for test fixtures; live manual food selection uses traceable source records.
- [x] **Step C — Build the first working flow:** authenticated user → select food → enter amount → review → calculate → confirm → saved history/daily totals. Verify persistence, missing data, units, timezone boundaries, repeat saves and access isolation.
- [ ] **Step D — Connect and evaluate food data:** initial retained USDA import/seed, source/version snapshots, raw/cooked matching and illustrative recipes are implemented. Wider regional/provider coverage and evaluation remain open. Normal logging does not depend on a live provider.
- [ ] **Step E — Add restriction-aware suggestions, clinical review, Recipe Memory and photo assistance in separate increments:** build reviewed rules/evidence retrieval and eligible candidates; add target-aware AI drafts, automatic validation and individual nutritionist approval before clinical publication; add recipe/yield calculations and versions; introduce private photo uploads and reviewable analysis drafts. Evaluate examples, correction effort, error, latency and per-analysis cost.
- [ ] **Step F — Complete the agreed pilot scope:** health records, confirmed ingredient checks, data controls, summary screens, retention/recovery behavior, review and end-to-end verification. Decide readiness from the acceptance evidence before a consenting private pilot.

Steps B–F are coding increments within the existing P2–P5 roadmap, not newly completed phases or a promised calendar schedule. Data protection is designed from Step B and verified throughout, with pilot readiness checked in Step F. Work starts locally; external distribution is a later release step.

### Acceptance evidence

- [x] Known food, conversion and recipe-yield fixtures produce the agreed totals; missing nutrients remain visibly unavailable.
- [x] Only confirmed meals enter history totals; repeated saves produce one record; confirmed results remain reproducible after food or recipe changes.
- [ ] Different users cannot access each other's records/media; upload, export/deletion and retention behavior match the agreed policies.
- [ ] AI suggestions remain drafts until reviewed; failed/unavailable analysis leaves a usable manual route.
- [ ] Reusing/changing a recipe preserves earlier versions and historical calculations.
- [ ] Known ingredient/allergy conflicts and unknown coverage are handled according to the reviewed rules and wording.
- [ ] Daily suggestions and substitutions obey hard restrictions regardless of target matching or AI output; profile changes trigger revalidation; unsupported clinical rules are explicit.
- [ ] Clinical drafts without nutritionist approval cannot appear in user APIs, UI, notifications or exports. Approval binds the exact content/input/rule/source versions; edited or stale outputs require renewed checks and approval.
- [x] English and Arabic/RTL core flows work on phone and desktop widths, including mixed-script food names and quantities.
- [ ] Each completed verified increment updates the report and is committed/pushed to GitHub with a remote revision recorded, or the specific unsynced state is stated.
- [ ] Representative photo/recipe evaluation has recorded measurements and limitations. Agree pilot thresholds after initial feasibility measurements and before deciding pilot readiness.
- [x] The main flow works end to end on the selected platform, with exact run/check commands and results recorded in the progress report.

## Immediate next milestone

**Next cycle — bilingual foundation and the first reliable manual logging flow.** N1 GitHub setup/synchronization is complete; proceed with N2–N7 in the [decision and delivery record](nutrition-app-project-decisions.md), designing the [evidence/approval records](nutrition-app-clinical-review-plan.md) alongside the foundation. Exact clinical rules/populations and target method remain unresolved for affected work; GitHub access is resolved.

**First working milestone:** demonstrate onboarding/profile → source-backed manual logging → confirmed nutrient calculation → saved history/daily totals in English and Arabic, including persistence, ownership and the tested restriction framework. Record the verified GitHub checkpoint. Daily suggestions, Recipe Memory and photo assistance follow through that same foundation in separate increments.
