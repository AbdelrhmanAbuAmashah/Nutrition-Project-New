import logging
import secrets
import uuid
from datetime import date, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, Header, Query, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import delete, func, or_, select, text, update
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app import meals
from app.catalog import food_json, recipe_data
from app.config import get_settings
from app.database import get_db
from app.errors import AppError, error_body
from app.models import (
    AuditEvent,
    AuthSession,
    ClinicalDraft,
    Consent,
    FoodVersion,
    HealthCondition,
    Meal,
    MealItem,
    Profile,
    Recipe,
    RecipeVersion,
    Substance,
    User,
    UserCondition,
    UserRestriction,
)
from app.schemas import AccountDelete, Login, MealInput, ProfileUpdate, Register
from app.security import (
    DUMMY_HASH,
    REFRESH_COOKIE,
    check_csrf,
    clear_cookies,
    current_user,
    digest,
    new_session,
    now,
    passwords,
    rate_check,
    set_session_cookies,
)

settings = get_settings()
app = FastAPI(
    title="Nour API",
    version="0.1.0",
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url=None,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.hosts)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "X-CSRF-Token", "Idempotency-Key", "Accept-Language"],
)
DB = Annotated[Session, Depends(get_db)]
Member = Annotated[User, Depends(current_user)]
log = logging.getLogger("nour")


@app.middleware("http")
async def request_boundary(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())
    origin = request.headers.get("origin", "").rstrip("/")
    if request.method not in ("GET", "HEAD", "OPTIONS") and origin and origin not in settings.origins:
        return JSONResponse(error_body(request, "origin"), status_code=403)
    try:
        response = await call_next(request)
    except Exception as error:
        # Exception strings/SQL bind parameters may contain health information or credentials.
        log.error("request_failed type=%s request_id=%s", type(error).__name__, request.state.request_id)
        response = JSONResponse(error_body(request, "internal"), status_code=500)
    response.headers["X-Request-ID"] = request.state.request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(AppError)
async def app_error(request: Request, error: AppError):
    headers = {"Retry-After": "900"} if error.status == 429 else None
    return JSONResponse(error_body(request, error.code), status_code=error.status, headers=headers)


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, error: RequestValidationError):
    fields = [{"field": ".".join(map(str, item["loc"][1:])), "code": item["type"]} for item in error.errors()]
    return JSONResponse(error_body(request, "validation", fields), status_code=422)


@app.exception_handler(OperationalError)
async def database_unavailable(request: Request, error: OperationalError):
    log.error("database_unavailable request_id=%s", request.state.request_id)
    return JSONResponse(error_body(request, "service_unavailable"), status_code=503)


@app.exception_handler(HTTPException)
async def http_error(request: Request, error: HTTPException):
    return JSONResponse(
        error_body(request, "not_found" if error.status_code == 404 else "validation"),
        status_code=error.status_code,
    )


def user_json(user: User):
    return {"id": str(user.id), "email": user.email, "display_name": user.display_name, "role": user.role}


def profile_json(db: Session, user: User):
    profile = db.get(Profile, user.id)
    restrictions = db.scalars(select(UserRestriction).where(UserRestriction.user_id == user.id))
    conditions = list(db.scalars(select(UserCondition.condition_id).where(UserCondition.user_id == user.id)))
    return {
        "user": user_json(user),
        "locale": profile.locale,
        "country": profile.country,
        "timezone": profile.timezone,
        "units": profile.units,
        "goal": profile.goal,
        "target_origin": profile.target_origin,
        "calorie_target": str(profile.calorie_target) if profile.calorie_target is not None else None,
        "protein_target": str(profile.protein_target) if profile.protein_target is not None else None,
        "carbs_target": str(profile.carbs_target) if profile.carbs_target is not None else None,
        "fat_target": str(profile.fat_target) if profile.fat_target is not None else None,
        "allergy_status": profile.allergy_status,
        "preferences": profile.preferences,
        "revision": profile.revision,
        "onboarding_completed": profile.onboarding_completed_at is not None,
        "restrictions": [
            {"substance_id": r.substance_id, "kind": r.kind, "confirmed": r.confirmed} for r in restrictions
        ],
        "conditions": conditions,
    }


@app.get("/health")
def health(db: DB):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ready", "version": "0.1.0"}


@app.post("/api/v1/auth/register", status_code=201)
def register(payload: Register, request: Request, response: Response, db: DB):
    email = str(payload.email).lower()
    rate_check(request, db, email)
    if not payload.accept_privacy:
        raise AppError("consent_required", 422)
    user = User(
        email=email, display_name=payload.display_name, password_hash=passwords.hash(payload.password)
    )
    db.add(user)
    try:
        db.flush()
        db.add(Profile(user_id=user.id, locale=payload.locale))
        db.add(Consent(user_id=user.id, purpose="service", version="2026-10-22"))
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise AppError("email_exists", 409) from error
    new_session(response, db, user)
    return profile_json(db, user)


@app.post("/api/v1/auth/login")
def login(payload: Login, request: Request, response: Response, db: DB):
    email = str(payload.email).lower()
    rate_check(request, db, email)
    user = db.scalar(select(User).where(User.email == email))
    valid = passwords.verify(payload.password, user.password_hash if user else DUMMY_HASH)
    if not user or not user.is_active or not valid:
        raise AppError("credentials", 401)
    new_session(response, db, user)
    return profile_json(db, user)


@app.post("/api/v1/auth/refresh")
def refresh(request: Request, response: Response, db: DB):
    token = request.cookies.get(REFRESH_COOKIE, "")
    auth = db.scalar(select(AuthSession).where(AuthSession.refresh_hash == digest(token)).with_for_update())
    if not token or not auth or auth.revoked_at or auth.expires_at <= now():
        raise AppError("session_expired", 401)
    check_csrf(request, auth)
    user = db.get(User, auth.user_id)
    if not user or not user.is_active:
        raise AppError("auth_required", 401)
    rotated, csrf = secrets.token_urlsafe(48), secrets.token_urlsafe(32)
    auth.refresh_hash, auth.csrf_hash = digest(rotated), digest(csrf)
    db.commit()
    set_session_cookies(response, user, auth, rotated, csrf)
    return profile_json(db, user)


@app.post("/api/v1/auth/logout", status_code=204)
def logout(request: Request, response: Response, user: Member, db: DB):
    request.state.auth_session.revoked_at = now()
    db.commit()
    clear_cookies(response)


@app.get("/api/v1/auth/me")
@app.get("/api/v1/profile")
def get_profile(user: Member, db: DB):
    return profile_json(db, user)


@app.patch("/api/v1/profile")
def update_profile(payload: ProfileUpdate, user: Member, db: DB):
    profile = db.scalar(select(Profile).where(Profile.user_id == user.id).with_for_update())
    if payload.revision != profile.revision:
        raise AppError("profile_conflict", 409)
    allergens = [r for r in payload.restrictions if r.kind == "allergy"]
    if (allergens and payload.allergy_status != "recorded") or (
        payload.allergy_status == "recorded" and not allergens
    ):
        raise AppError("allergy_status", 422)
    ids = {r.substance_id for r in payload.restrictions}
    if ids - set(db.scalars(select(Substance.id).where(Substance.id.in_(ids)))):
        raise AppError("validation", 422)
    if set(payload.conditions) - set(
        db.scalars(select(HealthCondition.id).where(HealthCondition.id.in_(payload.conditions)))
    ):
        raise AppError("validation", 422)
    values = payload.model_dump(
        exclude={"revision", "restrictions", "conditions", "complete_onboarding", "display_name"}
    )
    for key, value in values.items():
        setattr(profile, key, value)
    profile.revision += 1
    if payload.complete_onboarding and profile.onboarding_completed_at is None:
        profile.onboarding_completed_at = now()
    user.display_name = payload.display_name
    db.execute(delete(UserRestriction).where(UserRestriction.user_id == user.id))
    for restriction in payload.restrictions:
        db.add(UserRestriction(user_id=user.id, **restriction.model_dump(), confirmed=True))
    db.execute(delete(UserCondition).where(UserCondition.user_id == user.id))
    for condition in payload.conditions:
        db.add(UserCondition(user_id=user.id, condition_id=condition, confirmation_status="self_reported"))
    db.execute(
        update(ClinicalDraft)
        .where(
            ClinicalDraft.user_id == user.id,
            ClinicalDraft.status.in_(["awaiting_review", "approved", "published"]),
        )
        .values(status="stale")
    )
    db.add(
        AuditEvent(
            actor_id=user.id, operation="profile.updated", resource_type="profile", resource_id=str(user.id)
        )
    )
    db.commit()
    return profile_json(db, user)


@app.get("/api/v1/catalog/options")
def catalog_options(user: Member, db: DB):
    return {
        "substances": [
            {"id": s.id, "name_en": s.name_en, "name_ar": s.name_ar}
            for s in db.scalars(select(Substance).order_by(Substance.id))
        ],
        "conditions": [
            {"id": c.id, "name_en": c.name_en, "name_ar": c.name_ar, "module_status": c.module_status}
            for c in db.scalars(select(HealthCondition))
        ],
    }


@app.get("/api/v1/foods")
def search_foods(
    user: Member,
    db: DB,
    q: str = Query(default="", max_length=80),
    category: str | None = Query(default=None, max_length=40),
    limit: int = Query(default=40, ge=1, le=100),
):
    query = select(FoodVersion).where(FoodVersion.is_current.is_(True))
    if q.strip():
        needle = "%" + q.strip().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        query = query.where(
            or_(
                FoodVersion.name_en.ilike(needle, escape="\\"), FoodVersion.name_ar.ilike(needle, escape="\\")
            )
        )
    if category:
        query = query.where(FoodVersion.category == category)
    count = db.scalar(select(func.count()).select_from(query.subquery()))
    return {
        "items": [food_json(f) for f in db.scalars(query.order_by(FoodVersion.name_en).limit(limit))],
        "count": count,
    }


@app.get("/api/v1/foods/{food_id}")
def get_food(food_id: uuid.UUID, user: Member, db: DB):
    food = db.get(FoodVersion, food_id)
    if not food:
        raise AppError("not_found", 404)
    return food_json(food)


@app.get("/api/v1/recipes")
def get_recipes(user: Member, db: DB):
    versions = db.scalars(
        select(RecipeVersion)
        .join(Recipe)
        .where(Recipe.archived.is_(False), or_(Recipe.owner_id.is_(None), Recipe.owner_id == user.id))
        .order_by(Recipe.created_at)
    )
    return {"items": [recipe_data(db, v.id, user.id)[0] for v in versions]}


@app.post("/api/v1/meals/preview")
def meal_preview(payload: MealInput, user: Member, db: DB):
    return meals.preview(db, user, payload)


@app.post("/api/v1/meals", status_code=201)
def create_meal(
    payload: MealInput,
    user: Member,
    db: DB,
    idempotency_key: Annotated[str, Header(min_length=8, max_length=128)],
):
    fingerprint = meals.payload_hash(payload)
    existing = db.scalar(select(Meal).where(Meal.user_id == user.id, Meal.idempotency_key == idempotency_key))
    if existing:
        if existing.request_hash != fingerprint:
            raise AppError("idempotency_conflict", 409)
        return meals.meal_json(db, existing)
    result = meals.preview(db, user, payload)
    meal = Meal(
        user_id=user.id,
        title=payload.title,
        meal_type=payload.meal_type,
        consumed_at=payload.consumed_at,
        idempotency_key=idempotency_key,
        request_hash=fingerprint,
        nutrient_snapshot=result["nutrition"],
        restriction_snapshot=result["restrictions"],
        calculation_version=result["calculation_version"],
    )
    db.add(meal)
    try:
        db.flush()
        for item, snapshot in zip(payload.items, result["items"], strict=True):
            db.add(
                MealItem(
                    meal_id=meal.id,
                    user_id=user.id,
                    food_version_id=item.food_version_id,
                    recipe_version_id=item.recipe_version_id,
                    grams=item.grams,
                    evidence=item.evidence,
                    snapshot=snapshot,
                )
            )
        db.commit()
    except IntegrityError as error:
        db.rollback()
        existing = db.scalar(
            select(Meal).where(Meal.user_id == user.id, Meal.idempotency_key == idempotency_key)
        )
        if existing and existing.request_hash == fingerprint:
            return meals.meal_json(db, existing)
        raise AppError("idempotency_conflict", 409) from error
    return meals.meal_json(db, meal)


@app.post("/api/v1/meals/{meal_id}/confirm")
def confirm_meal(meal_id: uuid.UUID, user: Member, db: DB):
    meal = db.scalar(select(Meal).where(Meal.id == meal_id, Meal.user_id == user.id).with_for_update())
    if not meal:
        raise AppError("not_found", 404)
    if meal.status == "draft":
        meal.status, meal.confirmed_at = "confirmed", now()
        db.add(
            AuditEvent(
                actor_id=user.id, operation="meal.confirmed", resource_type="meal", resource_id=str(meal.id)
            )
        )
        db.commit()
    return meals.meal_json(db, meal)


@app.get("/api/v1/meals/{meal_id}")
def get_meal(meal_id: uuid.UUID, user: Member, db: DB):
    meal = db.scalar(select(Meal).where(Meal.id == meal_id, Meal.user_id == user.id))
    if not meal:
        raise AppError("not_found", 404)
    return meals.meal_json(db, meal)


@app.delete("/api/v1/meals/{meal_id}", status_code=204)
def delete_meal(meal_id: uuid.UUID, user: Member, db: DB):
    meal = db.scalar(select(Meal).where(Meal.id == meal_id, Meal.user_id == user.id))
    if not meal:
        raise AppError("not_found", 404)
    db.delete(meal)
    db.commit()


@app.get("/api/v1/diary")
def get_diary(user: Member, db: DB, day: date | None = None):
    profile = db.get(Profile, user.id)
    selected = day or now().astimezone(ZoneInfo(profile.timezone)).date()
    return meals.diary(db, user, selected)


@app.get("/api/v1/summary")
def get_summary(user: Member, db: DB, day: date | None = None):
    profile = db.get(Profile, user.id)
    selected = day or now().astimezone(ZoneInfo(profile.timezone)).date()
    days = [meals.diary(db, user, selected - timedelta(days=offset)) for offset in range(6, -1, -1)]
    return {
        "days": [
            {"date": d["date"], "nutrition": d["nutrition"], "meal_count": len(d["meals"])} for d in days
        ]
    }


@app.get("/api/v1/account/export")
def export_account(user: Member, db: DB):
    all_meals = db.scalars(select(Meal).where(Meal.user_id == user.id).order_by(Meal.consumed_at))
    return JSONResponse(
        {
            "export_version": "1",
            "exported_at": now().isoformat(),
            "profile": profile_json(db, user),
            "meals": [meals.meal_json(db, meal) for meal in all_meals],
        },
        headers={"Content-Disposition": 'attachment; filename="nour-export.json"'},
    )


@app.delete("/api/v1/account", status_code=204)
def delete_account(payload: AccountDelete, response: Response, user: Member, db: DB):
    if not passwords.verify(payload.password, user.password_hash):
        raise AppError("credentials", 401)
    db.delete(user)
    db.commit()
    clear_cookies(response)
