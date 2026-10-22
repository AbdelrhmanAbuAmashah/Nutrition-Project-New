"""Idempotent reference/catalog seed. Never creates users or clinical approvals."""

import hashlib
import json
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import engine
from app.models import (
    FoodRecord,
    FoodVersion,
    HealthCondition,
    Recipe,
    RecipeIngredient,
    RecipeVersion,
    ReferenceResource,
    Substance,
    SubstanceAlias,
)

NS = uuid.UUID("53758dd7-ac66-45e6-8b18-27b02e5dca07")


def stable(value):
    return uuid.uuid5(NS, value)


# Display translations are editorial labels; nutrient numbers come exclusively from the retained records.
FOODS = {
    171705: ("Avocado · raw", "أفوكادو · نيّئ", "fruit", []),
    171688: ("Apple with skin · raw", "تفاح بالقشر · نيّئ", "fruit", []),
    171413: ("Olive oil", "زيت زيتون", "pantry", []),
    170457: ("Tomato · raw", "طماطم · نيّئة", "vegetables", []),
    168409: ("Cucumber with peel · raw", "خيار بالقشر · نيّئ", "vegetables", []),
    168878: ("White rice · cooked", "أرز أبيض · مطبوخ", "grains", []),
    171477: ("Chicken breast · roasted", "صدر دجاج · مشوي", "protein", []),
    173424: ("Whole egg · hard-boiled", "بيض كامل · مسلوق", "protein", ["egg"]),
    173904: ("Oats · dry", "شوفان · جاف", "grains", ["oats"]),
    170567: ("Almonds", "لوز", "pantry", ["almond"]),
    172420: ("Lentils · dry", "عدس · جاف", "protein", ["lentil"]),
    173756: ("Chickpeas · dry", "حمص · جاف", "protein", ["chickpea"]),
    170416: ("Parsley · fresh", "بقدونس · طازج", "vegetables", []),
    170287: ("Bulgur · cooked", "برغل · مطبوخ", "grains", ["wheat"]),
    169910: ("Mango · raw", "مانجو · نيّئ", "fruit", []),
    173757: ("Chickpeas · cooked, no added salt", "حمص · مسلوق دون ملح مضاف", "protein", ["chickpea"]),
    172421: ("Lentils · cooked, no added salt", "عدس · مسلوق دون ملح مضاف", "protein", ["lentil"]),
    173944: ("Banana · raw", "موز · نيّئ", "fruit", []),
    170000: ("Onion · raw", "بصل · نيّئ", "vegetables", []),
}
SUBSTANCES = [
    ("milk", "Milk", "الحليب"),
    ("egg", "Egg", "البيض"),
    ("wheat", "Wheat", "القمح"),
    ("sesame", "Sesame", "السمسم"),
    ("peanut", "Peanut", "الفول السوداني"),
    ("almond", "Almond", "اللوز"),
    ("walnut", "Walnut", "الجوز"),
    ("soy", "Soy", "الصويا"),
    ("fish", "Fish", "السمك"),
    ("shellfish", "Shellfish", "المحار والقشريات"),
    ("chickpea", "Chickpea", "الحمص"),
    ("lentil", "Lentil", "العدس"),
    ("oats", "Oats", "الشوفان"),
]
RECIPES = [
    {
        "slug": "mujaddara",
        "en": "Mujaddara bowl",
        "ar": "طبق مجدّرة",
        "yield": 830,
        "serving": 275,
        "ingredients": [(172421, 400), (168878, 300), (170000, 100), (171413, 30)],
        "method_en": "Sample batch: combine cooked lentils and rice with onion and olive oil. Enter your own cooked yield for a different recipe.",
        "method_ar": "دفعة توضيحية: اخلط العدس والأرز المطبوخين مع البصل وزيت الزيتون. أدخل وزن الناتج المطبوخ لوصفتك الخاصة.",
    },
    {
        "slug": "tabbouleh",
        "en": "Tabbouleh salad",
        "ar": "سلطة تبّولة",
        "yield": 690,
        "serving": 230,
        "ingredients": [(170287, 200), (170457, 250), (168409, 100), (170416, 120), (171413, 20)],
        "method_en": "Sample recipe: combine cooked bulgur, chopped tomato, cucumber, parsley and olive oil. Quantities and yield are illustrative.",
        "method_ar": "وصفة توضيحية: اخلط البرغل المطبوخ والطماطم والخيار والبقدونس وزيت الزيتون. المقادير والوزن توضيحيان.",
    },
    {
        "slug": "balela",
        "en": "Balela chickpea salad",
        "ar": "سلطة بليلة بالحمص",
        "yield": 750,
        "serving": 250,
        "ingredients": [(173757, 400), (170457, 200), (170416, 30), (170000, 100), (171413, 20)],
        "method_en": "Sample batch: toss cooked chickpeas with tomato, parsley, onion and olive oil. Adjust quantities to match what you actually prepare.",
        "method_ar": "دفعة توضيحية: اخلط الحمص المسلوق والطماطم والبقدونس والبصل وزيت الزيتون. عدّل المقادير حسب وصفتك الفعلية.",
    },
]


def seed(db: Session):
    source_path = Path(__file__).resolve().parents[1] / "data/usda-source-records.json"
    content = source_path.read_bytes()
    data = json.loads(content)
    source_id = stable("usda-sr-legacy")
    if db.get(ReferenceResource, source_id) is None:
        db.add(
            ReferenceResource(
                id=source_id,
                key="usda-sr-legacy",
                title="USDA FoodData Central · SR Legacy",
                url="https://fdc.nal.usda.gov/",
                version="SR Legacy / retained API snapshot 2026-10-22",
                license="CC0-1.0",
                retrieved_at=datetime(2026, 10, 22, tzinfo=UTC),
                review_status="source_verified",
                content_hash=hashlib.sha256(content).hexdigest(),
            )
        )
    for key, en, ar in SUBSTANCES:
        if db.get(Substance, key) is None:
            db.add(Substance(id=key, name_en=en, name_ar=ar, kind="food"))
            db.add_all(
                [
                    SubstanceAlias(
                        id=stable(f"alias:{key}:{locale}"),
                        substance_id=key,
                        locale=locale,
                        normalized_name=label.lower(),
                    )
                    for locale, label in [("en", en), ("ar", ar)]
                ]
            )
    for key, en, ar in [
        ("type1_diabetes", "Type 1 diabetes", "السكري من النوع الأول"),
        ("type2_diabetes", "Type 2 diabetes", "السكري من النوع الثاني"),
        ("hypertension", "Hypertension", "ارتفاع ضغط الدم"),
    ]:
        if db.get(HealthCondition, key) is None:
            db.add(HealthCondition(id=key, name_en=en, name_ar=ar, module_status="not_activated"))
    db.flush()
    food_ids = {}
    nutrient_ids = {
        "calories": 1008,
        "protein": 1003,
        "fat": 1004,
        "carbs": 1005,
        "fiber": 1079,
        "sodium": 1093,
    }
    for raw in data["records"]:
        fdc = raw["fdcId"]
        if fdc not in FOODS:
            continue
        record_id, version_id = stable(f"food:{fdc}"), stable(f"food:{fdc}:snapshot:2026-10-22")
        food_ids[fdc] = version_id
        if db.get(FoodVersion, version_id) is not None:
            continue
        en, ar, category, substances = FOODS[fdc]
        nutrient_map = {n["nutrient"]["id"]: n.get("amount") for n in raw["foodNutrients"]}
        values = {
            key: Decimal(str(nutrient_map[nid])) if nutrient_map.get(nid) is not None else None
            for key, nid in nutrient_ids.items()
        }
        db.add(FoodRecord(id=record_id, source_id=source_id, external_id=str(fdc)))
        db.flush()
        db.add(
            FoodVersion(
                id=version_id,
                food_id=record_id,
                version=1,
                is_current=True,
                name_en=en,
                name_ar=ar,
                category=category,
                preparation=raw["description"],
                data_type=raw["dataType"],
                source_url=f"https://fdc.nal.usda.gov/food-details/{fdc}/nutrients",
                source_date=raw.get("publicationDate", "SR Legacy"),
                basis_grams=100,
                ingredient_substances=substances,
                ingredient_coverage="documented",
                source_snapshot=raw,
                **values,
            )
        )
    db.flush()
    for spec in RECIPES:
        recipe_id, version_id = stable("recipe:" + spec["slug"]), stable("recipe:" + spec["slug"] + ":1")
        if db.get(Recipe, recipe_id) is not None:
            continue
        db.add(
            Recipe(
                id=recipe_id,
                owner_id=None,
                slug=spec["slug"],
                name_en=spec["en"],
                name_ar=spec["ar"],
                is_sample=True,
            )
        )
        db.flush()
        db.add(
            RecipeVersion(
                id=version_id,
                recipe_id=recipe_id,
                version=1,
                method_en=spec["method_en"],
                method_ar=spec["method_ar"],
                yield_grams=spec["yield"],
                serving_grams=spec["serving"],
                review_status="sample_not_clinical",
            )
        )
        db.flush()
        for fdc, grams in spec["ingredients"]:
            if fdc not in food_ids:
                raise RuntimeError(f"Missing required USDA source record {fdc}")
            db.add(RecipeIngredient(recipe_version_id=version_id, food_version_id=food_ids[fdc], grams=grams))
    db.commit()


if __name__ == "__main__":
    with Session(engine()) as db:
        seed(db)
    print("Reference catalog ready: 19 traceable USDA foods and 3 illustrative local recipes; no demo users.")
