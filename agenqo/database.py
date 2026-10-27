"""Agenqo data ownership: existing MySQL is operational source of truth.

No PostgreSQL runtime. DuckDB is only optional embedded analytics.
SQLite is permitted only in explicitly enabled local/unit-test contexts.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

def configured_database_url() -> str:
    url = os.environ.get("AGENQO_DATABASE_URL", "")
    if not url:
        if os.environ.get("AGENQO_ALLOW_SQLITE_DEV") == "1":
            return "sqlite:///./agenqo_dev.db"
        raise RuntimeError(
            "AGENQO_DATABASE_URL is required; use existing MySQL "
            "(mysql+pymysql://...), or opt into SQLite for local tests.")
    parsed = make_url(url)
    if parsed.get_backend_name() not in {"mysql", "mariadb", "sqlite"}:
        raise RuntimeError("Unsupported database; configure MySQL or explicit local SQLite")
    if parsed.get_backend_name() == "sqlite" and os.environ.get("AGENQO_ALLOW_SQLITE_DEV") != "1":
        raise RuntimeError("SQLite is allowed only when AGENQO_ALLOW_SQLITE_DEV=1")
    return url

DATABASE_URL = configured_database_url()
backend = make_url(DATABASE_URL).get_backend_name()
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"check_same_thread": False} if backend == "sqlite" else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
