# Nutrition app: evidence and clinical approval workflow

Recorded 22 October 2026 from the owner's nutrition-expert integration decision and follow-up approval answer. Status: agreed workflow and proposed implementation plan; no clinical module, reference corpus, AI integration or reviewer interface is implemented yet.

## Owner decisions

- Repository: [AbdelrhmanAbuAmashah/Nutrition-project](https://github.com/AbdelrhmanAbuAmashah/Nutrition-project), with the supplied HTTPS Git URL used for synchronization.
- A certified nutritionist/dietitian is on the project and will review and sign off on rules, recommendations and warnings. Availability is owner-confirmed; reviewer identity, access assignment, coverage and credentials have not been independently verified in this session.
- AI prepares evidence-grounded personalized meal suggestions, clinical warning drafts and proposed rules first. The nutritionist verifies, edits, approves or rejects them rather than authoring every draft from scratch.
- **Each AI-generated clinical plan and clinical warning requires nutritionist approval before the user can see it.** This was explicitly confirmed in the follow-up answer. Rule-version approval alone does not publish an individual clinical output.
- Connect to verified nutrition data and suitable guidelines. Diabetes, hypertension and food allergies are initial areas for module definition; diabetes types, supported populations and precise therapeutic claims remain to be agreed with the reviewer.

## What each source layer supplies

| Layer | Starting references checked on 22 Oct 2026 | Current review limits / next action |
| --- | --- | --- |
| Food composition | [USDA FoodData Central documentation](https://fdc.nal.usda.gov/data-documentation/) and the API reference already registered as SRC-04 | Food data types and provenance support deterministic nutrient calculation. No live API integration, target-market coverage evaluation or production seed has been completed. |
| General nutrition principles | [WHO healthy diet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet); [FAO/WHO joint statement, 2024](https://www.who.int/publications/i/item/9789240101876) | WHO fact sheet read; joint statement publication overview read, not the full 22-page publication. Select permitted passages/versions with the reviewer before runtime use. |
| Diabetes module preparation | [NIDDK: Healthy Living with Diabetes](https://www.niddk.nih.gov/health-information/diabetes/overview/healthy-living-with-diabetes) | Meal-planning context and individualization sections read. This is an educational starting reference, not an approved complete diabetes protocol. Reviewer selects exact condition-specific clinical guidelines and scope. |
| Hypertension module preparation | [NHLBI: DASH eating plan](https://www.nhlbi.nih.gov/health/dash-eating-plan); [Saudi MOH hypertension nutrition](https://www.moh.gov.sa/en/healthawareness/educationalcontent/food-and-nutrition/pages/003.aspx) | Relevant pages read for scope and local educational context. Numeric targets, exclusions, combined-condition conflicts and user wording remain unapproved. |
| Allergens and ingredient coverage | [FDA food allergies](https://www.fda.gov/food/nutrition-food-labeling-and-critical-foods/food-allergies), previously registered as SRC-09 | Supports ingredient/cross-contact limitations. A reviewed ingredient/alias map and applicable local sources are still needed; do not treat a single jurisdiction's major-allergen list as complete coverage. |

The food database and clinical knowledge layer have different jobs. Food records supply composition inputs. A guideline or reviewed rule supplies population/context-dependent guidance. Connecting sources does not by itself establish clinical accuracy; supported claims, calculation checks, evaluation and nutritionist sign-off must be traceable.

No source text has been copied into a runtime vector database, model training set or production application. Register exact version/date, source location, rights for the intended use, population, limitations, reviewer, approval and update status before ingestion or rule activation. Public accessibility alone is not a redistribution or commercial-use permission. Treat retrieved material as reference data and prevent it from changing authorization or tool behavior.

## Workflow to implement

1. **Reference intake:** register and verify the exact source, relevant sections, version, reuse rights and intended module. The nutritionist accepts the source for the stated use.
2. **AI-prepared rule draft:** extract a proposed structured rule with citations, applicability, required inputs, missing-data behavior and potential conflicts. Mark it draft. The nutritionist edits/approves a rule version before it becomes active for user-facing clinical workflows.
3. **AI-prepared personalized draft:** read the user's confirmed profile and target provenance, retrieve approved relevant evidence and eligible source-backed food/recipe candidates, then draft the plan and any clinical warnings. Include source references, ingredient IDs, portions, nutrient calculation inputs, unresolved questions, active rule versions and known coverage limits.
4. **Automated checks:** recalculate nutrients in code; enforce allergies and approved hard constraints; reject invalid IDs, unsupported claims/references, missing required evidence, incomplete ingredients or unresolved rule conflicts. Failed checks block publication and return the issue for correction/review. An automated pass is not clinical approval.
5. **Nutritionist review queue:** show the exact clinical draft, supporting evidence and required confirmed context. The reviewer can approve, edit, reject or request more information. Edits rerun automated checks and require approval of the resulting version.
6. **Approved publication:** publish only the reviewed version after verifying that its user/profile/targets/rules/ingredients/source versions still match. Record reviewer identity, timestamps, version, decision and relevant notes. Until then, the user can see a pending status, but not draft clinical advice in screens, APIs, notifications, exports or AI chat.
7. **Changes and follow-up:** relevant changes invalidate affected future recommendations and require regeneration/review. Preserve approved historical outputs and actual meal records with their original provenance. Retired sources/rules cannot silently remain active.

Proposed clinical output lifecycle:

```text
draft → checks passed → awaiting nutritionist review → approved → published
       ↘ blocked / needs information        ↘ rejected / edited → checks again
```

Automatic exclusion of known incompatible ingredients continues before and after AI generation and does not wait for a reviewer's availability. It cannot be overridden by the model to satisfy a nutrient target. New AI-generated clinical warning text remains behind the individual approval gate. Existing restriction state and any fixed user-facing conflict wording must follow the accepted, reviewed interface policy.

The review queue is a focused MVP capability, separate from a full practitioner portal. Grant reviewers only assigned, consented context needed for a review. Keep audit metadata minimal; do not put patient data, generated clinical drafts or real health profiles into GitHub.

## Next features and acceptance checklist

- [ ] Source register and exact evidence/citation links, with permissions and review status.
- [ ] Versioned rules with draft/approved/retired states and explicit applicability.
- [ ] AI draft schema for meal plans and warnings, including confirmed input versions and nutrient provenance.
- [ ] Backend calculation, allergy, missing-data, citation and combined-condition checks.
- [ ] Minimal nutritionist queue with review/edit/approve/reject/request-information actions.
- [ ] User-facing pending/approved states and server-side publication authorization.
- [ ] Tests that unapproved or stale clinical outputs cannot reach users through any supported delivery path.
- [ ] Tests that a reviewer edit reruns checks, approval is tied to an exact version and profile changes require revalidation.
- [ ] Reviewer-accepted cases for the initial allergy/diabetes/hypertension modules, including conflicting restrictions and insufficient evidence. Modules remain inactive until their scope/rules/evaluation are accepted.

Still needed before affected clinical activation: diabetes subtype/population and module boundaries; reviewer's named access and availability; selected guideline versions and permissions; target-setting rules; initial ingredient mapping/recipe set; and review turnaround expectations. These do not prevent GitHub setup or the bilingual source-backed manual logging foundation.

## Immediate milestone

The GitHub planning baseline is published. Next deliver the first bilingual manual logging increment and restriction foundation. Design evidence/rule/clinical-draft records alongside it. Implement and verify the nutritionist approval queue before any AI-generated clinical plan or warning is published to a user.
