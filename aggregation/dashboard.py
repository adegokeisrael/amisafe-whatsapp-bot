"""
Aggregation layer for AmiSafe.

Provides:
  - Public-facing aggregate statistics (no individual report data ever exposed)
  - Partner export of anonymised reports at ANONYMOUS_RESEARCH / VERIFIED_PARTNER
    disclosure levels

This module enforces the core privacy guarantee of AmiSafe:
individual reports are never exposed outside the encrypted store except
in aggregate or fully anonymised form, and only to API-key-authenticated
partners.
"""

from collections import Counter
from database.db import get_db
from database.models import Report, DisclosureLevel
from privacy.anonymiser import decrypt


def get_aggregate_stats() -> dict:
    """
    Returns counts by harm type, language, region, and platform.
    No individual report content is included.
    """
    with get_db() as db:
        reports = db.query(Report).all()

        total = len(reports)
        by_harm_type = Counter(r.harm_type for r in reports)
        by_language = Counter(r.language for r in reports)
        by_region = Counter(r.region_code or "XX" for r in reports)
        by_platform = Counter(r.platform_hint for r in reports if r.platform_hint)

        with_evidence = sum(1 for r in reports if r.evidence_type and r.evidence_type != "none")
        evidence_integrity_rate = round((with_evidence / total) * 100, 1) if total else 0.0

        return {
            "total_reports": total,
            "by_harm_type": dict(by_harm_type),
            "by_language": dict(by_language),
            "by_region": dict(by_region),
            "by_platform": dict(by_platform),
            "evidence_integrity_rate_pct": evidence_integrity_rate,
        }


def export_reports(disclosure_level: str) -> dict:
    """
    Export anonymised reports for a vetted partner.

    Only ANONYMOUS_RESEARCH and VERIFIED_PARTNER levels are ever stored
    server-side, so this is the maximum scope of what can be exported.
    Description text is decrypted server-side and returned already
    anonymised (PII was stripped before encryption at submission time).
    """
    valid_levels = {DisclosureLevel.ANONYMOUS_RESEARCH, DisclosureLevel.VERIFIED_PARTNER}
    if disclosure_level not in valid_levels:
        return {"error": f"disclosure_level must be one of {[l.value for l in valid_levels]}"}

    with get_db() as db:
        reports = db.query(Report).filter_by(disclosure_level=disclosure_level).all()

        results = []
        for r in reports:
            description = None
            if r.description_encrypted:
                try:
                    description = decrypt(r.description_encrypted)
                except Exception:
                    description = "[decryption error]"

            transcript = None
            if r.transcript_encrypted:
                try:
                    transcript = decrypt(r.transcript_encrypted)
                except Exception:
                    transcript = "[decryption error]"

            results.append({
                "report_id": r.id,
                "harm_type": r.harm_type,
                "language": r.language,
                "description": description,
                "transcript": transcript,
                "evidence_type": r.evidence_type,
                "evidence_hash": r.evidence_hash,
                "platform_hint": r.platform_hint,
                "region_code": r.region_code,
                "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None,
                "is_verified": r.is_verified,
            })

        return {
            "disclosure_level": disclosure_level,
            "count": len(results),
            "reports": results,
        }
