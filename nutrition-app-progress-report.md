# Nutrition app: progress report and working checklist

Updated: 22 October 2026, Asia/Amman. Status: the owner-approved bilingual logging foundation is implemented, running locally and published to GitHub. Backend/bilingual browser checks and remote CI pass. The larger AI/clinical MVP and public deployment remain subsequent work.

**Active repository:** [Nutrition-Project-New](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New), public, with a fresh owner-only baseline at `2bc9e5657c19c2ea190a8ba9c17362cd2a5d3328`. GitHub resolves both baseline author and committer to `AbdelrhmanAbuAmashah`. It is now the only remaining GitHub repository for this project. The owner-authorized cleanup deleted `Nutrition-project` and `Nutrition-Project-New-history-backup`; three unrelated repositories were preserved. Prior Git metadata remains in an ignored local backup. The local working repository uses the clean history and canonical origin. New changes continue through protected feature branches/PRs. See the [cleanup record](docs/repository-cleanup.md).

This is the ongoing progress resource requested by the owner. The roadmap uses the handoff's six phases. Confirmed owner direction is recorded in the [project decisions and next delivery cycle](nutrition-app-project-decisions.md); unresolved proposals remain labeled. Explicit owner decisions supersede earlier conflicting proposals. Update this report after each completed increment or new resource review.

## The idea from A to Z

Build a responsive web nutrition companion for Jordan and Saudi Arabia, in English and Arabic with RTL. It helps people record intake, understand source-backed nutrient estimates, reuse confirmed recipes and receive daily meal suggestions adapted to their confirmed profile restrictions and daily targets. A user sets preferences/goals and relevant health information, then reviews and confirms meal inputs. Calculation code uses traceable food-composition records. Voice and barcodes remain later proposals. Confirmed meals appear in history and daily summaries; a mobile client is later work using the same API contracts.

The proposed distinguishing feature is **Personal Recipe Memory**: remember the ingredients, quantities, cooking yield, and portions of a person's actual recipe. When they repeat it or change an ingredient, confirm the change and calculate a new version. Preserve the original calculations for earlier meals. Initially, this memory means storing confirmed information and retrieving it.

Dynamic adaptation includes automatic allergen exclusion and initial module definition for diabetes/hypertension/allergies. The owner confirms a certified nutritionist is on board. AI prepares evidence-grounded rules, personalized clinical plans and warning drafts first; the nutritionist verifies them. Every clinical plan/warning must receive individual approval before user publication. Exact condition populations, rule/source versions, named reviewer access/availability and target-setting methods remain open. See the [clinical review plan](nutrition-app-clinical-review-plan.md).

The proposed commercial path is a consumer product with basic free logging and paid convenience features. A practitioner product is another option awaiting a decision. Neither pricing nor a business model has been approved.

## Verified progress

**Working product milestones achieved: 1 — the bilingual, source-backed manual logging foundation.** The complete flow is account/onboarding → food or sample recipe → quantity/time → review → confirmation → persisted diary/dashboard, in English and Arabic.

**Foundation checklist: 7 of 7 tasks complete (N1–N7).** The active repository contains the foundation from root [2bc9e56](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New/commit/2bc9e5657c19c2ea190a8ba9c17362cd2a5d3328). Its [post-merge CI run 39726433154](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New/actions/runs/39726433154) completed successfully at revision `68ac7d0`, read back during cleanup. Legacy checkpoint `ae28042` and run `39713405773` were verified previously; their hosted pages were removed with the old repository. Detailed TODOs are in the [decision record](nutrition-app-project-decisions.md); commands/results/limits are in [the evidence log](docs/verification.md).

**Broader handoff phases: 0 of 6 fully closed.** P2/P3 now have substantial implemented foundation work; their wider photo/pilot/MVP exit criteria remain open. Clinical populations/rules, reviewer access and automatic target methodology are still unresolved. This broader phase count is separate from the achieved foundation milestone and is not an overall completion percentage.

### Feature-branch workflow adoption (SRC-19)

- [x] **W1 — Dedicated branch and persistent instructions:** this maintenance milestone uses `feature/github-feature-branch-workflow`; the workflow guide, root agent instructions and PR template require a dedicated branch and reviewable PR for each future milestone.
- [x] **W2 — Local verification before publication:** `bash scripts/setup.sh` and `bash scripts/test.sh` pass again: production format/type/build, migration drift check, Ruff, 36 API tests and four bilingual desktop/mobile browser flows. Workflow YAML/protection JSON validation and `git diff --check` pass.
- [x] **W3 — Applied GitHub protections:** the owner-authenticated API read-back confirms main requires PRs, GitHub Actions `verify` (app ID 15368), strict up-to-date checks, resolved conversations and linear history. Administrators are included; force pushes/deletion are blocked. Solo mode requires no second approving reviewer. Existing rules/protections were inspected before applying the versioned policy.
- [x] **W4 — Publish through a PR:** the original workflow branch was published as legacy `Nutrition-project` PR #1 with scope and local results. That hosted page was later deleted with the old repository. The active repository's [PR #1](https://github.com/AbdelrhmanAbuAmashah/Nutrition-Project-New/pull/1) demonstrates the protected delivery path with successful CI and a completed merge. Future changes require their own current checks before normal merging.

The [workflow guide](docs/github-workflow.md) describes this policy. Workflow configuration/publication tasks W1–W4 are complete; every new PR records its own checks and merge state. The existing 7/7 foundation task count remains unchanged; this is a delivery-process milestone rather than a new clinical/AI feature.

### Repository cleanup (SRC-21)

- [x] Inventory all owned repositories and identify the two older nutrition project copies.
- [x] Verify canonical fetch/push origin, synchronized main, exact repository IDs and the ignored local Git-history backup.
- [x] Delete `Nutrition-project` and `Nutrition-Project-New-history-backup` using the owner-authenticated API; verify HTTP 204 deletion responses followed by HTTP 404 reads.
- [x] Re-enumerate the account: `Nutrition-Project-New` is the only remaining repository for this project; all three unrelated repositories remain.
- [x] Verify the sole contributor is `AbdelrhmanAbuAmashah` and protected main retains PR enforcement and strict required `verify` checks.

The [cleanup record](docs/repository-cleanup.md) contains IDs, verification time and local recovery details. The name remains unchanged. This repository maintenance does not add a product milestone or activate clinical features.

- [x] Read the complete handoff.
- [x] Read the complete expanded resources and scope document.
- [x] Inspect the supplied project files.
- [x] Separate established intent, proposals, and later expansion.
- [x] Record requirements, resource status, questions, and a proposed roadmap in this report.
- [x] Prepare and update the [MVP scope and development start plan](nutrition-app-mvp-plan.md) for the owner's strategic inputs. Remaining scope proposals are labeled.
- [x] Receive and record the owner's initial strategic/product decisions; see SRC-06 and D-01–D-11 below.
- [x] Define the next delivery cycle N1–N7, automatic restriction behavior and acceptance evidence in the [decision record](nutrition-app-project-decisions.md).
- [x] Record repository selection, nutritionist availability, AI-first drafting and approval of each clinical plan/warning in the [clinical review plan](nutrition-app-clinical-review-plan.md).
- [x] Prepare a repository README and ignore rules; check initial WHO/FAO, diabetes, hypertension and Saudi educational references with review limits recorded.
- [x] Initialize local Git on `main`, configure the owner-selected `origin` and commit the eight-file planning baseline as `d07c310`.
- [x] Verify `AbdelrhmanAbuAmashah` identity and repository push permission, publish the planning checkpoint and configure `main` to track `origin/main`.
- [x] Receive explicit approval of the foundation phase plan and automatic setup/security/seed/UI requirements (SRC-17).
- [x] Implement and verify the first working meal-logging flow, including desktop/mobile English and Arabic.
- [ ] Close the larger private-pilot MVP scope, clinical population/rules, target method and release criteria before affected activation.

At the original review, the workspace contained two project documents and no application code. It now contains the web/API/database implementation, locked packages, migrations, source data, tests, setup scripts and operating documentation. The referenced original `nutrition-app-project-plan.md` was not supplied; the self-contained handoff remains the available historical baseline.

Initial review evidence was file inventory and complete document reading. Current application evidence includes a successful production build, PostgreSQL migration/seed and drift checks, 36 backend tests, four bilingual browser journeys, visual screenshot review and an isolated backup/restore exercise. See [verification details](docs/verification.md). No clinical efficacy, complete accessibility audit or public-deployment readiness is claimed.

Subsequent planning update, 22 October 2026: the USDA API guide and data-type documentation were opened for the MVP resource plan. The limited findings and references are recorded below and in the MVP plan. Other external source and clinical-review statuses remain unchanged.

Earlier owner-input checks (resolved later), 22 October 2026: SRC-06 processed and Next.js, FastAPI, FDA and GitHub references opened. At that point the workspace had no usable Git repository and sandboxed CLI checks reported invalid credentials. The subsequent approved external authentication check corrected that result. No app tests ran.

Repository/expert update, 22 October 2026: owner selected Nutrition-project, confirmed nutritionist availability and required individual clinical approval. Initial baseline `d07c310` was published through `44015a0` after owner authentication. `main` tracks `origin/main`; earlier account-access blockers are resolved. Application implementation has now followed explicit approval. No clinical rule or personalized clinical output has been approved or activated.

## Resource register

| ID | Resource and source location | Date / attribution | Review and permissions | Impact / next action |
| --- | --- | --- | --- | --- |
| SRC-01 | [nutrition-app-codex-handoff.md](nutrition-app-codex-handoff.md), sections 1–14 | 9 Oct 2026; owner-supplied handoff; individual author not stated | Fully read 22 Oct 2026 for planning. No individual patient records observed. External data/content rights remain unverified. | Baseline FR-01–FR-12, six delivery phases, resource intake, and acceptance expectations. Confirm proposals with owner. |
| SRC-02 | [nutrition-resources-and-expanded-scope-en.md](nutrition-resources-and-expanded-scope-en.md), sections 1–12 | 9 Oct 2026; attributes ideas to the owner; individual compiler not stated | Fully read 22 Oct 2026 for planning. No individual patient records observed. Its descriptions of prior source reviews are not new verification in this session. | Adds EXT-01–EXT-06 below. Separate recording/education from clinical functionality; stage expansion. |
| SRC-03 | `nutrition-app-project-plan.md`, referenced by SRC-01 | Original proposal dated 9 Sep 2026 according to handoff | Not supplied; contents, author, permissions, and differences cannot be checked. | Optional reconciliation if supplied; SRC-01 is the current available baseline. |
| SRC-04 | [USDA API guide](https://fdc.nal.usda.gov/api-guide/) | USDA official technical reference; page revision date not stated; retrieved 22 Oct 2026 | API/key handling, search/details and CC0 attribution sections read during planning; original-record retrieval subsequently recorded under SRC-18. | Supports FR-03/FR-04; retained source import/seed implemented, wider regional coverage remains open. |
| SRC-05 | [USDA data-type documentation](https://fdc.nal.usda.gov/data-documentation/) | USDA official reference; page revision date not stated; retrieved 22 Oct 2026 | Data-type comparison read; no individual food dataset or local coverage was evaluated. | Supports FR-04/FR-05 source-type provenance; retain data type with food records. |
| SRC-06 | [Owner project decisions](nutrition-app-project-decisions.md), confirmed direction and scope change | Owner's strategic/workflow message, recorded 22 Oct 2026 | Read and normalized for planning; no individual patient data. Explicit owner direction takes precedence over earlier proposals. | Confirms two markets, bilingual web, solo/iterative work, traceability, GitHub and restriction-aware daily suggestions. No app features implemented. |
| SRC-07 | [Next.js installation](https://nextjs.org/docs/app/getting-started/installation) | Official technical reference; retrieved 22 Oct 2026 | Setup/tooling read; the subsequent implementation locks Next.js and its dependencies and verifies the container production build. | Supports implemented D-06 web-client setup. |
| SRC-08 | [FastAPI features](https://fastapi.tiangolo.com/features/) | Official technical reference; retrieved 22 Oct 2026 | OpenAPI, schemas and interactive documentation sections read. | Supports shared API contracts; no API implemented. |
| SRC-09 | [FDA food allergies](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies) | Official reference; retrieved 22 Oct 2026 | Ingredient labeling, undeclared allergens and cross-contact discussion read. This does not verify Jordanian/Saudi law or establish a complete mapping taxonomy. | Supports FR-07/NEW-02 unknown/coverage design; reviewer and local implementation scope remain open. |
| SRC-10 | [GitHub repository setup](https://docs.github.com/en/get-started/start-your-journey/creating-a-repository-for-your-project-on-github) | Official technical reference; retrieved 22 Oct 2026 | Workflow read; existing owner-selected remote used. Identity, push permission and successful initial push verified. | Supports NEW-04; initial baseline published through 44015a0, with main tracking origin/main. |
| SRC-11 | [Repository/expert/approval owner answers](nutrition-app-clinical-review-plan.md), owner decisions | Owner's asynchronous answers, 22 Oct 2026 | Repository URL and certified reviewer availability supplied; individual clinical plan/warning approval explicitly confirmed. No patient data supplied. | Resolves Q27 target and Q28 approval policy; informs D-05/D-10/D-12 and NEW-05. Exact module scope and permissions remain open. |
| SRC-12 | [WHO healthy diet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet) | WHO, dated 26 Jan 2026; retrieved 22 Oct 2026 | General nutrition fact sheet read. Reuse rights and clinical applicability must be checked for the selected runtime use. | General principles candidate for NEW-05; no clinical rule approved or ingested. |
| SRC-13 | [FAO/WHO joint statement](https://www.who.int/publications/i/item/9789240101876) | FAO/WHO, 24 Oct 2024; ISBN 9789240101876; retrieved 22 Oct 2026 | Publication overview read; full 22-page publication not read. No reuse permission or full-text ingestion claimed. | Candidate general reference; select exact relevant content with reviewer. |
| SRC-14 | [NIDDK: Healthy Living with Diabetes](https://www.niddk.nih.gov/health-information/diabetes/overview/healthy-living-with-diabetes) | NIDDK official educational page; retrieved 22 Oct 2026 | Meal-planning and individualized-context sections read; no complete diabetes guideline/rule set reviewed. | Starting source for module definition and reviewer selection of exact clinical guidelines. |
| SRC-15 | [NHLBI DASH eating plan](https://www.nhlbi.nih.gov/health/dash-eating-plan) | NHLBI, page last updated 25 Feb 2026; retrieved 22 Oct 2026 | Overview/targets and contextual material read; no targets approved for any individual. | Hypertension module preparation; clinician must resolve applicability/conflicts. |
| SRC-16 | [Saudi MOH hypertension nutrition](https://www.moh.gov.sa/en/healthawareness/educationalcontent/food-and-nutrition/pages/003.aspx) | Saudi MOH, content update shown 22 Apr 2025; retrieved 22 Oct 2026 | Educational page read; permissions/local protocol suitability unverified. | Regional educational reference candidate; no executable rule approved. |
| SRC-17 | Owner's phase approval and six enterprise directives, conversation | Owner, 22 Oct 2026 | Explicit authorization to implement, install/configure dependencies, create files/scripts, seed data and build the approved phase. No real patient records supplied. | Authorizes bilingual UI, scalable PostgreSQL foundation, zero-to-one setup, security/error handling, realistic traceable seeds and autonomous delivery. |
| SRC-18 | [Retained USDA records and source manifest](docs/food-sources.md) | USDA FoodData Central, retrieved 22 Oct 2026 | 19 original SR Legacy API records retained; CC0, source IDs/type/date/units preserved. Arabic labels and sample recipes are project editorial content. | Implemented manual-food pipeline for FR-04/FR-05/NEW-03. Three recipes are illustrative; source-backed data do not establish exact real-world portion accuracy or clinical suitability. |
| SRC-19 | Owner's feature-branch workflow directive, conversation | Owner, 22 Oct 2026 | Explicit request for dedicated milestone branches, complete local verification, PR summaries/results and merging only after automated checks pass. | Applies immediately to this workflow setup and every subsequent milestone; supersedes the initial direct-to-main checkpoint practice. Existing published foundation history remains the baseline. |
| SRC-20 | Owner's Git identity, new-repository and final owner-only contributor instructions, conversation | Owner, 22 Oct 2026 | Requested local identity AbdelrhmanAbuAmashah and public Nutrition-Project-New. Initially selected preserved history, then explicitly requested a fresh repository with only their own attribution. Account authentication already works; a GitHub noreply email provides verified attribution. | Final owner-only instruction supersedes preservation inside the active repository. Existing data/code are retained; historical copies were initially backed up, with the remote copies subsequently deleted under SRC-21. Fresh baseline 2bc9e56 has no inherited parents and is attributed only to the owner. |
| SRC-21 | Owner's repository cleanup instruction and GitHub deletion authorization, conversation; [verification record](docs/repository-cleanup.md) | Owner, 22 Oct 2026 | Explicit authorization to identify and delete older project repositories while preserving Nutrition-Project-New. Authenticated owner, exact IDs and local Git backup checked before deletion. | Two legacy repositories deleted and verified absent; canonical origin and sole owner contributor verified; three unrelated repositories preserved. Prior Git metadata remains locally, while old hosted PR/CI pages are unavailable. Optional rename was not requested. |

External resources stay under SRC-01 section 11 and SRC-02 references R01–R13. Before using a resource in software, record its exact version, retrieval date, permitted use, review scope, and linked requirement. The addendum explicitly records incomplete reviews for some references; none should silently become an approved executable rule.

You will provide additional resources. I will read them, register their sources, reconcile requirements, and update the plan before applying affected changes.

## Scope and decisions

Established intent in SRC-01 section 2 and SRC-06 now includes photo-assisted logging, traceable nutrition calculation, medication/allergy history, dynamic profile-aware recommendations, cost awareness, bilingual web delivery and GitHub workflow. Specific clinical modules and remaining release boundaries still need definition. Owner instructions have already resolved the decisions marked confirmed below.

| Decision | Current state | Proposed starting position / reason |
| --- | --- | --- |
| D-01 Audience and intended use | Partially resolved by owner | User-profile nutrition/wellness with dynamic health constraints. Adult-only eligibility, first paying customer and exact clinical modules remain open. |
| D-02 Market and language | Confirmed by owner, 22 Oct 2026 | Jordan and Saudi Arabia; English and Arabic with RTL in the initial web product. |
| D-03 Consumer platform | Confirmed by owner, 22 Oct 2026 | Responsive web first; mobile later, using shared backend contracts. |
| D-04 Main differentiator | Proposed | Personal Recipe Memory; validate usefulness through repeated-meal logging. |
| D-05 Health-feature boundary | Owner confirmed; precise activation scope open | Allergies plus diabetes/hypertension module definition. AI drafts rules/plans/warnings from accepted evidence; nutritionist reviews. Rules need approval before activation; each personalized clinical plan/warning needs approval before publication. |
| D-06 Technical stack | Implemented within approved phase | Next.js/TypeScript, FastAPI, PostgreSQL 17, Alembic and Docker; locked packages, JWT/Argon2id sessions, generated local configuration. Private media storage/hosting remain later work. |
| D-07 Food and AI providers | USDA seed implemented; AI vendor pending | 19 retained USDA records plus reproducible import and provenance. Local recipes are illustrative. Wider regional coverage, AI provider/costs and clinical source activation remain open. |
| D-08 Budget, staffing, dates, pricing | Partially resolved by owner | Solo developer, low-to-medium budget, continuous iterative delivery without a fixed deadline. Numeric spending caps, prices and usage estimates remain open; historical figures are not commitments. |
| D-09 Focused pilot MVP boundary | Updated with owner scope expansion | [MVP plan](nutrition-app-mvp-plan.md) now includes target-aware daily meal/recipe suggestions with automatic restrictions. Voice/barcodes/payments and broad treatment/interaction modules remain later proposals; other prior MVP features remain proposed. |
| D-10 GitHub workflow | Protected feature-branch policy, owner-only active repository and cleanup (SRC-19/SRC-20/SRC-21) | Nutrition-Project-New is the only remaining project repository, initialized at owner-only root 2bc9e56 with the verified foundation's identical files. Prior Git history remains in an ignored local backup; deleted repositories' hosted PR/CI pages are unavailable. Future milestones use dedicated branches, local checks and PRs, with strict GitHub Actions `verify`, administrator enforcement and resolved conversations before normal merging. |
| D-11 Agent role | Confirmed by owner | Technical assistant and co-pilot across architecture, development, debugging and planning, with maintained decisions, verification evidence and progress. |
| D-12 Clinical review and publication | Confirmed by owner, 22 Oct 2026 | Certified nutritionist on board. AI drafts first; reviewer verifies/edits/approves every clinical plan and warning before users can see it. Minimal review queue is required MVP functionality. |

## Findings and remaining release decisions

1. **The expanded vision exceeds the original delivery assumption.** SRC-01 section 10 assumes a focused first release; SRC-02 sections 3–9 add many populations, conditions, labs, substances, and interaction types. A full clinical platform needs a new estimate and separate module plans. The documents already acknowledge this distinction.
2. **Consumer and practitioner products require different workflows.** The owner's direction describes user onboarding/profile and a web product. Supported populations and first paying customer still need confirmation before specialist sharing or billing work.
3. **The launch feature list needs an explicit cut.** Photo, manual, barcode, voice, recipe memory, administration, and subscriptions are described in the handoff. Decide what is essential for the first usable release and what comes in later increments. The proposed first coding slice below covers only the meal-logging foundation.
4. **Dynamic adaptation needs executable boundaries.** Automatic allergy-aware daily suggestions are now required. Keep health entity types distinct, enforce reviewed hard restrictions in code before and after AI, and define each additional clinical rule/reviewer before activation. SRC-02 sections 1, 3, 8 and SRC-06 support these boundaries.
5. **Photo analysis needs measured feasibility.** The documents provide no achieved accuracy, model benchmark, or validated pilot result. Confirm portions, preserve unknowns, and benchmark target dishes before approving accuracy claims. See SRC-01 sections 3–4 and 9.
6. **The initial source pipeline is implemented.** Exact food versions, cooked/raw states, sample recipe yields, source snapshots and missing nutrients are tested. The catalog is small; regional brands, measured local recipes and wider coverage remain to be curated and reviewed.
7. **Catalog counts are ambitions.** SRC-02 section 4 gives proposed herb, supplement, and interaction counts, without completed catalogs or an interaction dataset. Define substances versus branded products and select initial coverage. Its interaction examples are review material, not approved production rules.
8. **Bilingual and data handling work starts early.** English and Arabic/RTL are confirmed initial requirements. Design both immediately; settle optional health data, processing region and retention before affected integrations. Synthetic fixtures are for development/testing; live manual food entries must use traceable source-backed records.
9. **Recommendations expanded the MVP.** Profile-restricted, target-aware daily suggestions supersede the earlier meal-planning deferral. This adds candidate recipe coverage, target provenance, a rule framework, final validation and new verification; it changes workload for the solo developer. No unchanged historical deadline/budget is implied.
10. **GitHub setup is complete.** Owner identity, push permission and upstream tracking are verified. Application CI configuration now accompanies code; only actual remote run evidence counts as a successful CI run.
11. **Clinical review changes the MVP workflow.** A nutritionist is available and individual clinical approval is mandatory. Add evidence-linked drafts, a minimal assigned-review queue, version-specific approval, stale-output checks and publication authorization; a full practitioner portal remains later work. Sources improve grounding but do not replace calculation checks or clinical sign-off.

No source-document edits are necessary to preserve the idea at this stage. The main work is to resolve these open choices and record the accepted first release. Any later source corrections should retain their provenance and the owner's decisions.

## Requirements checklist and traceability

The approved foundation implements all or part of FR-01–FR-05, FR-07, FR-09, FR-12 and NEW-01–NEW-04. The table retains the wider product scope; rows spanning future features are not fully complete merely because their schema exists. Clinical approval, photo/voice, Personal Recipe Memory, recommendations and specialist modules remain inactive.

| ID | Product TODO | Source | Expected delivery / evidence |
| --- | --- | --- | --- |
| FR-01 | Accounts, profile, onboarding, consent | SRC-01 §4 FR-01 | Foundation implemented/tested: owned profile, optional context, service consent, session controls. Public account lifecycle/recovery is later work. |
| FR-02 | Medication, allergy, intolerance history | SRC-01 §4 FR-02 | Partial: separate confirmed allergies/intolerances/dislikes and self-reported conditions implemented. Medication/lifecycle UI remains later; schema alone does not complete it. |
| FR-03 | Meal capture, review, confirmation, failure handling | SRC-01 §4 FR-03 | Manual flow implemented/tested, including concurrent duplicate saves. Photo/voice/barcodes remain later. |
| FR-04 | Deterministic nutrient calculation | SRC-01 §4 FR-04; SRC-02 §2 | Foundation implemented/tested: decimal quantities, units, null nutrients, original USDA records, recipe yield and historical snapshots. |
| FR-05 | Evidence and uncertainty | SRC-01 §4 FR-05 | Source, entered/weighed portion evidence, incomplete totals and ingredient coverage are visible. No exact intake/clinical safety claim. |
| FR-06 | Personal recipes and versions | SRC-01 §4 FR-06 | P4, with recipe-related feasibility in P2: changing a recipe leaves historical meals intact. |
| FR-07 | Known ingredient/allergy checks | SRC-01 §4 FR-07 | Foundation checks implemented/tested: conflicts and unknowns retained; candidate eligibility fails hard conflicts/unknowns. Full taxonomy, nutritionist wording and live recommendations remain later. |
| FR-08 | Push-to-talk, transcript review | SRC-01 §4 FR-08 | P4 if accepted: food names, amounts, units, dialects, and recording retention verified. |
| FR-09 | Meal history, totals, summaries, trends | SRC-01 §4 FR-09 | Foundation implemented/tested: daily diary, seven-day totals, source breakdown, timezone/DST bounds. Broader reporting remains later. |
| FR-10 | Educational guidance and personalization | SRC-01 §4 FR-10 | Schedule after approved content and review responsibilities; responses traceable to accepted sources. |
| FR-11 | Admin tools, subscriptions, usage limits | SRC-01 §4 FR-11 | P4 if accepted: permissions and entitlement/payment failure cases verified. |
| FR-12 | Export, deletion, retention, consent withdrawal | SRC-01 §4 FR-12 | Current profile/diary export and password-confirmed account deletion/cascades tested. Broader retention, media and sharing withdrawal require their later modules/deployment policy. |
| EXT-01 | Topic register: separate goals, conditions, symptoms, patterns, life stages, lifestyle, lab observations, substances | SRC-02 §§1, 3, 11 | Design in P1; stage implementation with relevant features. One identifier per topic with tags and required language aliases. |
| EXT-02 | Supplement/herb records, product/ingredient distinction, phased catalog | SRC-02 §4 | Candidate early health-profile extension; exact coverage pending. User-confirmed recording and catalog coverage are separate deliverables. |
| EXT-03 | Education, symptoms, lab storage/trends, practitioner export | SRC-02 §§7–8 | Later knowledge/follow-up increment unless explicitly prioritized; confirmed values, units, dates, source and sharing controls. |
| EXT-04 | Evidence-backed interaction records and checks | SRC-02 §§5–6 | Separate governed increment: licensed coverage, approved rules, reviewer, source version, unknown states, verification. |
| EXT-05 | Selected clinical and high-specialization modules | SRC-02 §§8–9 | Separate module specifications and estimates; clinical ownership, evidence, permissions, and module-specific acceptance required. |
| EXT-06 | Practitioner collaboration and sharing | SRC-01 §5; SRC-02 §§8, 12 | Later backlog under consumer-first proposal; revisit P1 architecture if practitioner-first is chosen. |
| NEW-01 | Jordan/Saudi responsive web and English/Arabic RTL core flows | SRC-06; SRC-07 | Foundation implemented: four bilingual phone/desktop journeys pass, including Arabic numeric input, localized errors and saved profile country/timezone. |
| NEW-02 | Automatic profile restrictions and target-aware daily meal/recipe recommendations | SRC-06; SRC-02 §8; SRC-09 | Framework in N3/N6; live suggestions in the following increment. Reject known conflicts and unknown coverage, revalidate on edits, enforce reviewed clinical rules and validate final AI output. |
| NEW-03 | Verified manual-food source pipeline | SRC-06; SRC-04/SRC-05/SRC-18 | N4/N5 implemented/tested: 19 original USDA records, source version/snapshot, quantities, matching preparation states and null handling. No AI-generated authoritative nutrients. |
| NEW-04 | GitHub-backed iterative delivery | SRC-06; SRC-10 | N1/N7 complete: owner-authenticated remote checkpoint ae28042, matching SHA, successful application CI and updated progress evidence. Credentials and patient data stay outside Git. |
| NEW-05 | Evidence-backed AI clinical drafts, nutritionist review and individual publication approval | SRC-11–SRC-16; SRC-04/SRC-05/SRC-09 | Before clinical release: source/rule registry, exact evidence links, checks, edit/approve/reject queue, approval audit/version binding and tests blocking unapproved/stale output across all user delivery paths. |

## Proposed delivery roadmap

P1–P6 below follow the handoff's six delivery phases. The addendum's M1–M4 labels describe **scope tracks** (foundation through high specialization), not completed delivery milestones. They must not be added to the phase completion count.

The [MVP plan](nutrition-app-mvp-plan.md) incorporates the owner's direction. N1–N7 track the first working increment separately from the complete handoff phases. The logging foundation is achieved; the broader MVP remains in progress.

| TODO | Phase / status | Exit evidence and dependency |
| --- | --- | --- |
| [ ] P1 | Discovery and scope agreement — in progress; owner strategic decisions recorded | Complete remaining supported-population, clinical-rule, target-method and release acceptance boundaries. Markets, platform, languages, solo capacity, iterative approach and GitHub intent are already answered. |
| [ ] P2 | Feasibility — foundation complete; wider trials open | Bilingual logging/calculation/history, source-backed catalog and restriction framework verified. Representative photo/personal-recipe accuracy, correction effort, latency and cost trials remain. |
| [ ] P3 | Core alpha — partial implementation | Accounts, ownership, manual capture, optional profile context, history and current data controls work together with tests. Remaining agreed MVP capture/clinical/reviewer features are open. |
| [ ] P4 | Differentiation and commercial features — not started | Recipe-memory/versioning and restriction-aware daily suggestions within accepted MVP scope; clarification and any later-approved voice/barcodes/admin/subscriptions. Verify repeat-recipe, restriction, target and failure scenarios. |
| [ ] P5 | Pilot and hardening — not started | After feature readiness: appropriate reviewed content, privacy/security checks, consenting pilot, measured outcomes, defects triaged, release criteria assessed. Pilot size/thresholds need agreement. |
| [ ] P6 | Launch preparation — not started | After pilot acceptance: approved launch claims, operational readiness, restore/deletion checks, support, platform distribution, and staged release/handover. |

The historical 16–20 week team estimate and 6–9 month solo estimate in SRC-01 section 10 are unverified planning assumptions. No new deadline, operating budget, price, or clinical-module estimate is committed by this report.

### Later scope checklist

- [ ] Reviewed knowledge, symptom and laboratory follow-up, as selected.
- [ ] Full practitioner portal and consent-based sharing, if consumer-first is selected initially. The minimal nutritionist review/publication queue is required MVP work under NEW-05.
- [ ] Separately approved interaction coverage and clinical modules.
- [ ] Family accounts, household sharing, wearables, broader/grocery planning and partnerships, as prioritized. Daily restriction-aware meal suggestions are requested MVP work under NEW-02.
- [ ] Specialized populations and therapeutic workflows through dedicated reviewed tracks.
- [ ] Additional languages beyond English/Arabic, broader regional coverage, richer voice or custom model work after demonstrated need. Both initial markets and Arabic RTL are already in scope.

## Questions for the owner

This preserves question IDs and owner answers. Do not re-ask the repository URL, reviewer availability, languages/platform/markets or individual clinical approval policy. Remaining affected-work decisions include precise populations/module/guideline scope, named reviewer access/availability, target-setting method and quantitative spending caps. Technical choices can be handled by the engineering lead.

### Needed to agree on the first release

1. **Q01 — Audience and market:** Who is the first user and paying customer: individual adults, dietitians, or clinics? Which country comes first?
   Answer/status: Jordan and Saudi Arabia confirmed. The flow is user/profile-oriented; supported age/population and first paying customer remain open.
2. **Q02 — Intended use:** Is launch focused on general nutrition/wellness, or must it include specific clinical guidance? If clinical guidance is essential, name the first one or two modules and the professional responsible for reviewing them.
   Answer/status: Wellness plus dynamic adaptation; allergy exclusion and diabetes/hypertension module definition. Certified nutritionist available. Exact diabetes subtype/population, approved rules/guidelines and named reviewer access remain open.
3. **Q03 — Platform:** Which comes first: Android/iOS mobile or responsive web? Are there platform constraints already agreed with a client?
   Answer/status: Responsive web first, mobile later. Resolved.
4. **Q04 — Language:** English, Arabic, or both at launch? Are Arabic RTL and a particular dialect required initially?
   Answer/status: English and Arabic with RTL confirmed. Voice/dialect specifics can wait for voice scope.
5. **Q05 — Priority:** Is Personal Recipe Memory the main differentiator? Which three outcomes must the first release deliver, and which expanded features can wait?
   Answer/status: Verified manual logging, dynamic onboarding/profile adaptation and allergy/target-aware daily suggestions are explicit priorities. Flagship selection and remaining deferrals not explicitly accepted.
6. **Q06 — Capacity:** Who will build/review the product, what are the development and monthly operating budgets, and is there a fixed deadline or contractual commitment?
   Answer/status: Solo developer, low-to-medium budget, continuous measurable iterative progress without a fixed deadline; certified nutritionist review support confirmed. Numeric spending caps and reviewer availability/turnaround remain open.
7. **Q07 — Existing decisions/resources:** Is there existing code elsewhere, a design, original proposal, client commitment, dataset, or prior decision we must reconcile? Is either supplied document superseded by newer information?

### Resolve during discovery and before affected implementation

8. **Q08 — Health profile:** Which conditions, medicines, allergies, intolerances, supplements, and herbs should users record initially? Which are optional, and which may influence app behavior?
   Answer/status: Profile/history must adapt recommendations; food allergies are explicitly active restrictions. Exact additional condition/substance coverage remains open.
9. **Q09 — Medical advice:** Is storing medicine history sufficient at launch, or are interaction warnings mandatory? If mandatory, what exact interaction types, reviewed sources, licensing budget, and reviewer are available?
10. **Q10 — Labs and symptoms:** Are these launch features or later work? Is their purpose recording/trends, clinician sharing, or interpretation?
11. **Q11 — Personalization:** Do we calculate calorie/nutrient targets, record a user/professional target, or only show logged totals initially? Who approves any calculation and recommendation method?
   Answer/status: Daily targets must guide meal suggestions. Target origin/formula and review are not specified; design provenance fields now and use only an accepted method when activating suggestions.
12. **Q12 — Eligibility:** How should the product handle minors, pregnancy, complex conditions, or eating-disorder risk? Who defines the supported experience and escalation route?
13. **Q13 — Capture order:** Must photo, barcode, and voice all be available in the first release? Can the first coding increment be manual logging, followed by photo assistance?
   Answer/status: The owner approved and authorized the manual logging foundation first. That flow is implemented; photo/voice/barcode ordering beyond this increment remains open.
14. **Q14 — Portions:** Will users weigh meals, confirm estimates, select household measures, or use several methods? How much clarification effort is acceptable?
15. **Q15 — Food coverage:** Which dishes, cuisines, local brands, and food types are essential? Are measured recipes, representative photos, or label examples available with permission?
   Answer/status: Jordan/Saudi coverage is required. Initial dish/brand list and permissioned examples are still needed progressively.
16. **Q16 — Nutrition output:** Which nutrients, units, summaries, and accuracy claims matter? What would count as a useful, successful meal estimate for the first users?
   Answer/status: Verified, traceable manual food sources and trustworthy calculated outputs are required. Specific accuracy claims/metrics remain unapproved; source integrity is not proof of exact portion measurement.
17. **Q17 — Recipe behavior:** Are recipes personal or shared? Should each changed quantity create a recipe version, or can a user make a one-meal adjustment while preserving the saved recipe?
18. **Q18 — Catalog scope:** Are the herb/supplement counts launch requirements or long-term targets? Do supplement counts mean ingredients or branded products, and which are the initial priorities?
19. **Q19 — Data processing:** Are cloud AI services permitted? Are there required hosting regions, prohibited providers, retention restrictions, or client privacy commitments? Exact vendor terms will be checked before integration.
20. **Q20 — Data lifetime:** How long should photos, voice, lab documents, and health records remain? What export, deletion, consent withdrawal, and practitioner-sharing behavior is expected?
21. **Q21 — Resources and rights:** Who owns supplied content/data, and what permission exists to store, display, redistribute, or use it for evaluation? Any training/research use needs a separate decision.
22. **Q22 — Business model:** Free, subscription, professional licensing, or a staged experiment? Which capabilities are paid, and which platform/payment constraints apply?
23. **Q23 — Operations:** How many initial users and daily analyses are expected? Who handles content corrections, support, clinical questions, and administrative access?

### Resolve before pilot and launch

24. **Q24 — Evaluation:** Who can provide representative users and permissioned examples? Which agreed thresholds for calculation correctness, correction effort, error, latency, and cost decide whether to proceed?
25. **Q25 — Review and sign-off:** Who accepts the product, approves nutrition content and intended claims, and owns market-specific privacy/regulatory review where applicable?
   Answer/status: A certified nutritionist/dietitian will verify/sign off on rules, recommendations and warnings. The reviewer approves each clinical plan/warning before user access. Named access, availability, product sign-off and market-specific responsibilities remain to be assigned.
26. **Q26 — Release:** Is the first external release a demonstration, private pilot, or public product? Who owns the hosting, app-store/payment accounts, and ongoing maintenance?
27. **Q27 — GitHub target and access:** Which repository URL or account/repository name should be used, and how will authenticated access be established? If creating a repository, private visibility is proposed until specified otherwise.
   Answer/status: Resolved. Supplied origin configured; owner authenticated as AbdelrhmanAbuAmashah; identity and push permission verified; initial planning history pushed through 44015a0. Do not re-ask repository/account/access setup.
28. **Q28 — Clinical output approval:** Must the nutritionist approve each clinical plan/warning before users see it, or only rules and sampled outputs?
   Answer/status: Approve each clinical plan/warning before users see it. Explicitly resolved by owner; implement individual approval and publication checks.

## Keeping this report current

- Check a task only when the deliverable exists and its required verification is recorded.
- For each implementation update, record the milestone, changed files, acceptance evidence, exact test commands/results, limitations, and next task. Label mock and live integrations explicitly.
- Record each owner answer against Q and D IDs with its date. Preserve unresolved or changed decisions and their scope/cost effects.
- Commit/push meaningful verified increments and planning updates on dedicated feature branches, then open PRs to `main` with exact local test evidence. Merge only through the normal protected path after current checks pass, the branch is up to date and conversations are resolved. Record the branch, PR, checked revision and merge state; keep credentials and real health records out of Git. See [workflow](docs/github-workflow.md).
- Register new resources before applying affected requirements. Preserve topic proposals even when deferred.
- Recount P1–P6 only when a phase's exit criteria are satisfied. Split phases into smaller tasks as implementation becomes concrete.

### Update log

| Date | Change | Evidence / phase impact |
| --- | --- | --- |
| 22 Oct 2026 | Initial review and report created from the two supplied documents | Both documents fully read; inventory contains no application implementation. Discovery review tasks complete; 0/6 delivery phases complete. |
| 22 Oct 2026 | Proposed MVP scope/resources and development start plan added; USDA reference checks registered | Documentation and limited source review only. Audience/platform/scope answers and acceptance remain pending; 0/6 delivery phases complete. |
| 22 Oct 2026 | Owner strategic inputs recorded; MVP updated for bilingual web, two markets, traceable manual data, automatic restrictions, daily suggestions and GitHub workflow | SRC-06–SRC-10 and NEW-01–NEW-04 added; N1–N7 planned. GitHub checks show no usable local repository/authentication; no commit/push or implementation. 0/6 delivery phases complete. |
| 22 Oct 2026 | Repository target, nutritionist availability and individual clinical approval recorded; source roles and review-queue plan added | SRC-11–SRC-16, D-12, NEW-05, README and ignore rules prepared. Authentication works outside the sandbox; repo public/empty and neither configured account has push permission. Local baseline preparation continues; no application features implemented. 0/6 delivery phases complete. |
| 22 Oct 2026 | Local planning baseline committed | `git init -b main`, supplied origin configured, eight explicit files staged, staged summary inspected and commit `d07c310` created. Initial post-commit status was clean. Remote sync awaits Write permission; no app tests exist. 0/6 delivery phases complete. |
| 22 Oct 2026 | Local status commit and owner-account authentication setup | `1455799` records the local baseline. Exact account AbdelrhmanAbuAmashah was requested; credential check found it unauthenticated, so GitHub device sign-in was started. No remote push has occurred. |
| 22 Oct 2026 | Owner authentication and initial GitHub push complete | Device sign-in succeeded as AbdelrhmanAbuAmashah; identity and push/admin permission verified; `git push --set-upstream origin main` published the history through 44015a0 and configured upstream tracking. N1 complete, N2–N7 open; 0/6 delivery phases complete. |
| 22 Oct 2026 | Owner-approved logging foundation implemented and verified | Next.js/FastAPI/PostgreSQL, 28-table Alembic migration, generated environment/setup, JWT/Argon2id/CSRF/origin/ownership controls, bilingual profile/diary/dashboard, 19 original USDA records, three illustrative recipes, export/deletion and future clinical/recipe/AI boundaries. `bash scripts/test.sh` passes: no migration drift, Ruff passes, 36 API tests and four EN/AR desktop/mobile browser journeys pass. Production format/type/build and isolated backup/restore also pass. N1–N6 complete; N7 publication pending in this checkpoint. |
| 22 Oct 2026 | Foundation published; N7 complete | Owner-authenticated push published ae28042266bf7966c428c0b26a16cefb144f80fd; remote reference exactly matches. GitHub Actions run 39713405773 reports completed/success. N1–N7: 7/7 complete; one working product milestone achieved. Four owned synthetic accounts from the initial failed browser run were removed through authenticated API deletion. Core app services remain running locally; no external production deployment or clinical activation. |
| 22 Oct 2026 | Feature-branch workflow adopted following owner directive | W1–W4 configuration/publication complete on feature/github-feature-branch-workflow: persistent instructions/PR template, mandatory PR CI without path skips, full local verification, applied main protection and legacy Nutrition-project PR #1 with test evidence. That repository and its hosted PR page were subsequently deleted under SRC-21. Future merges require successful current checks through the normal protected path. |
| 22 Oct 2026 | Owner-only repository cutover following explicit correction | Created a single-parentless root 2bc9e56 authored/committed by AbdelrhmanAbuAmashah, verified an identical tracked-file tree, and published it to fresh public Nutrition-Project-New. The history-bearing copy was renamed Nutrition-Project-New-history-backup; original Nutrition-project remains. Active local Git metadata was replaced with the clean metadata after backing up the prior Git directory. Environment, app data, source files and prior backups were preserved. Required PR/check protections reapplied. Active-link/documentation changes use chore/owner-only-repository. |
| 22 Oct 2026 | Legacy remote repositories deleted at the owner's explicit request | SRC-21 supersedes remote backup retention: Nutrition-project (ID 1429079145) and Nutrition-Project-New-history-backup (ID 1429243261) returned HTTP 204 on deletion and HTTP 404 on authenticated follow-up. Account inventory confirms only Nutrition-Project-New remains for this project, with three unrelated repositories intact. Active origin, main SHA, owner-only contributors and strict PR/check protections verified. Ignored local Git backup retained. This documentation update uses chore/repository-cleanup-report and requires fresh PR CI. Foundation count remains 7/7 tasks and one product milestone. |

## First milestone and immediate next step

**First working milestone achieved: the bilingual, source-backed manual logging foundation (7/7 tasks).** Run `bash scripts/setup.sh`, open http://localhost:3000 and create an account. The [README](README.md) explains setup; the [verification log](docs/verification.md) records results/limits, and the [operations guide](docs/operations.md) covers restart, backups and deployment dependencies. N7 records the verified published code checkpoint and successful CI run.

**Next milestone: target-aware daily suggestions with individual nutritionist approval of every clinical plan/warning.** The [next-milestone TODO plan](docs/next-milestone.md) lists S1–S7, exit evidence and six inputs needed before affected clinical/provider work. Preserve confirmed decisions; do not repeat GitHub/language/market/approval questions.

Foundation evidence: known calculations match; source provenance and historical inputs remain preserved; missing nutrients stay unavailable; confirmed-only totals and concurrent duplicate protection pass; timezone/access checks pass; all four bilingual viewport journeys pass; restriction conflicts/unknowns fail candidate eligibility. Recipe Memory editing, photo assistance, live AI/clinical review, email recovery and production deployment remain open. The npm advisory service returned HTTP 503, so a clean vulnerability scan is not claimed. Complete the deployment and clinical dependencies before any public clinical pilot.
