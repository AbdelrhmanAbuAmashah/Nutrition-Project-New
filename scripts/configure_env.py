"""Generate local credentials once; never prints secrets or overwrites existing values."""
import os
import secrets
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / ".env"
existing = path.read_text() if path.exists() else ""
keys = {line.split("=", 1)[0] for line in existing.splitlines() if "=" in line and not line.startswith("#")}
defaults = {
    "COMPOSE_PROJECT_NAME": "nour",
    "POSTGRES_ADMIN_PASSWORD": secrets.token_hex(32),
    "MIGRATION_DB_PASSWORD": secrets.token_hex(32),
    "APP_DB_PASSWORD": secrets.token_hex(32),
    "JWT_SECRET": secrets.token_hex(48),
    "WEB_PORT": "3000", "API_PORT": "8000", "DB_PORT": "54329",
    "ENVIRONMENT": "development", "COOKIE_SECURE": "false",
    "ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000,http://web:3000",
    "ALLOWED_HOSTS": "localhost,127.0.0.1,api,testserver",
}
addition = "".join(f"{key}={value}\n" for key, value in defaults.items() if key not in keys)
if addition:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(descriptor, "w") as output:
        if existing and not existing.endswith("\n"):
            output.write("\n")
        output.write(addition)
    path.chmod(0o600)
print("Local environment ready; existing configuration preserved. Secrets were not displayed.")
