import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

Password = Annotated[str, StringConstraints(strip_whitespace=False)]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Register(Input):
    email: EmailStr
    password: Password = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)
    locale: Literal["en", "ar"] = "en"
    accept_privacy: bool


class Login(Input):
    email: EmailStr
    password: Password = Field(min_length=1, max_length=128)


class RestrictionInput(Input):
    substance_id: str = Field(max_length=60)
    kind: Literal["allergy", "intolerance", "dislike"] = "allergy"


class ProfileUpdate(Input):
    revision: int = Field(ge=1)
    display_name: str = Field(min_length=1, max_length=80)
    locale: Literal["en", "ar"]
    country: Literal["JO", "SA"]
    timezone: str = Field(max_length=64)
    units: Literal["metric", "imperial"] = "metric"
    goal: Literal["understand", "maintain", "lose", "gain"] = "understand"
    target_origin: Literal["user", "professional"] = "user"
    calorie_target: Decimal | None = Field(default=None, gt=0, le=15000, decimal_places=2)
    protein_target: Decimal | None = Field(default=None, ge=0, le=2000, decimal_places=2)
    carbs_target: Decimal | None = Field(default=None, ge=0, le=3000, decimal_places=2)
    fat_target: Decimal | None = Field(default=None, ge=0, le=2000, decimal_places=2)
    allergy_status: Literal["unknown", "none", "recorded"] = "unknown"
    restrictions: list[RestrictionInput] = Field(default_factory=list, max_length=40)
    conditions: list[str] = Field(default_factory=list, max_length=20)
    preferences: list[Literal["vegetarian", "vegan", "halal", "pescatarian"]] = Field(default_factory=list)
    complete_onboarding: bool = False

    @field_validator("timezone")
    @classmethod
    def valid_timezone(cls, value):
        try:
            ZoneInfo(value)
        except (ZoneInfoNotFoundError, ValueError) as error:
            raise ValueError("timezone") from error
        return value

    @model_validator(mode="after")
    def unique_restrictions(self):
        values = [(r.substance_id, r.kind) for r in self.restrictions]
        if len(values) != len(set(values)) or len(self.conditions) != len(set(self.conditions)):
            raise ValueError("duplicate")
        return self


class MealItemInput(Input):
    food_version_id: uuid.UUID | None = None
    recipe_version_id: uuid.UUID | None = None
    grams: Decimal = Field(gt=0, le=10000, max_digits=8, decimal_places=3)
    evidence: Literal["weighed", "user_entered"] = "user_entered"

    @model_validator(mode="after")
    def exactly_one_source(self):
        if (self.food_version_id is None) == (self.recipe_version_id is None):
            raise ValueError("one_source")
        return self


class MealInput(Input):
    title: str = Field(min_length=1, max_length=120)
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"]
    consumed_at: AwareDatetime
    items: list[MealItemInput] = Field(min_length=1, max_length=40)


class AccountDelete(Input):
    password: Password = Field(min_length=1, max_length=128)


def iso(value: datetime | None):
    return value.isoformat() if value else None
