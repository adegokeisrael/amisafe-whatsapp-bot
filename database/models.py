"""
Database models for AmiSafe.

Design principles:
- Phone numbers are NEVER stored in plaintext. Only HMAC-SHA256 hashes.
- All report content is encrypted at rest via Fernet symmetric encryption.
- Report IDs are pseudonymous UUIDs with no link to real identity.
- Evidence is stored as an encrypted hash + metadata, not raw content.
"""

from sqlalchemy import (
    Column, String, Integer, DateTime, Text, Boolean, JSON, Enum
)
from sqlalchemy.orm import DeclarativeBase
from utils import utcnow
import enum

# NOTE: We deliberately use naive UTC datetimes (via utils.utcnow) throughout
# this module rather than timezone-aware datetimes (datetime.now(timezone.utc)).
# SQLite silently drops tzinfo on round-trip, which causes
# "can't compare offset-naive and offset-aware datetimes" errors if one side
# of a comparison is aware and the other naive after a DB read. Keeping
# everything naive-but-UTC avoids this class of bug across both SQLite (dev)
# and PostgreSQL (prod, assuming TIMESTAMP WITHOUT TIME ZONE columns).


class Base(DeclarativeBase):
    pass


class ConversationState(str, enum.Enum):
    START = "START"
    LANGUAGE_SELECTION = "LANGUAGE_SELECTION"
    HARM_TYPE_SELECTION = "HARM_TYPE_SELECTION"
    DESCRIPTION = "DESCRIPTION"
    EVIDENCE_REQUEST = "EVIDENCE_REQUEST"
    EVIDENCE_RECEIVED = "EVIDENCE_RECEIVED"
    DISCLOSURE_LEVEL = "DISCLOSURE_LEVEL"
    CONFIRMATION = "CONFIRMATION"
    COMPLETE = "COMPLETE"


class DisclosureLevel(str, enum.Enum):
    PRIVATE = "PRIVATE"
    ANONYMOUS_RESEARCH = "ANONYMOUS_RESEARCH"
    VERIFIED_PARTNER = "VERIFIED_PARTNER"


class HarmType(str, enum.Enum):
    FAKE_IMAGE_OR_VIDEO = "FAKE_IMAGE_OR_VIDEO"
    FALSE_INFORMATION = "FALSE_INFORMATION"
    UNFAIR_TREATMENT = "UNFAIR_TREATMENT"
    HARASSMENT_OR_INTIMIDATION = "HARASSMENT_OR_INTIMIDATION"
    FINANCIAL_HARM = "FINANCIAL_HARM"
    OTHER = "OTHER"


class Session(Base):
    """
    Tracks conversation state per reporter.
    Keyed to hashed phone number so we can resume a conversation,
    but cannot reconstruct the real number.
    """
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)            # pseudonymous session UUID
    phone_hash = Column(String, unique=True, index=True)  # HMAC-SHA256 of phone number
    state = Column(String, default=ConversationState.START)
    language = Column(String, nullable=True)
    harm_type = Column(String, nullable=True)
    description_encrypted = Column(Text, nullable=True)   # encrypted at rest
    evidence_path = Column(String, nullable=True)          # temp path, cleared after DB write
    evidence_hash = Column(String, nullable=True)          # SHA-256 of evidence file
    evidence_type = Column(String, nullable=True)          # image / audio / text
    disclosure_level = Column(String, nullable=True)
    report_id = Column(String, nullable=True)              # links to Report once submitted
    created_at = Column(DateTime, default=lambda: utcnow())
    updated_at = Column(DateTime, default=lambda: utcnow(),
                        onupdate=lambda: utcnow())
    expires_at = Column(DateTime, nullable=True)


class Report(Base):
    """
    Final structured AI harm report.
    Content fields are Fernet-encrypted.
    Only ANONYMOUS_RESEARCH and VERIFIED_PARTNER reports are stored here
    (PRIVATE reports are confirmed to the user but not persisted server-side).
    """
    __tablename__ = "reports"

    id = Column(String, primary_key=True)            # pseudonymous report UUID
    session_id = Column(String, index=True)          # links to Session
    harm_type = Column(String, nullable=False)
    language = Column(String, nullable=False)
    description_encrypted = Column(Text, nullable=True)
    evidence_hash = Column(String, nullable=True)    # SHA-256 of original evidence
    evidence_type = Column(String, nullable=True)
    transcript_encrypted = Column(Text, nullable=True)  # for voice notes
    disclosure_level = Column(String, nullable=False)
    platform_hint = Column(String, nullable=True)    # e.g. "Twitter/X", "Facebook" — user-provided
    region_code = Column(String, nullable=True)      # derived from phone prefix, e.g. "NG", "KE"
    submitted_at = Column(DateTime, default=lambda: utcnow())
    is_verified = Column(Boolean, default=False)     # set by community moderation layer
    is_flagged = Column(Boolean, default=False)      # flagged for review
    moderation_notes = Column(Text, nullable=True)


class AggregateSnapshot(Base):
    """
    Pre-computed aggregate statistics exported to the public dashboard.
    Never contains individual report data.
    """
    __tablename__ = "aggregate_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_date = Column(DateTime, default=lambda: utcnow())
    total_reports = Column(Integer, default=0)
    by_harm_type = Column(JSON, default=dict)        # {harm_type: count}
    by_language = Column(JSON, default=dict)         # {language_code: count}
    by_region = Column(JSON, default=dict)           # {region_code: count}
    by_platform = Column(JSON, default=dict)         # {platform: count}
    evidence_integrity_rate = Column(Integer, default=0)  # % with attached evidence
