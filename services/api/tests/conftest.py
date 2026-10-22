import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

os.environ.setdefault("JWT_SECRET", "isolated-test-secret-longer-than-thirty-two-characters")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("ALLOWED_ORIGINS", "http://testserver,http://localhost:3000")

from app.database import engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Base  # noqa: E402
from app.seed import seed  # noqa: E402


@pytest.fixture(autouse=True)
def clean_test_database():
    if not (make_url(str(engine().url)).database or "").endswith("_test"):
        raise RuntimeError("Tests require an isolated PostgreSQL database with a name ending _test")
    with engine().begin() as connection:
        tables = ", ".join('"' + table + '"' for table in Base.metadata.tables)
        connection.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    with Session(engine()) as db:
        seed(db)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def register(client, email="alice@example.com"):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "CorrectHorse!42",
            "display_name": "Amal",
            "locale": "en",
            "accept_privacy": True,
        },
    )
    assert response.status_code == 201, response.text
    client.headers["X-CSRF-Token"] = client.cookies.get("nour_csrf")
    return response.json()


@pytest.fixture
def member(client):
    return register(client)


@pytest.fixture
def meal_payload(client, member):
    food = client.get("/api/v1/foods?q=rice").json()["items"][0]
    return {
        "title": "Lunch",
        "meal_type": "lunch",
        "consumed_at": "2026-10-22T10:00:00Z",
        "items": [{"food_version_id": food["id"], "grams": "150", "evidence": "weighed"}],
    }
