"""
Shared utilities for AmiSafe.
"""
from datetime import datetime, timezone


def utcnow() -> datetime:
    """
    Return the current UTC time as a naive datetime (no tzinfo).

    We use naive-but-UTC datetimes everywhere rather than timezone-aware
    ones because SQLite silently drops tzinfo on round-trip through the
    database. Mixing aware and naive datetimes after a DB read raises
    TypeError on comparison. Keeping everything naive avoids this class
    of bug consistently across SQLite (dev) and PostgreSQL (prod, assuming
    TIMESTAMP WITHOUT TIME ZONE columns).
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
