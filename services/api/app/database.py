from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings


@lru_cache
def engine():
    return create_engine(get_settings().database_url, pool_pre_ping=True, pool_size=5, max_overflow=10)


def get_db():
    with Session(engine(), expire_on_commit=False) as session:
        yield session


def session_factory():
    return sessionmaker(engine(), expire_on_commit=False)
