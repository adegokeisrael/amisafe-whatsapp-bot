"""
Unit tests for AmiSafe privacy and anonymisation logic.

Run with:
    pytest tests/ -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("WHATSAPP_TOKEN", "test_token")
os.environ.setdefault("WHATSAPP_PHONE_NUMBER_ID", "test_id")
os.environ.setdefault("VERIFY_TOKEN", "test_verify")
os.environ.setdefault("ENCRYPTION_KEY", "lZkbDx2lh9pTfbz4Q4kU8XwGZ7VYsK3xQbZ1Hh1vC2I=")  # valid Fernet key for tests
os.environ.setdefault("PARTNER_API_KEY", "test_partner_key")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_amisafe.db")

from privacy.anonymiser import (
    hash_phone, encrypt, decrypt, anonymise_text,
    extract_platform_hint, get_region_code,
    generate_report_id, generate_session_id,
)


class TestPhoneHashing:
    def test_same_number_produces_same_hash(self):
        h1 = hash_phone("+2348012345678")
        h2 = hash_phone("+2348012345678")
        assert h1 == h2

    def test_different_numbers_produce_different_hashes(self):
        h1 = hash_phone("+2348012345678")
        h2 = hash_phone("+2348012345679")
        assert h1 != h2

    def test_hash_does_not_contain_original_number(self):
        h = hash_phone("+2348012345678")
        assert "2348012345678" not in h

    def test_hash_is_fixed_length(self):
        h1 = hash_phone("+234801234")
        h2 = hash_phone("+254712345678901")
        assert len(h1) == len(h2) == 64  # SHA-256 hex digest length


class TestEncryption:
    def test_encrypt_decrypt_roundtrip(self):
        original = "This is a sensitive report description."
        encrypted = encrypt(original)
        decrypted = decrypt(encrypted)
        assert decrypted == original

    def test_encrypted_text_differs_from_original(self):
        original = "Sensitive content"
        encrypted = encrypt(original)
        assert encrypted != original

    def test_encrypt_handles_unicode(self):
        original = "Ìròyìn nípa ìpalára AI ní èdè Yorùbá"
        encrypted = encrypt(original)
        decrypted = decrypt(encrypted)
        assert decrypted == original


class TestTextAnonymisation:
    def test_strips_email(self):
        text = "Contact me at john@example.com about this."
        result = anonymise_text(text)
        assert "john@example.com" not in result
        assert "[EMAIL REMOVED]" in result

    def test_strips_phone_number(self):
        text = "Call me on +2348012345678 if you need details."
        result = anonymise_text(text)
        assert "+2348012345678" not in result

    def test_strips_url(self):
        text = "I saw it here https://example.com/post/123"
        result = anonymise_text(text)
        assert "https://example.com" not in result
        assert "[URL REMOVED]" in result

    def test_strips_titled_name(self):
        text = "Dr. Adamu posted this fake video."
        result = anonymise_text(text)
        assert "Adamu" not in result

    def test_preserves_general_narrative(self):
        text = "I saw a fake video on Facebook claiming the president said something he never said."
        result = anonymise_text(text)
        assert "fake video" in result
        assert "president" in result

    def test_empty_string_returns_empty(self):
        assert anonymise_text("") == ""

    def test_none_returns_none(self):
        assert anonymise_text(None) is None


class TestPlatformExtraction:
    @pytest.mark.parametrize("text,expected", [
        ("I saw this on Facebook yesterday", "Facebook"),
        ("posted on tiktok this morning", "TikTok"),
        ("it was on twitter.com originally", "Twitter/X"),
        ("found via x.com", "Twitter/X"),
        ("no platform mentioned here", None),
    ])
    def test_extract_platform(self, text, expected):
        assert extract_platform_hint(text) == expected


class TestRegionCode:
    @pytest.mark.parametrize("phone,expected", [
        ("+2348012345678", "NG"),
        ("+254712345678", "KE"),
        ("+27821234567", "ZA"),
        ("+233241234567", "GH"),
        ("+19998887777", "XX"),  # unsupported region
    ])
    def test_region_detection(self, phone, expected):
        assert get_region_code(phone) == expected


class TestIDGeneration:
    def test_report_id_format(self):
        report_id = generate_report_id()
        assert report_id.startswith("AMI-")
        parts = report_id.split("-")
        assert len(parts) == 3
        assert len(parts[1]) == 8   # YYYYMMDD
        assert len(parts[2]) == 8   # hex suffix

    def test_report_ids_are_unique(self):
        ids = {generate_report_id() for _ in range(100)}
        assert len(ids) == 100

    def test_session_ids_are_valid_uuids(self):
        import uuid
        session_id = generate_session_id()
        uuid.UUID(session_id)  # raises if invalid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
