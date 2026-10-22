from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    database_url: str = "postgresql+psycopg://nour_app:local-only@localhost:54329/nour"
    jwt_secret: str = Field(min_length=32)
    jwt_issuer: str = "nour-api"
    jwt_audience: str = "nour-web"
    access_minutes: int = Field(default=15, ge=1, le=60)
    session_days: int = Field(default=14, ge=1, le=90)
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    allowed_hosts: str = "localhost,127.0.0.1,api,testserver"
    cookie_secure: bool = False
    login_limit: int = Field(default=15, ge=3, le=100)
    ip_login_limit: int = Field(default=300, ge=20, le=5000)
    auth_rate_window_minutes: int = 15

    @property
    def origins(self) -> list[str]:
        return [value.strip().rstrip("/") for value in self.allowed_origins.split(",") if value.strip()]

    @property
    def hosts(self) -> list[str]:
        return [value.strip() for value in self.allowed_hosts.split(",") if value.strip()]

    @model_validator(mode="after")
    def validate_security(self):
        if "*" in self.origins:
            raise ValueError("CORS requires explicit origins")
        if not self.database_url.startswith("postgresql"):
            raise ValueError("PostgreSQL is required")
        if self.environment == "production":
            if not self.cookie_secure or any(not origin.startswith("https://") for origin in self.origins):
                raise ValueError("Production requires secure cookies and HTTPS origins")
            if "*" in self.hosts:
                raise ValueError("Production requires explicit host names")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
