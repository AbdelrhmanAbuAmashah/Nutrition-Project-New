import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace

import jwt
import pytest
from conftest import register
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.calculations import check_restrictions, portion, total
from app.clinical import approval_allows_publication
from app.config import Settings, get_settings
from app.database import engine
from app.main import app
from app.meals import day_bounds
from app.models import AuthSession, FoodVersion, Meal, User
from app.security import now
from app.seed import seed


def create(client, payload, key=None):
    return client.post("/api/v1/meals", json=payload, headers={"Idempotency-Key": key or str(uuid.uuid4())})


def test_simultaneous_saves_and_confirms_create_one_record(client, meal_payload):
    key = str(uuid.uuid4())
    with ThreadPoolExecutor(max_workers=6) as workers:
        responses = list(workers.map(lambda _: create(client, meal_payload, key), range(6)))
    assert all(response.status_code == 201 for response in responses)
    ids = {response.json()["id"] for response in responses}
    assert len(ids) == 1
    meal_id = ids.pop()
    with ThreadPoolExecutor(max_workers=4) as workers:
        confirmations = list(workers.map(lambda _: client.post(f"/api/v1/meals/{meal_id}/confirm"), range(4)))
    assert all(response.status_code == 200 for response in confirmations)
    with Session(engine()) as db:
        assert db.scalar(select(func.count()).select_from(Meal)) == 1
    diary = client.get("/api/v1/diary?day=2026-10-22").json()
    assert len(diary["meals"]) == 1
    assert diary["nutrition"]["values"]["calories"] == "195.00"


def test_password_whitespace_is_significant(client):
    payload = {
        "email": "spacing@example.com",
        "display_name": "Amal",
        "locale": "en",
        "password": "  Meaningful Password!42  ",
        "accept_privacy": True,
    }
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": payload["email"],
                "password": payload["password"].strip(),
            },
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={
                "email": payload["email"],
                "password": payload["password"],
            },
        ).status_code
        == 200
    )


def test_production_configuration_requires_https_secure_cookies_and_exact_origins():
    with pytest.raises(ValueError):
        Settings(environment="production", cookie_secure=False, allowed_origins="https://nour.example")
    with pytest.raises(ValueError):
        Settings(environment="production", cookie_secure=True, allowed_origins="http://nour.example")
    with pytest.raises(ValueError):
        Settings(cookie_secure=True, allowed_origins="*")
    assert Settings(
        environment="production",
        cookie_secure=True,
        allowed_origins="https://nour.example",
        allowed_hosts="nour.example,api",
    ).cookie_secure


def confirm(client, payload):
    result = create(client, payload)
    assert result.status_code == 201, result.text
    result = client.post(f"/api/v1/meals/{result.json()['id']}/confirm")
    assert result.status_code == 200, result.text
    return result.json()


def test_health_and_catalog_are_protected(client):
    assert client.get("/health").json()["database"] == "ready"
    assert client.get("/api/v1/foods").status_code == 401
    assert client.get("/api/v1/profile").status_code == 401


def test_registration_password_hash_and_cookie_security(client):
    profile = register(client)
    with Session(engine()) as db:
        user = db.get(User, uuid.UUID(profile["user"]["id"]))
        assert user.password_hash.startswith("$argon2id$")
        assert "CorrectHorse" not in user.password_hash
    response = client.post(
        "/api/v1/auth/login", json={"email": "ALICE@example.com", "password": "CorrectHorse!42"}
    )
    assert response.status_code == 200
    cookies = response.headers.get_list("set-cookie")
    assert any("nour_access=" in c and "HttpOnly" in c and "SameSite=lax" in c for c in cookies)
    assert any("nour_refresh=" in c and "HttpOnly" in c for c in cookies)
    assert "password_hash" not in response.text and "refresh_hash" not in response.text


def test_registration_does_not_accept_privileges_or_weak_password(client):
    payload = {
        "email": "alice@example.com",
        "display_name": "Alice",
        "password": "short",
        "accept_privacy": True,
        "role": "admin",
    }
    result = client.post("/api/v1/auth/register", json=payload)
    assert result.status_code == 422
    assert '"input"' not in result.text and '"password":"short"' not in result.text
    payload.pop("role")
    payload.update(password="CorrectHorse!42", accept_privacy=False)
    assert client.post("/api/v1/auth/register", json=payload).json()["error"]["code"] == "consent_required"


def test_bad_credentials_are_localized(client, member):
    response = client.post(
        "/api/v1/auth/login",
        headers={"Accept-Language": "ar"},
        json={"email": "alice@example.com", "password": "incorrect-password"},
    )
    assert response.status_code == 401
    assert "غير صحيحة" in response.json()["error"]["message"]
    assert response.json()["error"]["request_id"]


def test_login_is_rate_limited(client):
    payload = {"email": "nobody@example.com", "password": "incorrect-password"}
    for _ in range(get_settings().login_limit):
        assert client.post("/api/v1/auth/login", json=payload).status_code == 401
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 429 and response.headers["retry-after"] == "900"


def test_csrf_and_foreign_origins_are_rejected(client, member):
    client.headers.pop("X-CSRF-Token")
    assert client.post("/api/v1/auth/logout").status_code == 403
    client.headers["X-CSRF-Token"] = client.cookies.get("nour_csrf")
    assert client.post("/api/v1/auth/logout", headers={"Origin": "https://evil.example"}).status_code == 403
    assert (
        client.get("/api/v1/profile", headers={"Origin": "https://evil.example"}).headers.get(
            "access-control-allow-origin"
        )
        is None
    )


def test_jwt_tampering_and_wrong_audience_fail(client, member):
    original = client.cookies.get("nour_access")
    client.cookies.set("nour_access", original[:-8] + "badtoken", domain="testserver.local", path="/api/v1")
    assert client.get("/api/v1/auth/me").status_code == 401
    claims = jwt.decode(original, get_settings().jwt_secret, algorithms=["HS256"], audience="nour-web")
    claims["aud"] = "another-app"
    client.cookies.set(
        "nour_access",
        jwt.encode(claims, get_settings().jwt_secret, algorithm="HS256"),
        domain="testserver.local",
        path="/api/v1",
    )
    assert client.get("/api/v1/auth/me").status_code == 401


def test_refresh_rotates_and_old_refresh_cannot_be_reused(client, member):
    old = client.cookies.get("nour_refresh")
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 200
    assert client.cookies.get("nour_refresh") != old
    client.headers["X-CSRF-Token"] = client.cookies.get("nour_csrf")
    client.cookies.set("nour_refresh", old, domain="testserver.local", path="/api/v1/auth")
    assert client.post("/api/v1/auth/refresh").status_code == 401


def test_logout_revokes_access_even_if_token_is_replayed(client, member):
    token = client.cookies.get("nour_access")
    assert client.post("/api/v1/auth/logout").status_code == 204
    client.cookies.set("nour_access", token, domain="testserver.local", path="/api/v1")
    assert client.get("/api/v1/auth/me").status_code == 401


def test_session_expiry_is_enforced(client, member):
    with Session(engine()) as db:
        session = db.scalar(select(AuthSession))
        session.expires_at = now() - timedelta(seconds=1)
        db.commit()
    assert client.get("/api/v1/auth/me").status_code == 401


def test_traceable_seed_search_and_idempotent_seed(client, member):
    foods = client.get("/api/v1/foods").json()["items"]
    assert len(foods) == 19
    assert all(
        f["source"]["external_id"] and f["source"]["url"].startswith("https://fdc.nal.usda.gov/")
        for f in foods
    )
    assert client.get("/api/v1/foods?q=عدس").json()["count"] == 2
    assert client.get("/api/v1/foods?q=%25").json()["count"] == 0
    with Session(engine()) as db:
        seed(db)
        assert db.scalar(select(func.count()).select_from(FoodVersion)) == 19
        assert db.scalar(select(func.count()).select_from(User)) == 1


def test_preview_uses_server_values_and_does_not_save(client, meal_payload):
    result = client.post("/api/v1/meals/preview", json=meal_payload)
    assert result.status_code == 200
    assert result.json()["nutrition"]["values"]["calories"] == "195.00"
    assert result.json()["items"][0]["source"]["source"]["external_id"] == "168878"
    with Session(engine()) as db:
        assert db.scalar(select(func.count()).select_from(Meal)) == 0


def test_confirmed_only_diary_and_duplicate_confirm(client, meal_payload):
    created = create(client, meal_payload).json()
    assert client.get("/api/v1/diary?day=2026-10-22").json()["meals"] == []
    path = f"/api/v1/meals/{created['id']}/confirm"
    assert client.post(path).status_code == client.post(path).status_code == 200
    diary = client.get("/api/v1/diary?day=2026-10-22").json()
    assert len(diary["meals"]) == 1
    assert diary["nutrition"]["values"]["calories"] == "195.00"


def test_repeated_save_is_idempotent_and_changed_body_conflicts(client, meal_payload):
    key = str(uuid.uuid4())
    first, second = create(client, meal_payload, key), create(client, meal_payload, key)
    assert first.status_code == second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
    meal_payload["title"] = "Different lunch"
    assert create(client, meal_payload, key).status_code == 409


@pytest.mark.parametrize("grams", ["0", "-1", "10001", "NaN", "Infinity", "1.1234"])
def test_invalid_quantities_are_rejected(client, meal_payload, grams):
    meal_payload["items"][0]["grams"] = grams
    assert create(client, meal_payload).status_code == 422


def test_food_or_recipe_required_and_timezone_required(client, meal_payload):
    meal_payload["items"][0]["recipe_version_id"] = str(uuid.uuid4())
    assert create(client, meal_payload).status_code == 422
    meal_payload["items"][0].pop("recipe_version_id")
    meal_payload["consumed_at"] = "2026-10-22T10:00:00"
    assert create(client, meal_payload).status_code == 422


def test_missing_values_remain_unknown(client, meal_payload):
    food_id = uuid.UUID(meal_payload["items"][0]["food_version_id"])
    with Session(engine()) as db:
        db.get(FoodVersion, food_id).fiber = None
        db.commit()
    meal = confirm(client, meal_payload)
    assert meal["nutrition"]["values"]["fiber"] is None
    diary = client.get("/api/v1/diary?day=2026-10-22").json()
    assert diary["nutrition"]["values"]["fiber"] is None
    assert "fiber" in diary["nutrition"]["missing"]


def test_source_changes_do_not_recalculate_history(client, meal_payload):
    meal = confirm(client, meal_payload)
    with Session(engine()) as db:
        db.get(FoodVersion, uuid.UUID(meal_payload["items"][0]["food_version_id"])).calories = Decimal("999")
        db.commit()
    assert client.get(f"/api/v1/meals/{meal['id']}").json()["nutrition"]["values"]["calories"] == "195.00"


def test_cross_user_meal_access_is_hidden(client, meal_payload):
    meal = confirm(client, meal_payload)
    with TestClient(app) as other:
        register(other, "other@example.com")
        assert other.get(f"/api/v1/meals/{meal['id']}").status_code == 404
        assert other.post(f"/api/v1/meals/{meal['id']}/confirm").status_code == 404
        assert other.delete(f"/api/v1/meals/{meal['id']}").status_code == 404
        assert other.get("/api/v1/diary?day=2026-10-22").json()["meals"] == []


def profile_payload(member):
    return {
        k: member[k]
        for k in [
            "locale",
            "country",
            "timezone",
            "units",
            "goal",
            "target_origin",
            "calorie_target",
            "protein_target",
            "carbs_target",
            "fat_target",
            "allergy_status",
            "preferences",
            "revision",
            "conditions",
        ]
    } | {"display_name": member["user"]["display_name"], "restrictions": [], "complete_onboarding": True}


def test_profile_revision_and_confirmed_restrictions(client, member):
    payload = profile_payload(member)
    payload.update(allergy_status="recorded", restrictions=[{"substance_id": "egg", "kind": "allergy"}])
    response = client.patch("/api/v1/profile", json=payload)
    assert response.status_code == 200, response.text
    assert response.json()["revision"] == 2 and response.json()["restrictions"][0]["confirmed"]
    assert client.patch("/api/v1/profile", json=payload).status_code == 409
    egg = client.get("/api/v1/foods?q=whole%20egg").json()["items"][0]
    preview = client.post(
        "/api/v1/meals/preview",
        json={
            "title": "Egg",
            "meal_type": "breakfast",
            "consumed_at": "2026-10-22T08:00:00Z",
            "items": [{"food_version_id": egg["id"], "grams": 100}],
        },
    ).json()
    assert preview["restrictions"]["status"] == "conflict"
    assert preview["restrictions"]["recommendation_eligible"] is False


def test_profile_does_not_accept_unknown_substance_or_invalid_timezone(client, member):
    payload = profile_payload(member)
    payload.update(allergy_status="recorded", restrictions=[{"substance_id": "invented", "kind": "allergy"}])
    assert client.patch("/api/v1/profile", json=payload).status_code == 422
    payload.update(restrictions=[], allergy_status="none", timezone="not/a/timezone")
    assert client.patch("/api/v1/profile", json=payload).status_code == 422


def test_timezone_midnight_uses_user_day(client, member, meal_payload):
    meal_payload["consumed_at"] = "2026-10-21T22:30:00Z"
    confirm(client, meal_payload)
    assert len(client.get("/api/v1/diary?day=2026-10-22").json()["meals"]) == 1
    assert len(client.get("/api/v1/diary?day=2026-10-21").json()["meals"]) == 0


def test_timezone_day_can_be_23_hours():
    from datetime import date

    start, end = day_bounds(date(2026, 3, 8), "America/New_York")
    assert (end - start).total_seconds() == 23 * 3600


def test_local_recipes_use_yield_and_source_ingredients(client, member):
    recipes = client.get("/api/v1/recipes").json()["items"]
    assert len(recipes) == 3
    recipe = recipes[0]
    payload = {
        "title": "Sample recipe",
        "meal_type": "lunch",
        "consumed_at": "2026-10-22T10:00:00Z",
        "items": [{"recipe_version_id": recipe["id"], "grams": recipe["serving_grams"]}],
    }
    meal = confirm(client, payload)
    assert meal["nutrition"]["values"]["calories"] == recipe["nutrients"]["calories"]
    assert all(i["food"]["source"]["external_id"] for i in meal["items"][0]["source"]["ingredients"])


def test_export_and_account_deletion_cascade(client, member, meal_payload):
    confirm(client, meal_payload)
    exported = client.get("/api/v1/account/export")
    assert exported.status_code == 200 and len(exported.json()["meals"]) == 1
    assert not any(key in exported.text for key in ["password_hash", "refresh_hash", "csrf_hash"])
    assert client.request("DELETE", "/api/v1/account", json={"password": "wrong-password"}).status_code == 401
    response = client.request("DELETE", "/api/v1/account", json={"password": "CorrectHorse!42"})
    assert response.status_code == 204, response.text
    assert client.get("/api/v1/auth/me").status_code == 401
    with Session(engine()) as db:
        assert db.scalar(select(func.count()).select_from(User)) == 0
        assert db.scalar(select(func.count()).select_from(Meal)) == 0


def test_no_clinical_endpoint_publishes_unreviewed_content(client, member):
    assert client.get("/api/v1/clinical/plans").status_code == 404


def test_clinical_guard_binds_content_version_and_profile_revision():
    draft = SimpleNamespace(
        id=uuid.uuid4(),
        version=1,
        content_hash="a" * 64,
        profile_revision=1,
        checks_passed=True,
        status="approved",
    )
    profile = SimpleNamespace(revision=1)
    approval = SimpleNamespace(
        draft_id=draft.id,
        draft_version=1,
        content_hash="a" * 64,
        profile_revision=1,
        decision="approved",
        reviewer_id=uuid.uuid4(),
    )
    assert approval_allows_publication(draft, None, profile) is False
    assert approval_allows_publication(draft, approval, profile) is True
    draft.content_hash = "b" * 64
    assert approval_allows_publication(draft, approval, profile) is False
    draft.content_hash = "a" * 64
    profile.revision = 2
    assert approval_allows_publication(draft, approval, profile) is False


def test_decimal_calculation_missing_data_and_unknown_restrictions():
    assert portion({"calories": "100"}, Decimal("33.333"))["calories"] == Decimal("33.333")
    assert (
        total([{"calories": Decimal("1.005")}, {"calories": Decimal("1.005")}])["values"]["calories"]
        == "2.01"
    )
    check = check_restrictions(set(), "unknown", [], "none")
    assert check["status"] == "unknown" and not check["recommendation_eligible"]
