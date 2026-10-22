# Food catalog and illustrative recipes

`services/api/data/usda-source-records.json` retains 19 original USDA FoodData Central API records retrieved on 22 October 2026. The source is SR Legacy. Its source publication dates and per-record nutrient IDs/units remain in the payload. Data are CC0; attribute USDA FoodData Central. [Official API and licensing reference](https://fdc.nal.usda.gov/api-guide/), [data-type documentation](https://fdc.nal.usda.gov/data-documentation/).

`scripts/import_usda_seed.py` is the reproducible import path. It uses `FDC_API_KEY` when provided and the restricted public `DEMO_KEY` otherwise. That import requires network access. Normal setup and seeding use the retained source file and need neither a provider key nor a live AI service.

The seed maps nutrient IDs 1008 (kcal), 1003 (protein g), 1004 (fat g), 1005 (carbohydrate g), 1079 (fiber g) and 1093 (sodium mg). Missing amounts remain null. Editorial English/Arabic display labels do not alter original descriptions or values. Raw and cooked foods are separate matches, particularly dry versus cooked rice/pulses. Seed IDs are deterministic and re-running the seed does not duplicate or overwrite historical versions.

Catalog: avocado, apple, olive oil, tomato, cucumber, cooked white rice, roasted chicken breast, hard-boiled egg, dry oats, almonds, dry lentils, dry chickpeas, parsley, cooked bulgur, mango, cooked chickpeas without added salt, cooked lentils without added salt, banana and onion.

Three local sample recipes—mujaddara, tabbouleh and balela—use those exact food versions and visible ingredient quantities/yields. Recipe amounts, yields and preparation notes are illustrative project examples, not measured household benchmarks or clinician-approved meal recommendations. Users can inspect every ingredient source before logging a portion. Actual recipes and cooking losses may differ; the source-backed composition does not prove an exact real-world portion estimate.

Recipe Memory editing/recognition, local-brand coverage, broad micronutrient coverage, clinical datasets and interaction databases are later work. Do not quietly classify a similar dish as an exact source match or populate missing nutrients from model output.
