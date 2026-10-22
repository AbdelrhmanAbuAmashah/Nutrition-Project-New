"""PostgreSQL domain model. Reference versions and confirmed meal snapshots are separate."""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )


class Identity:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Identity, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(Text)
    display_name: Mapped[str] = mapped_column(String(80))
    role: Mapped[str] = mapped_column(String(16), default="user", server_default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))
    __table_args__ = (
        CheckConstraint("role IN ('user','reviewer','admin')", name="role"),
        CheckConstraint("email = lower(email)", name="email_normalized"),
    )


class Profile(Base):
    __tablename__ = "profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    locale: Mapped[str] = mapped_column(String(2), default="en", server_default="en")
    country: Mapped[str] = mapped_column(String(2), default="JO", server_default="JO")
    timezone: Mapped[str] = mapped_column(String(64), default="Asia/Amman", server_default="Asia/Amman")
    units: Mapped[str] = mapped_column(String(10), default="metric", server_default="metric")
    goal: Mapped[str] = mapped_column(String(24), default="understand", server_default="understand")
    target_origin: Mapped[str] = mapped_column(String(20), default="user", server_default="user")
    calorie_target: Mapped[Decimal | None] = mapped_column(Numeric(9, 2))
    protein_target: Mapped[Decimal | None] = mapped_column(Numeric(9, 2))
    carbs_target: Mapped[Decimal | None] = mapped_column(Numeric(9, 2))
    fat_target: Mapped[Decimal | None] = mapped_column(Numeric(9, 2))
    allergy_status: Mapped[str] = mapped_column(String(16), default="unknown", server_default="unknown")
    preferences: Mapped[list] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"))
    revision: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    onboarding_completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = (
        CheckConstraint("locale IN ('en','ar')", name="locale"),
        CheckConstraint("country IN ('JO','SA')", name="country"),
        CheckConstraint("allergy_status IN ('unknown','none','recorded')", name="allergy_status"),
        CheckConstraint(
            "target_origin IN ('user','professional','reviewed_calculation')", name="target_origin"
        ),
        CheckConstraint("calorie_target IS NULL OR calorie_target > 0", name="calorie_target"),
        CheckConstraint("protein_target IS NULL OR protein_target >= 0", name="protein_target"),
        CheckConstraint("carbs_target IS NULL OR carbs_target >= 0", name="carbs_target"),
        CheckConstraint("fat_target IS NULL OR fat_target >= 0", name="fat_target"),
    )


class AuthSession(Identity, Base):
    __tablename__ = "auth_sessions"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    refresh_hash: Mapped[str] = mapped_column(String(64), unique=True)
    csrf_hash: Mapped[str] = mapped_column(String(64))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuthAttempt(Identity, Base):
    __tablename__ = "auth_attempts"
    identifier_hash: Mapped[str] = mapped_column(String(64), index=True)
    ip_hash: Mapped[str] = mapped_column(String(64), index=True)
    __table_args__ = (Index("ix_auth_attempts_ip_time", "ip_hash", "created_at"),)


class Consent(Identity, Base):
    __tablename__ = "consents"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    purpose: Mapped[str] = mapped_column(String(40))
    version: Mapped[str] = mapped_column(String(40))
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ReferenceResource(Identity, Base):
    __tablename__ = "reference_resources"
    key: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(100))
    license: Mapped[str] = mapped_column(String(100))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    review_status: Mapped[str] = mapped_column(String(20), default="draft", server_default="draft")
    content_hash: Mapped[str | None] = mapped_column(String(64))
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Substance(Base):
    __tablename__ = "substances"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_ar: Mapped[str] = mapped_column(String(120))
    kind: Mapped[str] = mapped_column(String(20), default="food", server_default="food")


class SubstanceAlias(Identity, Base):
    __tablename__ = "substance_aliases"
    substance_id: Mapped[str] = mapped_column(ForeignKey("substances.id", ondelete="CASCADE"), index=True)
    locale: Mapped[str] = mapped_column(String(2))
    normalized_name: Mapped[str] = mapped_column(String(160))
    __table_args__ = (UniqueConstraint("locale", "normalized_name"),)


class UserRestriction(Identity, Base):
    __tablename__ = "user_restrictions"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    substance_id: Mapped[str] = mapped_column(ForeignKey("substances.id"))
    kind: Mapped[str] = mapped_column(String(20))
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    reaction: Mapped[str | None] = mapped_column(String(200))
    severity: Mapped[str | None] = mapped_column(String(24))
    provenance: Mapped[str] = mapped_column(String(40), default="self_reported")
    __table_args__ = (
        UniqueConstraint("user_id", "substance_id", "kind"),
        CheckConstraint("kind IN ('allergy','intolerance','dislike')", name="kind"),
    )


class HealthCondition(Base):
    __tablename__ = "health_conditions"
    id: Mapped[str] = mapped_column(String(60), primary_key=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_ar: Mapped[str] = mapped_column(String(120))
    module_status: Mapped[str] = mapped_column(String(20), default="not_activated")


class UserCondition(Identity, Base):
    __tablename__ = "user_conditions"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    condition_id: Mapped[str] = mapped_column(ForeignKey("health_conditions.id"))
    confirmation_status: Mapped[str] = mapped_column(String(24), default="self_reported")
    details: Mapped[dict] = mapped_column(JSONB, default=dict)
    __table_args__ = (UniqueConstraint("user_id", "condition_id"),)


class MedicationRecord(Identity, Base):
    __tablename__ = "medication_records"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reported_name: Mapped[str] = mapped_column(String(200))
    normalized_identifier: Mapped[str | None] = mapped_column(String(100))
    dose: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    unit: Mapped[str | None] = mapped_column(String(40))
    route: Mapped[str | None] = mapped_column(String(40))
    frequency: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(16), default="active")
    start_date: Mapped[date | None] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    confirmation_status: Mapped[str] = mapped_column(String(24), default="draft")
    provenance: Mapped[str] = mapped_column(String(40), default="self_reported")
    __table_args__ = (CheckConstraint("status IN ('active','past')", name="status"),)


class FoodRecord(Identity, Base):
    __tablename__ = "food_records"
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reference_resources.id"))
    external_id: Mapped[str] = mapped_column(String(100))
    __table_args__ = (UniqueConstraint("source_id", "external_id"),)


class FoodVersion(Identity, Base):
    __tablename__ = "food_versions"
    food_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("food_records.id"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    name_en: Mapped[str] = mapped_column(String(250), index=True)
    name_ar: Mapped[str] = mapped_column(String(250), index=True)
    category: Mapped[str] = mapped_column(String(40))
    preparation: Mapped[str] = mapped_column(String(200))
    data_type: Mapped[str] = mapped_column(String(100))
    source_url: Mapped[str] = mapped_column(Text)
    source_date: Mapped[str] = mapped_column(String(40))
    basis_grams: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=100)
    calories: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    protein: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    carbs: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    fat: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    fiber: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    sodium: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    ingredient_substances: Mapped[list] = mapped_column(JSONB, default=list)
    ingredient_coverage: Mapped[str] = mapped_column(String(20), default="unknown")
    source_snapshot: Mapped[dict] = mapped_column(JSONB)
    __table_args__ = (
        UniqueConstraint("food_id", "version"),
        Index("uq_food_current_version", "food_id", unique=True, postgresql_where=text("is_current")),
        CheckConstraint("basis_grams > 0 AND version > 0", name="basis_version"),
        *[
            CheckConstraint(f"{key} IS NULL OR {key} >= 0", name=key)
            for key in ("calories", "protein", "carbs", "fat", "fiber", "sodium")
        ],
    )


class Recipe(Identity, Base):
    __tablename__ = "recipes"
    owner_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str | None] = mapped_column(String(100), unique=True)
    name_en: Mapped[str] = mapped_column(String(200))
    name_ar: Mapped[str] = mapped_column(String(200))
    is_sample: Mapped[bool] = mapped_column(Boolean, default=False)
    archived: Mapped[bool] = mapped_column(Boolean, default=False)


class RecipeVersion(Identity, Base):
    __tablename__ = "recipe_versions"
    recipe_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    method_en: Mapped[str] = mapped_column(Text)
    method_ar: Mapped[str] = mapped_column(Text)
    yield_grams: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    serving_grams: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    review_status: Mapped[str] = mapped_column(String(20), default="draft")
    __table_args__ = (
        UniqueConstraint("recipe_id", "version"),
        CheckConstraint("yield_grams > 0 AND serving_grams > 0 AND version > 0", name="quantities"),
    )


class RecipeIngredient(Identity, Base):
    __tablename__ = "recipe_ingredients"
    recipe_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipe_versions.id", ondelete="CASCADE"), index=True
    )
    food_version_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("food_versions.id"))
    grams: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    __table_args__ = (CheckConstraint("grams > 0", name="grams"),)


class Meal(Identity, Base):
    __tablename__ = "meals"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(120))
    meal_type: Mapped[str] = mapped_column(String(16))
    consumed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(16), default="draft")
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    idempotency_key: Mapped[str] = mapped_column(String(128))
    request_hash: Mapped[str] = mapped_column(String(64))
    calculation_version: Mapped[str] = mapped_column(String(24), default="1")
    nutrient_snapshot: Mapped[dict] = mapped_column(JSONB)
    restriction_snapshot: Mapped[dict] = mapped_column(JSONB)
    __table_args__ = (
        UniqueConstraint("user_id", "idempotency_key"),
        UniqueConstraint("id", "user_id"),
        Index("ix_meals_diary", "user_id", "status", "consumed_at"),
        CheckConstraint("status IN ('draft','confirmed')", name="status"),
        CheckConstraint("meal_type IN ('breakfast','lunch','dinner','snack')", name="meal_type"),
    )


class MealItem(Identity, Base):
    __tablename__ = "meal_items"
    meal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    food_version_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("food_versions.id"))
    recipe_version_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("recipe_versions.id"))
    grams: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    evidence: Mapped[str] = mapped_column(String(20), default="user_entered")
    snapshot: Mapped[dict] = mapped_column(JSONB)
    __table_args__ = (
        ForeignKeyConstraint(["meal_id", "user_id"], ["meals.id", "meals.user_id"], ondelete="CASCADE"),
        CheckConstraint("grams > 0", name="grams"),
        CheckConstraint("(food_version_id IS NULL) <> (recipe_version_id IS NULL)", name="one_source"),
    )


class MediaAsset(Identity, Base):
    __tablename__ = "media_assets"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    object_key: Mapped[str] = mapped_column(Text, unique=True)
    content_type: Mapped[str] = mapped_column(String(100))
    retention_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AnalysisRun(Identity, Base):
    __tablename__ = "analysis_runs"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    media_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("media_assets.id", ondelete="SET NULL"))
    provider: Mapped[str] = mapped_column(String(100))
    model_version: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(24), default="draft")
    draft: Mapped[dict] = mapped_column(JSONB, default=dict)
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped[Decimal | None] = mapped_column(Numeric(12, 6))


class ClinicalRule(Identity, Base):
    __tablename__ = "clinical_rules"
    module: Mapped[str] = mapped_column(String(80), index=True)
    rule_key: Mapped[str] = mapped_column(String(100))
    version: Mapped[int] = mapped_column(Integer)
    source_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reference_resources.id"))
    source_location: Mapped[str] = mapped_column(Text)
    applicability: Mapped[dict] = mapped_column(JSONB)
    rule: Mapped[dict] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(24), default="draft")
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        UniqueConstraint("rule_key", "version"),
        CheckConstraint("status IN ('draft','approved','retired')", name="status"),
    )


class ClinicalDraft(Identity, Base):
    __tablename__ = "clinical_drafts"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    analysis_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("analysis_runs.id", ondelete="SET NULL"))
    kind: Mapped[str] = mapped_column(String(20))
    version: Mapped[int] = mapped_column(Integer, default=1)
    profile_revision: Mapped[int] = mapped_column(Integer)
    content: Mapped[dict] = mapped_column(JSONB)
    evidence_versions: Mapped[dict] = mapped_column(JSONB)
    content_hash: Mapped[str] = mapped_column(String(64))
    checks_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(24), default="draft", index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (
        CheckConstraint(
            "status IN ('draft','blocked','awaiting_review','approved','published','rejected','stale')",
            name="status",
        ),
    )


class ClinicalApproval(Identity, Base):
    __tablename__ = "clinical_approvals"
    draft_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clinical_drafts.id", ondelete="CASCADE"), index=True
    )
    reviewer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    draft_version: Mapped[int] = mapped_column(Integer)
    content_hash: Mapped[str] = mapped_column(String(64))
    profile_revision: Mapped[int] = mapped_column(Integer)
    decision: Mapped[str] = mapped_column(String(20))
    notes: Mapped[str | None] = mapped_column(Text)
    __table_args__ = (
        CheckConstraint("decision IN ('approved','rejected','needs_information')", name="decision"),
    )


class ReviewerAssignment(Identity, Base):
    __tablename__ = "reviewer_assignments"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    consent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("consents.id", ondelete="CASCADE"))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    __table_args__ = (UniqueConstraint("user_id", "reviewer_id"),)


class LabObservation(Identity, Base):
    __tablename__ = "lab_observations"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    test_code: Mapped[str] = mapped_column(String(100))
    value: Mapped[Decimal] = mapped_column(Numeric(16, 6))
    unit: Mapped[str] = mapped_column(String(40))
    reference_range: Mapped[dict] = mapped_column(JSONB)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    provenance: Mapped[dict] = mapped_column(JSONB)
    confirmation_status: Mapped[str] = mapped_column(String(20), default="draft")


class Subscription(Identity, Base):
    __tablename__ = "subscriptions"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(40))
    external_id: Mapped[str] = mapped_column(String(200), unique=True)
    status: Mapped[str] = mapped_column(String(24))
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class AuditEvent(Identity, Base):
    __tablename__ = "audit_events"
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    operation: Mapped[str] = mapped_column(String(80))
    resource_type: Mapped[str] = mapped_column(String(80))
    resource_id: Mapped[str | None] = mapped_column(String(100))
    __table_args__ = (Index("ix_audit_operation_time", "operation", "created_at"),)
