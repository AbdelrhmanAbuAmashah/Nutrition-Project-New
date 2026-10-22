import hashlib
import hmac
import secrets
import uuid
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, Request, Response
from pwdlib import PasswordHash
from sqlalchemy import delete, func, select, text
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.errors import AppError
from app.models import AuthAttempt, AuthSession, User

passwords = PasswordHash.recommended()
DUMMY_HASH = passwords.hash("constant-timing-dummy-password-not-a-user")
ACCESS_COOKIE = "nour_access"
REFRESH_COOKIE = "nour_refresh"
CSRF_COOKIE = "nour_csrf"


def now():
    return datetime.now(UTC)


def digest(value: str):
    return hashlib.sha256(value.encode()).hexdigest()


def rate_check(request: Request, db: Session, email: str):
    settings = get_settings()
    # Do not trust a client-supplied X-Forwarded-For header. Configure the edge/proxy explicitly.
    ip = request.client.host if request.client else "unknown"
    identity = hmac.new(settings.jwt_secret.encode(), email.lower().encode(), "sha256").hexdigest()
    ip_hash = hmac.new(settings.jwt_secret.encode(), ip.encode(), "sha256").hexdigest()
    cutoff = now() - timedelta(minutes=settings.auth_rate_window_minutes)
    # Transaction locks keep the counters correct across concurrent requests and API workers.
    lock_keys = sorted(
        {int.from_bytes(bytes.fromhex(value[:16]), "big", signed=True) for value in (identity, ip_hash)}
    )
    for key in lock_keys:
        db.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": key})
    identity_count = db.scalar(
        select(func.count())
        .select_from(AuthAttempt)
        .where(
            AuthAttempt.created_at > cutoff,
            AuthAttempt.identifier_hash == identity,
        )
    )
    ip_count = db.scalar(
        select(func.count())
        .select_from(AuthAttempt)
        .where(AuthAttempt.created_at > cutoff, AuthAttempt.ip_hash == ip_hash)
    )
    if identity_count >= settings.login_limit or ip_count >= settings.ip_login_limit:
        raise AppError("rate_limit", 429)
    db.execute(delete(AuthAttempt).where(AuthAttempt.created_at < now() - timedelta(days=1)))
    db.add(AuthAttempt(identifier_hash=identity, ip_hash=ip_hash))
    db.commit()


def set_session_cookies(response: Response, user: User, auth: AuthSession, refresh: str, csrf: str):
    settings = get_settings()
    issued = now()
    token = jwt.encode(
        {
            "sub": str(user.id),
            "sid": str(auth.id),
            "jti": str(uuid.uuid4()),
            "iat": issued,
            "exp": issued + timedelta(minutes=settings.access_minutes),
            "iss": settings.jwt_issuer,
            "aud": settings.jwt_audience,
            "type": "access",
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    common = {"secure": settings.cookie_secure, "samesite": "lax"}
    response.set_cookie(
        ACCESS_COOKIE, token, httponly=True, path="/api/v1", max_age=settings.access_minutes * 60, **common
    )
    remaining = max(0, int((auth.expires_at - issued).total_seconds()))
    response.set_cookie(
        REFRESH_COOKIE, refresh, httponly=True, path="/api/v1/auth", max_age=remaining, **common
    )
    response.set_cookie(CSRF_COOKIE, csrf, httponly=False, path="/", max_age=remaining, **common)
    response.headers["Cache-Control"] = "no-store"


def new_session(response: Response, db: Session, user: User):
    refresh, csrf = secrets.token_urlsafe(48), secrets.token_urlsafe(32)
    auth = AuthSession(
        user_id=user.id,
        refresh_hash=digest(refresh),
        csrf_hash=digest(csrf),
        expires_at=now() + timedelta(days=get_settings().session_days),
    )
    db.add(auth)
    db.commit()
    set_session_cookies(response, user, auth, refresh, csrf)


def check_csrf(request: Request, auth: AuthSession):
    cookie = request.cookies.get(CSRF_COOKIE, "")
    header = request.headers.get("x-csrf-token", "")
    if (
        not cookie
        or not hmac.compare_digest(cookie, header)
        or not hmac.compare_digest(digest(header), auth.csrf_hash)
    ):
        raise AppError("csrf", 403)


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(ACCESS_COOKIE)
    if not token:
        raise AppError("auth_required", 401)
    settings = get_settings()
    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
            options={"require": ["exp", "iat", "sub", "sid", "jti", "type"]},
        )
        if claims["type"] != "access":
            raise ValueError("type")
        auth = db.get(AuthSession, uuid.UUID(claims["sid"]))
        user_id = uuid.UUID(claims["sub"])
    except (jwt.PyJWTError, ValueError, TypeError, KeyError) as error:
        raise AppError("session_expired", 401) from error
    if not auth or auth.revoked_at or auth.expires_at <= now() or auth.user_id != user_id:
        raise AppError("session_expired", 401)
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise AppError("auth_required", 401)
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        check_csrf(request, auth)
    request.state.auth_session = auth
    return user


def clear_cookies(response: Response):
    for name, path in [(ACCESS_COOKIE, "/api/v1"), (REFRESH_COOKIE, "/api/v1/auth"), (CSRF_COOKIE, "/")]:
        response.delete_cookie(name, path=path, secure=get_settings().cookie_secure, samesite="lax")
