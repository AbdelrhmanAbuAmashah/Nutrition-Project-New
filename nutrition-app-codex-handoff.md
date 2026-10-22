# Nutrition application — complete Codex handoff

Prepared 9 October 2026 from the supplied nutrition-app-project-plan.md, originally dated 9 September 2026.

This is a self-contained development handoff. The source plan is a preliminary proposal, not an approved specification or evidence of an existing implementation. The requirements below translate its intent into actionable work. Proposed technical details and unresolved choices are explicitly identified.

## 1. Instructions to the receiving Codex agent

Act as the technical lead and implementation partner for this project. Read this entire document and all supplied project resources before making architectural decisions. Do not assume access to the previous conversation, a repository, the earlier interactive concept, credentials, or files that have not actually been provided.

The owner will provide MORE RESOURCES: client messages, documents, designs, sample data, research, links, repository files, and possibly changes to the scope. This document is a living baseline. Follow the intake process in section 12 whenever new material arrives.

The initial task is discovery and planning. Inspect any supplied repository and its applicable instructions, identify what already exists, organize requirements, document gaps, and propose the first implementation milestone. Start coding when the owner requests implementation. Do not interpret this handoff as authorization to buy services, deploy publicly, or process real patient records.

When implementation is requested, complete the authorized milestone with meaningful verification rather than returning only advice. Use reasonable, documented assumptions for reversible decisions. Ask concise questions only where missing information materially blocks correct implementation or changes the agreed scope.

Work with the existing repository if one is supplied. Preserve unrelated changes and follow its conventions. Never claim that a feature, integration, test, deployment, or clinical review is complete without evidence.

## 2. Product purpose and current decisions

The client wants a nutrition application where users can photograph a meal, estimate calories and nutrients, retain their meal history, record medication and allergy history, and receive useful support for healthier habits.

The owner also wants a distinctive feature, a realistic delivery plan, a viable subscription model, and a preference for free or low-cost development components.

Treat the following as established intent:

- Photo-assisted meal logging and nutrition calculation.
- Relevant health history, including current/past medicines and food/drug allergies.
- Personalization using user-confirmed information.
- Additional resources and requirements will arrive.
- Cost awareness, practical AI recommendations, and commercial differentiation.

Treat the following as PROPOSED, pending owner/client acceptance:

- Adult general-wellness scope for the initial release.
- Personal Recipe Memory as the flagship differentiator.
- React Native client, FastAPI backend, PostgreSQL database.
- One launch market and primary language.
- Deferring broad medication-food interaction advice to a separately governed release.
- All time estimates, subscription prices, model choices, operating budgets, and pilot thresholds.

Do not turn a proposal into a confirmed business decision silently.

## 3. Flagship feature: Personal Recipe Memory

Remember how this user or household prepares a particular meal. Store confirmed ingredients, amounts, cooking method, cooked yield, serving information, and recipe versions.

Example:

1. A user logs homemade maqluba.
2. The app suggests a dish match and asks the user to confirm the ingredients and quantities.
3. The user provides recipe details, including oil and portion information.
4. The app saves a personal recipe version.
5. On a later occasion, the user says, “Same recipe, but less rice.”
6. The app retrieves the recipe, confirms what changed, and recalculates that serving.
7. The app explains which changed inputs affected the estimate.

The proposed distinction is the combination of personal recipe evidence, versioned memory, targeted clarification, and transparent recalculation. Saved recipes, photo logging, and voice logging individually already exist in competing products. Global novelty has NOT been established. Never claim “nobody has built this” or “first ever” without appropriate investigation.

Clarification requirements:

- Identify unresolved ingredients or quantities that meaningfully affect the estimate.
- Start with transparent sensitivity rules: prioritize the largest answerable source of uncertainty while considering user effort.
- Normally ask at most one or two questions, with “I don't know,” correction, and manual-entry alternatives.
- Ask whether a saved recipe changed before reusing its assumptions.
- Do not infer hidden oil or allergens as confirmed facts from an image.
- Preserve prior recipe versions and historical meal calculations.
- A new recipe version must not silently recalculate past meals.

“Learning” in version one means storing and retrieving confirmed facts. It does not mean continuously retraining a foundation model.

## 4. Functional requirements

### FR-01 Accounts, onboarding, and preferences

Support authentication, profile editing, goals, preferred units, relevant age/height/weight/activity inputs, food preferences, and granular consent. Final required fields depend on the approved goal-setting method. Do not require a complete lifetime medical history before allowing meal logging.

Support export and account deletion. Separate consent for optional research/training or practitioner sharing from normal service use.

### FR-02 Progressive health timeline

Allow users to add and edit current and historical medication, allergy, and intolerance records. Preserve unknown fields rather than guessing.

Medication fields: original reported name, normalized ingredient/identifier when verified, dose, unit, route, frequency, active/past status, start/end dates if known, confirmation status, and record provenance.

Allergy fields: food/drug category, substance, reported reaction, severity if known, date if known, self-reported/professionally confirmed status, and provenance. Keep allergies, intolerances, and dislikes distinct.

AI extraction may create a draft. The user must confirm before the draft becomes an active health fact. Do not infer medication equivalence or drug-allergy cross-reactivity from similar names.

### FR-03 Meal capture and review

Support manual food search, text entry, photo upload/capture, common barcode lookup, and short voice dictation. Allow corrections to suggested foods, cooking method, quantities, serving sizes, and consumed fraction.

Separate drafts from confirmed meals. Handle upload failures, unsupported dishes, incomplete identification, duplicates, and unavailable providers. Manual logging must remain usable without an AI provider.

Suggested state model, to adapt to the repository: draft → analyzing → needs review → confirmed. Provide explicit failed/cancelled handling. A repeated save request must not create duplicate meals.

### FR-04 Deterministic nutrition calculation

For each food item:

nutrient contribution = consumed grams × nutrient amount per 100 grams ÷ 100.

Sum contributions in server-side calculation code. Do not ask an LLM to invent nutrient values or perform the authoritative arithmetic.

Preserve food identifier, source/version, units, raw/cooked state, ingredient quantity, serving assumption, and calculation version.

For a sufficiently uniform recipe, allocate batch nutrition using cooked yield and consumed serving mass. For a mixed plate with unequal proportions, handle components separately. Include oil, sauces, edible portions, and leftovers when relevant.

Report missing nutrient values as unavailable, not zero. Avoid double-counting cooking oil already included in a food record. Define rounding consistently.

### FR-05 Evidence and uncertainty

Distinguish photo-estimated portions, user-confirmed recipe/package information, and weighed quantities. User confirmation is not automatically a laboratory measurement.

Do not promise exact weight from an ordinary photo. If presenting a range, record how it was derived. Do not label heuristic bounds as a calibrated confidence interval.

The earlier interactive demonstration used hypothetical inputs. Its numbers are not product benchmarks or validated AI performance.

### FR-06 Personal recipe management

Create, name, review, edit through new versions, archive, and reuse personal recipes. Match a new meal to candidate personal recipes, with user confirmation when ambiguous.

Track confirmed information separately from model suggestions. Retain the relationship between a meal and the exact recipe version used.

### FR-07 Ingredient checks

Compare known, confirmed ingredient information against recorded food allergies. Present relevant ingredient warnings and an explicit unknown/verify state when information is insufficient.

A photo cannot establish absence of allergens or cross-contact. Never display an unconditional “safe to eat” result based on image recognition. Do not allow generated advice to override recorded restrictions.

Medication history is included in the proposed first release. Broad medication-food or drug-drug advice is deferred unless explicitly added with clinical data licensing, professional review, permitted provider use, and revised scope.

### FR-08 Voice entry

Start with push-to-talk meal descriptions and corrections. Display the transcript and extracted quantities for confirmation. Test food names, units, accents/dialects, noise, and ambiguous numbers.

Example: “Two eggs, one slice of bread, and tea with one teaspoon of sugar.”

Delete or retain recordings according to the approved retention policy. Spoken replies and real-time conversation are later enhancements.

### FR-09 History and progress

Show confirmed meal history, daily nutrient totals, weekly summaries, and user-entered weight trends. Handle timezone boundaries and unit conversion consistently.

Provide reminders with user controls. Explain patterns without unsupported causation or guaranteed health outcomes. Symptom logging, if added, records observations and does not diagnose allergies or disease.

### FR-10 Guidance and personalization

Use confirmed preferences, recipes, and relevant approved context. For educational responses, retrieve approved reference material and retain citations/source versions.

Define the professional-review route for needs outside the approved wellness scope, including minors, pregnancy, complex conditions, and eating-disorder risk. Goal-setting and recommendation rules require appropriate nutrition review.

### FR-11 Administration and subscriptions

Provide food-catalog correction tools, approved-content management, issue reports, basic monitoring, subscription entitlements, and usage limits.

Restrict administrative access. Administrative privileges must not automatically grant unrestricted access to health records.

Choose payment integration after platform/market decisions. Verify payment callbacks and handle duplicate events, failed payments, cancellation, and expired entitlements.

### FR-12 User data controls

Provide appropriate export, deletion, access controls, retention settings, and consent withdrawal behavior. Explain how deletion affects backups and third-party processing.

Basic safety information, access to recorded restrictions, and export/deletion must not depend on an active premium subscription.

## 5. Later-stage backlog

Keep these distinct from committed first-release requirements:

- Meal planning around culture, budget, cooking time, preferences, and reviewed dietary constraints.
- Grocery lists and recipe substitutions.
- Regional recipes, local brands, Arabic localization, and dialect support where relevant.
- Kitchen-scale integration and richer batch-cooking support.
- Optional symptom journal and practitioner-ready reports.
- Dietitian portal with explicit sharing permissions.
- Family accounts and controlled household recipe sharing.
- Wearable integrations.
- Restaurant/supermarket partnerships.
- Reviewed medical-document import.
- Professionally governed medication interaction features.
- Natural spoken replies and real-time voice.
- Specialist model training or fine-tuning, only after a measured need.

## 6. Proposed architecture and data contracts

Default candidate: React Native for a cross-platform mobile client, FastAPI for the API, PostgreSQL for structured records, private object storage for media, and a small web administration interface. A responsive web-first implementation is an alternative if the owner chooses it. Do not build both consumer frontends by default.

Prefer a modular application and controlled workflows. Add workers/queues when justified by inference or media processing. Do not introduce a complex microservice or multi-agent design without a concrete need.

Proposed entities:

| Entity | Key information |
| --- | --- |
| User/Profile | Identity reference, preferences, goals, units, timezone |
| Consent | Purpose, version, grant/withdrawal timestamps |
| MedicationRecord | Structured medicine fields, status, verification |
| Allergy/IntoleranceRecord | Substance, type, reaction, status, provenance |
| FoodRecord | External/internal ID, source version, nutrient basis, units |
| Recipe/RecipeVersion | Ingredients, quantities, method, yield, confirmation |
| Meal/MealItem | Timestamp, portion, recipe version, confirmed nutrient snapshot |
| AnalysisRun | Provider/model version, structured draft, errors, latency/cost |
| MediaAsset | Private storage reference, owner, retention/deletion metadata |
| ReferenceResource | Source, version, permission/licensing status, review state |
| Subscription/Usage | Entitlements, provider references, usage counters |
| AuditEvent | Actor, operation, time, affected record; avoid sensitive payloads |

Specify schemas before integration. Model output should include suggested food matches, preparation state, quantity/unit or unknown, unresolved assumptions, evidence links, and review status. Validate it before using it. Model-reported confidence is not calibrated probability.

Define API contracts for profile/health history, food search, media upload, analysis jobs, draft review/confirmation, recipes, history, export/deletion, subscriptions, and administration. Match the repository's conventions; endpoint names here are deliberately not prescribed.

Record original model suggestions independently from user-confirmed facts. Store enough calculation inputs to reproduce historical results.

## 7. AI and data candidates

These candidates come from the September plan. Their current availability, licenses, versions, pricing, limits, and permitted uses were NOT reverified for this October handoff. Verify official documentation before implementation.

| Task | Candidate | Selection rule |
| --- | --- | --- |
| Vision | Qwen3-VL-8B-Instruct or an eligible hosted model | Benchmark actual target dishes and device images |
| Hosted extraction | Gemini Flash family; earlier plan named 3.5 Flash-Lite | Verify current model and terms; do not silently assume suitability for medical use |
| Speech-to-text | Whisper through faster-whisper | Compare dialect, quantity, noise accuracy, latency, and compute |
| Printed label OCR | PaddleOCR | Validate serving sizes, decimals, units, and incomplete labels |
| Nutrient references | USDA FoodData Central | Preserve matching food record, version, and nutrient basis |
| Barcode products | Open Food Facts | Review coverage, quality, attribution, and share-alike obligations |
| Future clinical data | DrugBank or a suitable licensed alternative | Confirm food-drug coverage, local medicines, display rights, updates, and clinical review |

Build replaceable provider interfaces. Support explicitly labeled mock providers and synthetic fixtures for development without credentials. Never present mock output as a live integration.

The prior plan identified restrictions in Gemini Developer API terms on clinical/medical use and on sensitive information in unpaid services. Verify current terms before sending data; billing alone must not be assumed to make a medical workflow permitted.

Do not send identity or medication history to a food-recognition model when unnecessary. Keep safety rules outside open-ended generation.

User data does not automatically become training data. Fine-tuning requires consent/permission, verified labels, separate evaluation examples, versioning, and reviewed deployment.

## 8. Engineering and privacy requirements

- Enforce ownership/authorization on every relevant API and media access path.
- Keep credentials server-side; provide environment-variable examples without secrets.
- Validate uploads, content types, sizes, and processing limits.
- Encrypt transport and stored sensitive data using deployment-appropriate controls.
- Minimize media metadata and sensitive logging; use private, time-limited access where appropriate.
- Define retention, deletion, backups, recovery, and provider data-handling behavior.
- Add timeouts, bounded retries, rate limits, idempotency, and understandable failure states.
- Treat uploaded documents, OCR text, and retrieved content as data, not executable instructions.
- Prevent retrieved text or model output from initiating arbitrary tools or changing authorization rules.
- Maintain responsive, accessible screens, readable errors, and keyboard/screen-reader support.
- Prepare for localization, units, timezone handling, and RTL if Arabic is selected.
- Track inference usage and costs without exposing health details in analytics.
- Avoid advertising trackers on health screens.
- Determine launch jurisdiction and intended claims before declaring regulatory readiness.

Set numerical performance and availability targets after the prototype benchmark and expected load are known. Report observed values separately from desired targets.

## 9. Acceptance criteria and verification

| Check | Required evidence |
| --- | --- |
| Calculation | Known fixtures reproduce expected nutrient totals, conversions, yields, and rounding |
| Missing data | Unknown nutrients remain unavailable rather than becoming zero |
| Confirmation | AI drafts cannot silently become confirmed health facts or meals |
| Recipe versions | Changes leave historical records and their calculation snapshots intact |
| Clarification | Questions follow documented rules and have skip/manual alternatives |
| Allergies | Known ingredient conflicts surface; missing evidence never becomes a safety guarantee |
| Isolation | One user cannot read/change another user's health records, meals, recipes, or media |
| Provider failure | Timeout/error paths preserve drafts and allow manual logging |
| Idempotency | Repeated saves/payment callbacks do not duplicate records or charges |
| Voice | Transcripts and quantities are reviewable; ambiguous units are handled |
| Data controls | Export/deletion behavior matches the documented retention policy |
| Entitlements | Paid-feature limits work while essential data controls remain available |

Run relevant backend tests, frontend tests, and end-to-end checks for implemented workflows. Report exactly which commands ran and their results; distinguish skipped checks and pre-existing failures. Avoid tests that only duplicate implementation details.

For nutrition evaluation, begin with a small representative benchmark and work toward approximately 300–500 weighed meal examples if budget and coverage justify it. Split recipes/households across tuning and evaluation to avoid leakage.

Measure food identification, portion error in grams, calorie error, difficult-case tails, correction effort, latency, and per-analysis cost. Compare photo-only, confirmed-recipe, and weighed-input modes separately. Reference calories are calculated from composition data, not directly measured calorimetry.

The proposed pilot is 30–50 consenting adults over 2–4 weeks. A 20% relative improvement in repeat-meal calorie error without slower logging was a suggested experiment threshold, not an achieved result or universal release standard.

## 10. Phases and commercial assumptions

Original planning estimate: 16–20 weeks with two full-time engineers plus part-time design, QA, and dietitian input. It assumes a focused first release, one main language/market, and no broad clinical interaction advice or custom model training.

| Phase | Estimated window | Outcome |
| --- | --- | --- |
| Discovery | Weeks 1–2 | Resources, scope, designs, acceptance plan, decisions |
| Feasibility | Weeks 3–4 | Thin prototype and measured model/cost/error comparison |
| Core alpha | Weeks 5–8 | Accounts, logging, calculation, health records, history |
| Differentiation | Weeks 9–12 | Recipe memory, clarification, voice, barcodes, subscriptions |
| Pilot | Weeks 13–16 | Evaluation, security/privacy checks, fixes |
| Launch preparation | Weeks 17–20 | Contingency, store review, staged rollout, handover |

A comparable solo effort was estimated at 6–9 months. Additional languages/coverage and later features change the schedule. Re-estimate once actual team, repository, data, and clinical scope are known.

Proposed business model: free basic logging plus limited photo use; consumer Plus at $7–10/month; a later practitioner offering at $50–150/month depending on volume. These are pricing experiments, not approved prices.

The prior plan's technical operating allowance was $250–800/month for 1,000 active users and about 60,000 monthly photo analyses. It excludes staff, clinical datasets/review, dedicated GPUs, support, fees, taxes, marketing, and other launch expenses. Earlier token-rate calculations are historical illustrations; obtain current rates and measure real usage before quoting.

Prefer free/open components where suitable, while accounting for compute and operations. Evaluate paid services by measurable benefit. Do not purchase hardware or subscriptions without owner authorization.

Track activation, repeated-recipe reuse, correction effort, retained users, paid conversion, cancellation, support burden, and cost per retained paying customer.

## 11. Initial resource register

The project owner may provide additional or newer sources. Treat this list as starting references, not proof that every page has been reviewed in the receiving session.

| Resource | Intended use |
| --- | --- |
| nutrition-app-project-plan.md | Original proposal; read if supplied and reconcile with this handoff |
| https://fdc.nal.usda.gov/api-guide/ | Nutrient API and licensing |
| https://fdc.nal.usda.gov/download-datasets | Downloadable nutrition data |
| https://openfoodfacts.github.io/openfoodfacts-server/api/ | Barcode data, usage, and licensing |
| https://arxiv.org/html/2103.03375v2 | Nutrition5k research; not an accuracy guarantee |
| https://github.com/google-research-datasets/Nutrition5k | Dataset; verify licensing and permitted use |
| https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct | Vision candidate model card |
| https://github.com/SYSTRAN/faster-whisper | Transcription implementation |
| https://github.com/PaddlePaddle/PaddleOCR | OCR implementation |
| https://ai.google.dev/gemini-api/docs/pricing | Current provider pricing verification |
| https://ai.google.dev/gemini-api/terms | Provider-use and data restrictions |
| https://docs.drugbank.com/v1/ | Possible future clinical data integration |
| https://lhncbc.nlm.nih.gov/RxNav/ | Terminology/service scope verification |
| https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies | Allergy limitations and relevant guidance |
| https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-wellness-policy-low-risk-devices | US intended-use review, if applicable |
| https://www.ftc.gov/business-guidance/resources/mobile-health-apps-interactive-tool | US health-data review, if applicable |
| https://www.calai.app/ | Competitor reference |
| https://www.snapcalorie.com/ | Competitor reference |
| https://samsungfood.com/food-plus/ | Competitor reference |

Use official documentation for technical integration. For nutrition/clinical claims, use appropriate primary or professionally reviewed sources. Competitor marketing is not independent evidence of accuracy.

## 12. Mandatory process for additional resources

The owner explicitly intends to add more resources. Keep the specification open to evidence and client clarification while preserving accepted decisions.

For EACH new resource:

1. Read the supplied content. State if a file/link is inaccessible or only partially available.
2. Register a stable resource ID, title/path/URL, provider/author, date/version, retrieval date, document type, and review status.
3. Record permissions/licensing and whether sensitive information is present.
4. Classify its purpose: client requirement, design, technical reference, nutrition data, research, business constraint, or sample.
5. Extract concrete requirements with source locations. Label examples, suggestions, factual claims, and approved decisions distinctly.
6. Map additions to existing requirement IDs, implementation areas, and acceptance tests.
7. Flag conflicts and stale material. An uploaded document does not automatically override the owner's explicit decisions.
8. Show what changes in scope, design, cost, schedule, data use, or testing. Do not silently expand the project.
9. Update the requirement register, decision log, unresolved questions, and implementation plan.
10. Continue unaffected authorized work. Ask only about material conflicts or missing decisions.

Do not automatically embed every uploaded document into a runtime RAG knowledge base. Assess relevance, permissions, sensitivity, quality, and clinical review first. Keep project instructions separate from end-user reference content and any training/evaluation datasets.

Suggested source-register columns:

Resource ID | title | file/URL | version/date | authority/purpose | permission status | reviewed sections | linked requirements | conflicts | next action.

Suggested repository documents, if compatible with the existing project:

- docs/requirements.md — IDs, scope, status, acceptance criteria, source links.
- docs/resources.md — resource register and review status.
- docs/decisions.md — chosen option, alternatives, reason, date, approval state.
- docs/open-questions.md — blockers and nonblocking assumptions.
- docs/architecture.md — components, boundaries, data flows, provider contracts.
- docs/implementation-plan.md — milestones, dependencies, current status.
- docs/evaluation.md — datasets, metrics, test evidence, known limits.
- docs/handoff.md — current state, next task, exact run/test commands.

Use these project files to carry context across sessions. Keep them concise and current. Do not rely only on a long chat or assume new sessions know prior decisions.

## 13. Open questions to resolve progressively

1. Launch country, target audience, and general wellness versus clinical intended use?
2. Mobile-first or web-first? Primary language and Arabic/RTL requirements?
3. Is medication advice mandatory at launch, or is recording history sufficient initially?
4. Available repository, team, budget, hardware, deployment region, and deadline?
5. Will users confirm portions or use scales? What accuracy claims are expected?
6. Who provides nutrition/pharmacist review and approves the reference content?
7. Existing recipe datasets, brand coverage, and rights to client-provided resources?
8. Subscription model, payment platform, expected user volume, and operating budget?
9. Media/health-data retention and model-provider restrictions?
10. Which distinctive feature does the client actually approve?

Do not present all questions as a mandatory upfront questionnaire. Prioritize the few that block the next authorized milestone and document reversible assumptions for the rest.

## 14. Requested first response from Codex

After reading the available resources:

1. Summarize the product and flagship feature in plain language.
2. Identify confirmed intent, proposed choices, deferred scope, and unknowns.
3. Report the actual repository/resource state; do not invent missing files or implementation.
4. Propose a phased technical plan with acceptance criteria and dependencies.
5. Recommend the smallest useful first implementation slice: manual food entry, deterministic nutrition calculation, confirmation, and history, followed by AI suggestions.
6. List only the material decisions needed next.
7. Explicitly acknowledge: “You will provide additional resources. I will read them, register their sources, reconcile requirements, and update the plan before applying affected changes.”

When reporting completed implementation, include what changed, why, verification actually performed, remaining limitations, and the next milestone. Distinguish mock integrations, live integrations, and unverified assumptions.
