from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculations import NUTRIENTS, portion, rounded
from app.errors import AppError
from app.models import FoodVersion, Recipe, RecipeIngredient, RecipeVersion


def nutrient_values(food: FoodVersion):
    return {key: getattr(food, key) for key in NUTRIENTS}


def food_json(food: FoodVersion):
    return {
        "id": str(food.id),
        "name_en": food.name_en,
        "name_ar": food.name_ar,
        "category": food.category,
        "preparation": food.preparation,
        "basis_grams": str(food.basis_grams),
        "nutrients": {key: rounded(getattr(food, key)) for key in NUTRIENTS},
        "source": {
            "name": "USDA FoodData Central",
            "url": food.source_url,
            "data_type": food.data_type,
            "source_date": food.source_date,
            "external_id": str(food.source_snapshot["fdcId"]),
            "version": food.version,
        },
        "ingredient_substances": food.ingredient_substances,
        "ingredient_coverage": food.ingredient_coverage,
    }


def recipe_data(db: Session, version_id, user_id=None):
    row = db.execute(
        select(RecipeVersion, Recipe)
        .join(Recipe, Recipe.id == RecipeVersion.recipe_id)
        .where(RecipeVersion.id == version_id, Recipe.archived.is_(False))
    ).first()
    if not row or (row[1].owner_id is not None and row[1].owner_id != user_id):
        raise AppError("not_found", 404)
    version, recipe = row
    ingredients = db.execute(
        select(RecipeIngredient, FoodVersion)
        .join(FoodVersion, FoodVersion.id == RecipeIngredient.food_version_id)
        .where(RecipeIngredient.recipe_version_id == version.id)
    ).all()
    if not ingredients:
        raise AppError("food_unavailable", 409)
    rows = [portion(nutrient_values(food), item.grams, food.basis_grams) for item, food in ingredients]
    batch = {
        key: sum((row[key] for row in rows), Decimal(0))
        if all(row[key] is not None for row in rows)
        else None
        for key in NUTRIENTS
    }
    substances = sorted({s for _, food in ingredients for s in food.ingredient_substances})
    coverage = (
        "documented"
        if all(food.ingredient_coverage == "documented" for _, food in ingredients)
        else "unknown"
    )
    response = {
        "id": str(version.id),
        "recipe_id": str(recipe.id),
        "name_en": recipe.name_en,
        "name_ar": recipe.name_ar,
        "version": version.version,
        "is_sample": recipe.is_sample,
        "yield_grams": str(version.yield_grams),
        "serving_grams": str(version.serving_grams),
        "method_en": version.method_en,
        "method_ar": version.method_ar,
        "review_status": version.review_status,
        "nutrients": {
            k: rounded(v) for k, v in portion(batch, version.serving_grams, version.yield_grams).items()
        },
        "ingredients": [{"food": food_json(food), "grams": str(item.grams)} for item, food in ingredients],
        "ingredient_substances": substances,
        "ingredient_coverage": coverage,
    }
    return response, batch
