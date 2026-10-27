"""Versioned migrations: existing MySQL; SQLite explicitly allowed in tests."""
import os
from alembic import context
from sqlalchemy import create_engine, pool
from agenqo.models import Base

config = context.config
target_metadata = Base.metadata

def migration_url():
    url = os.getenv("AGENQO_DATABASE_URL", "")
    if not url:
        if os.getenv("AGENQO_ALLOW_SQLITE_DEV") == "1":
            return "sqlite:///./agenqo_dev.db"
        raise RuntimeError("AGENQO_DATABASE_URL required for migrations")
    from sqlalchemy.engine import make_url
    dialect = make_url(url).get_backend_name()
    if dialect not in {"mysql", "mariadb", "sqlite"}:
        raise RuntimeError("MySQL required; other DB engines not configured")
    if dialect == "sqlite" and os.getenv("AGENQO_ALLOW_SQLITE_DEV") != "1":
        raise RuntimeError("SQLite migrations require AGENQO_ALLOW_SQLITE_DEV=1")
    return url

def run_migrations_online():
    connectable = create_engine(migration_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    context.configure(url=migration_url(), target_metadata=target_metadata,
                      literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
