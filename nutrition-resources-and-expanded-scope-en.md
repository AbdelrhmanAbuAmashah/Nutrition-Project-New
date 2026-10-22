# Organizing App Ideas, Resources, and Specialized Nutrition Scope

**Date:** October 9, 2026  
**Type:** Resources and ideas addendum, to be handed to Codex alongside the project requirements file.  
**Primary source of ideas:** The project owner's list sent in this conversation.  
**Scope status:** Expansion proposals; not all of them are approved features for the first release.

The topics were kept, and duplicates were merged using a primary category plus additional tags. The USDA claims and the interaction examples received a focused review; no systematic review of the nutrition evidence for every condition in the list was carried out. A condition appearing here means it is within the product's area of interest. It does not mean that it is proven to be treatable through food, or that the app is ready to manage its treatment.

## 1. The Idea, Organized

The proposed app combines:

1. **Food logging and nutrient calculation:** photo, manual entry, barcode, or voice; then confirming the type and quantity.
2. **Personal profile:** goals, life stage, lifestyle, preferences, and dietary patterns.
3. **Health profile:** diagnosed or self-reported conditions, symptoms, allergies, medications, supplements, and herbs.
4. **Personal recipe memory:** saving confirmed recipes and their versions, and reducing repeated questions.
5. **Nutrition knowledge:** documented educational content, with education kept separate from treatment plans.
6. **Specialized clinical nutrition:** modules unlocked gradually once references and professional review are in place.
7. **Interactions:** documented checks for medications, supplements, herbs, and foods, with coverage limits shown.
8. **Follow-up:** a log of meals, symptoms, lab tests, and changes over time.

**Important for the data model:** A goal is not a disease, a diet is not a diagnosis, and a lab result is not an automatic diagnosis. We store these types as separate entities linked to the person.

## 2. USDA FoodData Central Review

**Proposed decision:** Adopt it as the primary source for food composition and nutrient calculation, with additional sources for local foods and products it does not cover.

| Statement provided | Assessment | More accurate wording for the app |
| --- | --- | --- |
| "The most accurate / the gold standard" | An absolute description this review does not establish | A trusted government source; the suitability of each food's record is evaluated |
| "Values per 100 grams" | A useful basis for calculation, provided record type and units are checked | We normalize values to a known basis and store the source's basis |
| "More than 150 nutrients" | We don't rely on the count as a coverage guarantee; we did not establish a uniform count per food | We show the nutrients actually available and distinguish missing from zero |
| "Lab data for many foods" | True for some data types; not for all records | We store the data type and the source of the values |
| "Completely free" | The data is available under CC0; running our app has costs | We separate the cost of data from hosting, maintenance, and AI |

USDA explains how its data types differ: Foundation Foods are based on analyses, Branded Foods on label information, and the sources of other types vary. So not all records should be treated as equivalent lab analyses. [R01]

### Integration Requirements

- Store the FDC ID, record type, food description, data version/date, units, and quantity basis.
- Match raw/cooked, drained/undrained, edible portion, and preparation method when available.
- Calculate nutrients in deterministic code: weight consumed × value per 100 g ÷ 100.
- Store estimated quantity separately from measured weight.
- If a local recipe isn't available: calculate it from its ingredients and cooked yield instead of silently picking a similar dish.
- USDA does not provide food weight from a photo, and it is not a database of treatment guidelines or a comprehensive interactions database.
- Keep the API key on the server; caching and bulk downloads are options depending on need and licensing.
- The currently published default limit is 1,000 requests/hour per IP address; re-verify at implementation time. [R02]

## 3. Primary Classification of Ideas

### A. Weight and Body Composition Goals

| Code | Topics |
| --- | --- |
| GOAL-WEIGHT | Weight loss; weight maintenance; weight gain |
| GOAL-COMPOSITION | Cutting; bulking; body recomposition |

These are goals the user chooses, not automatic instructions for a calorie deficit/surplus before determining whether they suit that user.

### B. Sports Nutrition

| Code | Topics |
| --- | --- |
| SPORT-PERFORMANCE | Muscle building; strength gain; improving athletic performance |
| SPORT-TIMING | Pre-workout nutrition; post-workout nutrition |
| SPORT-HYDRATION | Hydration |
| SPORT-SUPPLEMENTS | Sports supplements; linked to the supplements catalog and does not duplicate a separate database |

### C. Life Stage and Special Circumstances

| Category | Topics that appeared in the ideas |
| --- | --- |
| Infants | Infant nutrition needs; specialized track |
| Children and adolescents | Malnutrition; obesity; underweight; picky eating; constipation; food allergies; failure to thrive/growth faltering; iron deficiency; vitamin D deficiency |
| Adults | General nutrition goals, sports, lifestyle, and related conditions |
| Women's health | Pregnancy; breastfeeding; PCOS; endometriosis; PMS; menopause; iron deficiency during pregnancy |
| Older adults | Malnutrition; loss of appetite; loss of muscle mass; osteoporosis; swallowing difficulty; Alzheimer's; Parkinson's |

Life stage is stored separately from disease. Pregnancy and breastfeeding are additional special circumstances. The topic "iron deficiency during pregnancy" links to iron deficiency plus the pregnancy tag and doesn't need a duplicate disease record.

### D. Clinical Conditions and Symptoms

| Code / Area | Topics kept from the list |
| --- | --- |
| CLIN-GI — Digestive system | Irritable bowel syndrome (IBS); small intestinal bacterial overgrowth (SIBO); H. pylori; reflux (GERD); gastritis; stomach ulcer; constipation; diarrhea; celiac disease; non-celiac gluten sensitivity/intolerance when the diagnosis is clarified; lactose intolerance; Crohn's; ulcerative colitis; short bowel syndrome |
| CLIN-HEPATOBILIARY — Liver, gallbladder, and pancreas | Gallbladder disease; pancreatitis; fatty liver; hepatitis; cirrhosis |
| CLIN-ENDOCRINE — Diabetes and endocrine | Type 1 diabetes; type 2 diabetes; gestational diabetes; insulin resistance; prediabetes; polycystic ovary syndrome (PCOS); hypothyroidism; hyperthyroidism; adrenal disorders |
| CLIN-CARDIO — Heart and blood vessels | High blood pressure; high cholesterol; high triglycerides; coronary heart disease; heart failure; nutritional support after stroke |
| CLIN-RENAL — Kidneys and urinary tract | Chronic kidney disease; dialysis; kidney stones; recurrent urinary tract infection |
| CLIN-URATE — Uric acid metabolism | High uric acid; gout; linked to kidneys/joints when needed |
| CLIN-ALLERGY — Allergy and intolerance | Allergy to milk; eggs; tree nuts; fish; soy; wheat; sesame; shellfish; fructose intolerance; self-reported histamine intolerance |
| CLIN-ONCOLOGY — Cancer | Nutrition during chemotherapy; during radiotherapy; loss of appetite; cancer cachexia; post-treatment nutrition |
| CLIN-EATING — Eating disorders | Anorexia nervosa; bulimia nervosa; binge eating disorder; avoidant/restrictive food intake disorder (ARFID) |
| CLIN-MENTAL — Mental health and behavior | Nutritional support for depression; anxiety; sleep disorders; emotional eating |
| CLIN-SKIN — Skin, hair, and nails | Acne; eczema; psoriasis; rosacea; hair loss; weak nails |
| CLIN-ORAL — Mouth and teeth | Gingivitis; periodontitis; mouth ulcers; dry mouth; cavity prevention |
| CLIN-DEFICIENCY — Deficiencies and anemia | Deficiency of iron; vitamin D; vitamin B12; folate; calcium; magnesium; zinc; potassium; iodine; anemia |
| CLIN-INHERITED — Genetic and metabolic diseases | Phenylketonuria (PKU); galactosemia; glycogen storage diseases; urea cycle disorders; other inborn errors of metabolism |
| CLIN-NEURO — Neurology | Epilepsy and the therapeutic ketogenic diet when prescribed; multiple sclerosis; nutritional support for migraine; brain injuries; nutritional rehabilitation after stroke; Alzheimer's; Parkinson's |
| CLIN-MUSCULOSKELETAL — Bones, joints, and muscles | Rheumatoid arthritis; osteoarthritis; osteoporosis; osteomalacia; sarcopenia/loss of muscle mass and function |
| CLIN-ACUTE — Surgery and critical care | Pre-operative nutrition; post-operative nutrition; ICU nutrition; tube feeding (enteral nutrition); intravenous (parenteral) nutrition |

### Rules to Prevent Duplication and Confusion

- PCOS has a single record with two tags: "Endocrine" and "Women's health".
- Osteoporosis has a single record with life-stage and women's-health tags when needed.
- Stroke has a single record that can be linked to cardiovascular, neurology, and rehabilitation.
- Constipation, allergies, iron deficiency, and others link to life stage instead of creating a copy for each age group.
- Loss of appetite as a symptom is different from anorexia nervosa as an eating disorder.
- Don't treat milk allergy as equal to lactose intolerance, or celiac disease as equal to wheat allergy and non-celiac sensitivity.
- What is meant by "gluten sensitivity" must be clarified before normalizing it into a diagnosis.
- Anemia is not a synonym for iron deficiency; the system does not link them automatically.
- Symptoms such as fatigue and hair loss do not prove a specific nutrient deficiency.
- "Histamine intolerance" is recorded as a self-reported claim/diagnosis with a verification status; it is not inferred from symptoms automatically.
- This indexing is product organization, not an endorsement of a therapeutic diet for every condition.

### E. Dietary Patterns

| Type | Patterns |
| --- | --- |
| General or customizable patterns | Mediterranean; vegetarian; vegan |
| Macronutrient distribution | Keto; low-carb; low-fat; high-protein |
| Patterns with clinical applications | DASH; low-FODMAP; gluten-free; dairy-free |

Don't present these patterns as equivalent options for everyone. Therapeutic keto for epilepsy is a different clinical track from a user's keto for weight loss. The low-FODMAP diet is a phased track that includes reintroduction and personalization; don't turn it into a permanent blanket restriction. [R09]

### F. Lifestyle

- Quitting smoking.
- Desk work.
- Night shift work.
- Travel.
- Ramadan.
- Hajj and Umrah.

This information is used for meal timing, reminders, and preferences. It does not mean the app decides whether fasting is appropriate or changes medication schedules automatically.

### G. General Health Goals

Immune support; gut health; energy; sleep; focus; fertility; skin; hair; bones.

The two duplicate lists were merged here. These are used as user interests and education areas, with measurable descriptions where possible. They are not used as promises such as "boosting immunity" or "treating infertility" just by choosing a diet.

## 4. Supplements and Herbs

### 4.1 Required Supplements Catalog

Vitamins; minerals; protein powders/supplements; omega-3; probiotics; prebiotics; fiber; creatine; caffeine; electrolytes.

The system separates the **active ingredient**, the **commercial product**, and the **dose**. A multivitamin product is not counted as a single substance when checking for duplication or interactions.

### 4.2 Herbs Catalog

The stated target: 100–150 common herbs. The full names of these herbs were not provided, so this is a **proposed coverage target**, not a completed catalog.

For each herb: scientific name, common and local names, part used, form ("drink/food/powder/extract"), concentration standard if any, and method of use. Don't treat turmeric as a spice as equal to curcumin extract, or green tea as a drink as equal to its extract.

### 4.3 Database Sizes

| Proposal sent | How we adopt it |
| --- | --- |
| 100–150 herbs | A gradual target after defining the market and the most commonly used |
| 150–200 supplements | Need to define whether this means substances or products; remove duplicates first |
| 3,000–10,000 interactions | A commercial ambition with unproven feasibility or coverage; we don't generate records to hit the number |

We start with licensed sources and documented, high-priority relationships. The database's success is measured by the correctness of each record and its coverage of context, not by row count.

## 5. Review of the Interaction Examples Provided

This is an editorial review before data entry, not a treatment prescription for the user.

| Example | Review finding | Data entry decision |
| --- | --- | --- |
| Iron + green tea; "moderate, separate by two hours" | There is evidence that some polyphenols affect non-heme iron absorption. NHS advises a two-hour gap from tea/coffee in its guidance on taking ferrous sulfate. This does not establish a uniform severity for every iron preparation and every form of green tea. [R03, R04] | Specify the iron type, tea form, and context; don't generalize the timing or severity beyond their reference |
| Iron + turmeric; "possible, better to separate" | A case report was found on high doses of turmeric and possible iron deficiency. The full text was not available during this review due to an access barrier; the report alone doesn't establish a general rule or an effective separation period. [R08] | Put it on the evidence-review list; don't publish it as an automatic recommendation |
| Vitamin K + ginkgo; "high, bleeding risk" | The example is not supported as written in the sources we reviewed. The NCCIH warning concerns ginkgo with anticoagulants such as warfarin; ODS explains the vitamin K–warfarin interaction separately. [R05, R06] | Exclude the proposed pair from approved rules until there is direct evidence; don't transfer a drug warning to a different pair |

"Ginkgo + warfarin" and "vitamin K + warfarin" can be researched as two separate documented records. Don't combine them into a single rule, and don't assign a final severity rating without a classification framework and specialist review. The app does not change the dose of warfarin or any other medication.

## 6. Interactions Database Design

### 6.1 Relationship Types

- Drug ↔ drug.
- Drug ↔ supplement/nutrient.
- Drug ↔ herb.
- Drug ↔ food/beverage.
- Supplement ↔ supplement.
- Supplement ↔ herb.
- Herb ↔ herb, if appropriate evidence exists.
- Substance ↔ health condition/pregnancy/breastfeeding: a separate precaution or contraindication record, not mixed with pairwise interactions.
- Duplication of an active ingredient across several products: a detection rule separate from interactions.

### 6.2 Proposed Record Fields

| Field | Content |
| --- | --- |
| interaction_id / version | Stable identifier and version |
| entity_a / entity_b | Standardized substance identifiers, names, and categories |
| formulation | Form, concentration, plant part, and product if the rule is product-specific |
| dose_route_timing | The dose, route of administration, and timing covered by the evidence |
| population_context | Age group, pregnancy, disease, kidney/liver function when tied to the evidence |
| effect / direction | What changes: absorption, efficacy, toxicity, bleeding, or other |
| mechanism | Known mechanism or hypothesis, distinguishing the two |
| severity | Severity of clinical effect within a declared classification, or unspecified |
| evidence_level | Quality and type of evidence; separate from severity |
| clinical_relevance | Is the effect clinically documented, or theoretical/in-vitro? |
| recommendation | Context-reviewed text; the LLM does not generate timing or dosing on its own |
| source_citations | Reference, year, DOI/PMID if available, and the supporting excerpt |
| limitations | Evidence limits, conflicting studies, and uncovered contexts |
| license | Rights to store, display, and reuse |
| reviewer / reviewed_at | The specialist and review date |
| review_status | draft / reviewed / approved / retired |
| next_review_at | Date to review for updates |

### 6.3 UI Classification

| Status | Meaning |
| --- | --- |
| Documented severe interaction | Prominent warning with explanation and a reviewed action |
| Moderate interaction | Significant effect in a specific context, with conditions explained |
| Minor interaction | Limited effect per the reference |
| Possible interaction / severity unspecified | Evidence or clinical significance not settled |
| Unknown / not covered | Missing data, unmatched substance, or pair not checked |
| No documented interaction found within the sources checked | A search result limited by coverage and date; not a safety certificate |

Don't use green to mean "safe" just because no record exists. Don't rely on color alone; add clear text. Severity and evidence quality are two separate axes, and "possible" is not a severity level.

**Role of AI:** Extracting a draft from a reference, suggesting name matches, and simplifying an approved record. It is not allowed to author interactions or references, or to approve them itself.

## 7. Lab Tests

| Group | Tests mentioned |
| --- | --- |
| Glucose | Blood sugar test, specifying the type when available; HbA1c |
| Nutrients | Vitamin D; vitamin B12; iron; ferritin |
| Organ function | Liver function; kidney function |
| Lipids | Lipid tests |
| Other | Uric acid; thyroid hormones |

Each result has a test name/identifier, value, unit, the lab's reference range, sample collection date, source, and extraction confirmation status. Don't store a "kidney function" panel as a single number.

The early release can store results and show trends. Interpreting them, diagnosing a deficiency, or prescribing supplements requires context and review. When OCR is used, the value and unit must be confirmed, and a generic unit conversion must not be applied across different tests.

## 8. How We Turn the Catalog into a Product

The following classification is an implementation recommendation, not an assessment of how strong nutritional treatment is for each disease.

| Track | What can be added | Activation condition |
| --- | --- | --- |
| M1 — Foundation | Food logging, USDA, appropriate general goals, preferences, health profile with supplements and herbs, recipe memory | Core project requirements plus calculation and privacy tests |
| M2 — Knowledge and follow-up | Documented education pages, symptom history, lab storage, export for the doctor | Reviewed content, data confirmation, and a statement of usage limits |
| M3 — Selected clinical modules | Following a plan set by a specialist, clear rules for selected conditions, approved interactions | A specific reference, appropriate licensing, specialist review, and module-specific tests |
| M4 — High specialization | PKU and inborn errors of metabolism, dialysis, tube/IV feeding, critical care, oncology, eating disorders, infants, and others depending on scope | A dedicated project/professional track and clinical and regulatory evaluation before launch |

A complex condition can be recorded in the profile without activating automatic recommendations for it. Having a diagnosis on file doesn't mean the system "supports it therapeutically".

An appropriate experience for eating disorders should be provided, as defined by a specialist; don't assume that showing calories and deficit goals is suitable for all these conditions. NICE provides a care reference for eating disorders, but don't assume a single document covers every sub-diagnosis. [R12]

When multiple conditions are present, we don't automatically merge conflicting instructions. Conflicts are shown or referred to the specialist. An engineering example: a "high-protein" preference combined with a kidney condition needs review; list order does not make the treatment decision.

## 9. What Each Disease Track Needs Before Approval

One card per module covering:

- Scope definition, target group, and confirmed/self-reported diagnosis.
- Type of role: education, follow-up, support for a specialist's plan, or an approved therapeutic intervention.
- Specific sources and their versions, plus the strength and limits of the evidence.
- The data required and when it is insufficient.
- Cases that block a recommendation or require review.
- Conflict rules with other conditions, medications, and supplements.
- The person responsible for clinical review and its date.
- Tests for expected and high-risk scenarios.
- The wording allowed for users and the claims the evidence does not support.

A large list doesn't justify creating "one diet" per disease. USDA sources answer questions about food composition; guideline sources answer how nutrition is applied in a clinical context.

## 10. Source Register and Review Status

The following links are a documented starting point for this review, not a ready-made licensed interactions database.

| Code | Source | Use and review limits |
| --- | --- | --- |
| R01 | [USDA: Data Type Documentation](https://fdc.nal.usda.gov/data-documentation/) | The data-type comparison was read; distinguishes analysis from labels and others |
| R02 | [USDA: API Guide](https://fdc.nal.usda.gov/api-guide/) | Access, licensing, and rate limit were reviewed |
| R03 | [NIH ODS: Iron — Health Professional](https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/) | Absorption information was reviewed; does not establish all iron–herb pairs |
| R04 | [NHS: How and when to take ferrous sulfate](https://www.nhs.uk/medicines/ferrous-sulfate/how-and-when-to-take-ferrous-sulfate/) | The preparation's guidance was read; we don't generalize it to all iron preparations |
| R05 | [NCCIH: Ginkgo](https://www.nccih.nih.gov/health/ginkgo) | The anticoagulant warning was read |
| R06 | [NIH ODS: Vitamin K — Health Professional](https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/) | The warfarin interaction was read |
| R07 | [NCCIH: Turmeric](https://www.nccih.nih.gov/health/turmeric) | A reference page on turmeric; not in itself evidence for an "iron + turmeric" rule |
| R08 | [Iron Deficiency Anemia Due to High-dose Turmeric](https://pmc.ncbi.nlm.nih.gov/articles/PMC6414192/) | A case report that appeared in search; the full text couldn't be accessed during this review; needs critical reading |
| R09 | [Monash: Three phases of the low FODMAP diet](https://www.monashfodmap.com/blog/3-phases-low-fodmap-diet/) | The phases were read; does not grant the right to copy or license its app database |
| R10 | [ESPEN Guidelines](https://www.espen.org/guidelines) | The index was read; selecting and reading the appropriate guideline for each module is later work |
| R11 | [NIH ODS: Supplement fact sheets](https://ods.od.nih.gov/factsheets/list-all/) | The supplement resources index was read; not a comprehensive interactions API |
| R12 | [NICE NG69: Eating disorders](https://www.nice.org.uk/guidance/ng69) | The guideline's scope appeared in search; opening the page failed, and the detailed recommendations were not reviewed |
| R13 | [NIDDK: IBS nutrition](https://www.niddk.nih.gov/health-information/digestive-diseases/irritable-bowel-syndrome/eating-diet-nutrition) | Appeared in search as an educational source; must be read in full before turning it into rules |

### Additional Sources to Collect Later

- Selected guidelines from ADA for diabetes, KDIGO for kidney disease, and appropriate references for cardiology and sports nutrition. This is a proposed research list; no specific documents from it were reviewed here.
- A specialized reference for children and infants, and another for metabolic diseases, depending on the approved modules.
- National/local sources for dishes, products, and language.
- An interactions data provider that explicitly supports the required herbs, supplements, and medications, with commercial use and update rights. We don't assume any drug database subscription covers all herbs.
- Measured recipe data reviewed by a dietitian.

For each new source: record the version, access date, owner, license, content type, specialist review, and the requirements it supports. Free access to a page doesn't mean permission to copy or redistribute its database.

## 11. Instructions for Integrating This Addendum into Codex

1. Treat this file as an additional resource to nutrition-app-codex-handoff.md, not as approval to implement all modules immediately.
2. Extract a topic register with independent entities for goals, conditions, dietary patterns, life stages, lifestyle, lab tests, and substances.
3. Use a single identifier per topic with multiple tags, plus Arabic/English names and synonyms.
4. Distinguish status: proposed / evidence-review / clinically-approved / implemented / validated; don't let "on the list" mean "approved".
5. Link every executable rule to its source, version, reviewer, and approval date.
6. Don't enter the interaction examples provided as approved production data.
7. Keep missing data and unknown coverage visible; don't display a default green "safe".
8. Don't automatically copy every document into RAG or model training; review relevance, licensing, and privacy first.
9. Record the scope expansion and its impact on time and cost. The earlier project estimate does not automatically cover all these clinical modules.
10. Keep accepting new resources, and record conflicts without silently overwriting approved decisions.

**Codex integration note:** This is an expanded topic catalog and resource-review addendum. Preserve the owner's topics, normalize duplicates, and separate wellness goals, diagnoses, symptoms, dietary patterns, life stages, laboratory observations, and substances. Treat clinical modules and interaction examples as proposed until individually reviewed. Do not fabricate interaction records to meet target counts. Update the requirement/resource registers and identify the smallest approved next increment.

## 12. Next Decisions Required

- Which market and target group come first?
- Is the starting point an app for the general user, or a tool for dietitians?
- Which specific disease modules have priority, and who reviews them?
- Is the goal of lab tests to store results, or to support clinical interpretation?
- Is there a contract/budget for interactions data and its review?
- Are the herb and supplement counts long-term targets or launch requirements?

**Current output:** An organized idea map and a focused review of sources and examples. No actual interactions database or treatment protocols were created, and no comprehensive clinical scope was approved.
