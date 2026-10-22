# Next milestone: suggestions with individual clinical review

The first logging foundation exists. This is the proposed next feature increment; its clinical rules, provider and deployment choices are not activated by the foundation release.

## User outcome

A user requests meal ideas for an explicitly entered daily target. The API selects source-backed recipe candidates, applies confirmed restrictions, calculates portions in code, and validates the final candidates. AI can draft the explanation and proposed clinical plan/warning with exact evidence references. A clinical draft goes to an assigned nutritionist and reaches the user only after that exact version is approved. Edits to profile, recipe, rules or evidence require revalidation and, when affected, renewed approval.

## TODO and exit evidence

- [ ] **S1 — Define the clinical pilot boundary:** supported population/conditions, exact source editions/applicability, reviewed target approach, reviewer assignment and consent. Exit: the dietitian accepts a written rule/applicability checklist; unsupported cases remain explicit.
- [ ] **S2 — Expand and review candidate recipes:** source versions, confirmed ingredient identities, nested ingredients, quantities/yields and reviewed bilingual labels. Exit: representative Jordanian/Saudi candidates have traceable calculations; unknown/conflicting candidates fail eligibility.
- [ ] **S3 — Implement deterministic target matching:** compare eligible portions with accepted targets and preferences, preserve missing data and explain insufficient coverage. Exit: calculation/conflict/unknown/profile-change tests pass; goals never relax hard restrictions.
- [ ] **S4 — Add evidence-linked AI drafting:** structured identifiers and reference versions, bounded provider calls, schema validation, server-side recalculation and final restriction checks. Exit: unsupported model values/references fail validation; provider failure preserves the diary and clear retry status.
- [ ] **S5 — Build the nutritionist queue:** assigned reviewer authentication/authorization, consent-scoped access, evidence inspection, edit/approve/reject/request-information actions and audit trail. Exit: an unrelated reviewer cannot access a case or approve an output.
- [ ] **S6 — Enforce publication:** exact content/input/profile/rule/source version binding, stale-state handling and coverage of user APIs/UI/exports/notifications. Exit: no clinical draft without valid individual approval is published; approval of rules alone is insufficient.
- [ ] **S7 — Evaluate and checkpoint:** bilingual tests, dietitian-reviewed representative cases, rejection/failure scenarios, measured latency/cost and GitHub evidence. Exit: accepted evaluation thresholds and an explicitly scoped pilot decision.

## Inputs still needed before affected work

1. Who is the first supported population, and which precise condition/subtype modules and exclusions will the nutritionist review?
2. Which app account should receive reviewer access, and what review turnaround/capacity can the nutritionist provide? No credentials are needed in chat.
3. Should this next increment continue with user/professional-entered targets, or should the dietitian approve a particular target-calculation method and its applicability first?
4. Which initial local dishes/brands matter most? Are measured ingredient quantities and cooked yields available with permission?
5. What monthly service/AI spending ceiling and daily usage cap should apply? Which cloud providers/data regions are permitted?
6. What is the first external release: a private demonstration or a consenting private pilot? Who owns hosting, support and data-retention decisions?

Repository/account access, English/Arabic RTL, Jordan/Saudi markets, web-first delivery, nutritionist availability, AI-first drafting and individual clinical approval are already decided and do not need to be asked again. Unaffected design and test planning can proceed while these inputs are collected.

After this increment, the next feature candidates are Personal Recipe Memory (editable versioned personal ingredients/yields/portions) and photo-assisted drafts with confirmation. Voice, barcodes, subscriptions, broad interaction advice and a full practitioner portal remain separately scheduled.
