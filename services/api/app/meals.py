import hashlib
import json
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculations import NUTRIENTS, check_restrictions, portion, rounded, total
from app.catalog import food_json, nutrient_values, recipe_data
from app.errors import AppError
from app.models import FoodVersion, Meal, MealItem, Profile, User, UserRestriction
from app.schemas import MealInput


def preview(db: Session, user: User, payload: MealInput):
    profile = db.get(Profile, user.id)
    restrictions = list(db.scalars(select(UserRestriction).where(UserRestriction.user_id == user.id)))
    rows, snapshots, all_substances, coverage = [], [], set(), "documented"
    cache = {}
    for item in payload.items:
        if item.food_version_id:
            food = cache.get(item.food_version_id)
            if food is None:
                food = db.get(FoodVersion, item.food_version_id)
                cache[item.food_version_id] = food
            if not food:
                raise AppError("food_unavailable", 409)
            source = food_json(food)
            values = portion(nutrient_values(food), item.grams, food.basis_grams)
            snapshot = {"type": "food", "source": source}
        else:
            source, batch = recipe_data(db, item.recipe_version_id, user.id)
            values = portion(batch, item.grams, Decimal(source["yield_grams"]))
            snapshot = {"type": "recipe", "source": source}
        all_substances.update(source["ingredient_substances"])
        if source["ingredient_coverage"] != "documented":
            coverage = "unknown"
        rows.append(values)
        snapshots.append(
            {
                **snapshot,
                "grams": str(item.grams),
                "evidence": item.evidence,
                "nutrients": {key: rounded(values[key]) for key in NUTRIENTS},
            }
        )
    return {
        "nutrition": total(rows),
        "items": snapshots,
        "restrictions": check_restrictions(all_substances, coverage, restrictions, profile.allergy_status),
        "calculation_version": "1",
    }


def payload_hash(payload: MealInput):
    return hashlib.sha256(json.dumps(payload.model_dump(mode="json"), sort_keys=True).encode()).hexdigest()


def meal_json(db: Session, meal: Meal):
    items = db.scalars(
        select(MealItem).where(MealItem.meal_id == meal.id).order_by(MealItem.created_at, MealItem.id)
    )
    return {
        "id": str(meal.id),
        "title": meal.title,
        "meal_type": meal.meal_type,
        "status": meal.status,
        "consumed_at": meal.consumed_at.isoformat(),
        "confirmed_at": meal.confirmed_at.isoformat() if meal.confirmed_at else None,
        "nutrition": meal.nutrient_snapshot,
        "restrictions": meal.restriction_snapshot,
        "calculation_version": meal.calculation_version,
        "items": [item.snapshot for item in items],
    }


def day_bounds(day: date, timezone: str):
    zone = ZoneInfo(timezone)
    return (
        datetime.combine(day, time.min, zone).astimezone(UTC),
        datetime.combine(day + timedelta(days=1), time.min, zone).astimezone(UTC),
    )


def diary(db: Session, user: User, day: date):
    profile = db.get(Profile, user.id)
    start, end = day_bounds(day, profile.timezone)
    meals = list(
        db.scalars(
            select(Meal)
            .where(
                Meal.user_id == user.id,
                Meal.status == "confirmed",
                Meal.consumed_at >= start,
                Meal.consumed_at < end,
            )
            .order_by(Meal.consumed_at)
        )
    )
    return {
        "date": day.isoformat(),
        "timezone": profile.timezone,
        "nutrition": total([m.nutrient_snapshot["values"] for m in meals]),
        "meals": [meal_json(db, meal) for meal in meals],
    }
