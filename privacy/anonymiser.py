"""
Privacy and anonymisation layer for AmiSafe.

Responsibilities:
  - HMAC-SHA256 hashing of phone numbers (never store plaintext)
  - Fernet symmetric encryption of report content
  - Named-entity anonymisation of submitted text
  - EXIF stripping from images
  - Pseudonymous ID generation
"""

import hashlib
import hmac
import os
import re
import uuid
from cryptography.fernet import Fernet
from config import settings

import logging
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Encryption
# ─────────────────────────────────────────────────────────────────────────────

_fernet = Fernet(settings.encryption_key.encode())


def encrypt(text: str) -> str:
    """Encrypt a string. Returns base64-encoded ciphertext."""
    return _fernet.encrypt(text.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """Decrypt a Fernet ciphertext string."""
    return _fernet.decrypt(ciphertext.encode()).decode()


# ─────────────────────────────────────────────────────────────────────────────
# Phone number hashing
# ─────────────────────────────────────────────────────────────────────────────

def hash_phone(phone_number: str) -> str:
    """
    One-way HMAC-SHA256 hash of a phone number.
    Used as a session key — allows conversation resumption
    without storing the real number.
    """
    return hmac.new(
        settings.encryption_key.encode(),
        phone_number.encode(),
        hashlib.sha256
    ).hexdigest()


def get_region_code(phone_number: str) -> str:
    """
    Derive a broad region code from phone prefix.
    Supports the most common African country codes.
    Not meant to be precise — used for aggregate analytics only.
    """
    prefix_map = {
        "+234": "NG",   # Nigeria
        "+254": "KE",   # Kenya
        "+27":  "ZA",   # South Africa
        "+233": "GH",   # Ghana
        "+251": "ET",   # Ethiopia
        "+252": "SO",   # Somalia
        "+255": "TZ",   # Tanzania
        "+256": "UG",   # Uganda
        "+225": "CI",   # Côte d'Ivoire
        "+221": "SN",   # Senegal
        "+237": "CM",   # Cameroon
        "+249": "SD",   # Sudan
        "+212": "MA",   # Morocco
        "+20":  "EG",   # Egypt
        "+243": "CD",   # DRC
    }
    for prefix, code in prefix_map.items():
        if phone_number.startswith(prefix):
            return code
    return "XX"  # Unknown


# ─────────────────────────────────────────────────────────────────────────────
# Text anonymisation
# ─────────────────────────────────────────────────────────────────────────────

# Regex patterns for common PII in text
_PHONE_PATTERN = re.compile(
    r'(?:\+?[\d\s\-\(\)]{7,15})'
)
_EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
)
_URL_PATTERN = re.compile(
    r'https?://[^\s]+'
)

# Common Nigerian/African name patterns (heuristic — not exhaustive)
_COMMON_TITLES = re.compile(
    r'\b(Mr|Mrs|Miss|Dr|Prof|Chief|Alhaji|Alhaja|Pastor|Bishop|Senator|Hon|Barrister)\b\.?\s+[A-Z][a-z]+',
    re.IGNORECASE
)


def anonymise_text(text: str) -> str:
    """
    Apply heuristic anonymisation to submitted text.
    Strips phone numbers, emails, URLs, and titled names.

    Note: This is heuristic-based, not a full NER model.
    Names without titles may not be caught.
    The limitation is documented in README.
    """
    if not text:
        return text

    # Strip emails
    text = _EMAIL_PATTERN.sub("[EMAIL REMOVED]", text)

    # Strip phone-like patterns (preserve narrative structure)
    text = _PHONE_PATTERN.sub("[PHONE REMOVED]", text)

    # Preserve URLs as platform hints but strip after extraction
    # (caller should extract platform hint before calling this)
    text = _URL_PATTERN.sub("[URL REMOVED]", text)

    # Strip titled names
    text = _COMMON_TITLES.sub("[NAME REMOVED]", text)

    return text.strip()


def extract_platform_hint(text: str) -> str | None:
    """
    Try to extract a platform name from submitted text.
    Used to populate the platform_hint field before anonymisation strips URLs.
    """
    platform_patterns = {
        "Facebook": r'\bfacebook\b|\bfb\.com\b',
        "Twitter/X": r'\btwitter\b|\bx\.com\b|\b@\w+\b',
        "TikTok": r'\btiktok\b',
        "Instagram": r'\binstagram\b|\big\b',
        "YouTube": r'\byoutube\b|\byt\b',
        "WhatsApp": r'\bwhatsapp\b|\bwa\b',
        "LinkedIn": r'\blinkedin\b',
        "Telegram": r'\btelegram\b',
        "Google": r'\bgoogle\b',
    }
    text_lower = text.lower()
    for platform, pattern in platform_patterns.items():
        if re.search(pattern, text_lower):
            return platform
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Pseudonymous IDs
# ─────────────────────────────────────────────────────────────────────────────

def generate_session_id() -> str:
    """Generate a pseudonymous session UUID."""
    return str(uuid.uuid4())


def generate_report_id() -> str:
    """
    Generate a human-readable pseudonymous report ID.
    Format: AMI-YYYYMMDD-XXXXXXXX
    Example: AMI-20260615-3F9A2B1C
    """
    from utils import utcnow
    date_str = utcnow().strftime("%Y%m%d")
    unique_part = uuid.uuid4().hex[:8].upper()
    return f"AMI-{date_str}-{unique_part}"


# ─────────────────────────────────────────────────────────────────────────────
# File privacy
# ─────────────────────────────────────────────────────────────────────────────

def strip_exif(image_path: str) -> str:
    """
    Strip all EXIF metadata from an image file.
    Returns path to the cleaned file (overwrites in-place).
    Supports JPEG and PNG.
    """
    try:
        from PIL import Image
        import piexif

        img = Image.open(image_path)

        # For JPEG: remove EXIF block entirely
        if img.format in ("JPEG", "JPG"):
            try:
                piexif.remove(image_path)
            except Exception:
                # Fallback: re-save without EXIF
                data = img.getdata()
                clean = Image.new(img.mode, img.size)
                clean.putdata(data)
                clean.save(image_path, "JPEG", quality=95)
        else:
            # PNG: re-save without metadata
            data = img.getdata()
            clean = Image.new(img.mode, img.size)
            clean.putdata(data)
            clean.save(image_path)

        logger.info(f"EXIF stripped from {image_path}")
    except Exception as e:
        logger.warning(f"EXIF stripping failed for {image_path}: {e}")

    return image_path


def hash_file(file_path: str) -> str:
    """SHA-256 hash of a file. Used as tamper-evident evidence fingerprint."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def secure_delete(file_path: str):
    """
    Overwrite a file with zeros before deleting.
    Best-effort — not cryptographically guaranteed on all filesystems.
    """
    try:
        size = os.path.getsize(file_path)
        with open(file_path, "wb") as f:
            f.write(b"\x00" * size)
        os.remove(file_path)
        logger.info(f"Secure-deleted {file_path}")
    except Exception as e:
        logger.warning(f"Secure delete failed for {file_path}: {e}")
        try:
            os.remove(file_path)
        except Exception:
            pass
