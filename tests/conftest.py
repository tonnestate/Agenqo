"""Enable SQLite only as a fallback for isolated local unit tests.
CI sets AGENQO_DATABASE_URL to the MySQL 8.4 test service.
"""
import os

if not os.environ.get("AGENQO_DATABASE_URL"):
    os.environ["AGENQO_ALLOW_SQLITE_DEV"] = "1"
    os.environ["AGENQO_DATABASE_URL"] = "sqlite:///./agenqo_dev.db"
