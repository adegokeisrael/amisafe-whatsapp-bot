"""
Conversation state machine for AmiSafe WhatsApp bot.

Drives the reporter through:
  START -> LANGUAGE_SELECTION -> HARM_TYPE_SELECTION -> DESCRIPTION ->
  EVIDENCE_REQUEST -> EVIDENCE_RECEIVED -> DISCLOSURE_LEVEL ->
  CONFIRMATION -> COMPLETE

Each incoming message is routed to a handler based on the session's
current state. Handlers validate input, update the session, and
return the next outbound message.
"""

import logging
from datetime import timedelta
from utils import utcnow

from database.db import get_db
from database.models import Session as DBSession, ConversationState, DisclosureLevel, HarmType, Report
from bot.taxonomy import (
    LANGUAGE_MENU, LANGUAGE_CODES, HARM_TYPE_KEYS,
    get_strings, get_harm_type_label, get_disclosure_label,
)
from bot.whatsapp import send_message
from privacy.anonymiser import (
    hash_phone, generate_session_id, generate_report_id,
    encrypt, decrypt, anonymise_text, extract_platform_hint, get_region_code,
)
from media.processor import process_image, process_audio
from config import settings

logger = logging.getLogger(__name__)

GLOBAL_COMMANDS = {
    "help": "HELP_REQUESTED",
    "tip": "HELP_REQUESTED",
    "taimako": "HELP_REQUESTED",
    "iranlọwọ": "HELP_REQUESTED",
    "enyemaka": "HELP_REQUESTED",
    "msaada": "HELP_REQUESTED",
    "እርዳታ": "HELP_REQUESTED",
    "caawin": "HELP_REQUESTED",
    "usizo": "HELP_REQUESTED",
    "stop": "CANCEL_REQUESTED",
    "cancel": "CANCEL_REQUESTED",
    "tsaya": "CANCEL_REQUESTED",
    "dẹkun": "CANCEL_REQUESTED",
    "kwụsị": "CANCEL_REQUESTED",
    "simama": "CANCEL_REQUESTED",
    "ቆም": "CANCEL_REQUESTED",
    "jooji": "CANCEL_REQUESTED",
    "misa": "CANCEL_REQUESTED",
    "start": "START_REQUESTED",
    "fara": "START_REQUESTED",
    "bẹrẹ": "START_REQUESTED",
    "bido": "START_REQUESTED",
    "anza": "START_REQUESTED",
    "ጀምር": "START_REQUESTED",
    "bilow": "START_REQUESTED",
    "qala": "START_REQUESTED",
}


def _get_or_create_session(db, phone_hash: str) -> DBSession:
    session = db.query(DBSession).filter_by(phone_hash=phone_hash).first()
    now = utcnow()

    if session and session.expires_at and session.expires_at < now:
        db.delete(session)
        db.flush()
        session = None

    if not session:
        session = DBSession(
            id=generate_session_id(),
            phone_hash=phone_hash,
            state=ConversationState.START,
            expires_at=now + timedelta(seconds=settings.session_ttl),
        )
        db.add(session)
        db.flush()

    return session


def _touch_session(session: DBSession):
    session.updated_at = utcnow()
    session.expires_at = session.updated_at + timedelta(seconds=settings.session_ttl)


def _reset_session(db, session: DBSession):
    session.state = ConversationState.START
    session.language = None
    session.harm_type = None
    session.description_encrypted = None
    session.evidence_path = None
    session.evidence_hash = None
    session.evidence_type = None
    session.disclosure_level = None
    session.report_id = None


async def handle_incoming_message(
    phone_number: str,
    message_id: str,
    message_type: str,
    text_body: str | None = None,
    media_id: str | None = None,
    mime_type: str | None = None,
):
    """
    Main entry point. Routes an incoming WhatsApp message through
    the conversation state machine and sends the appropriate reply.
    """
    phone_hash = hash_phone(phone_number)

    with get_db() as db:
        session = _get_or_create_session(db, phone_hash)
        lang = session.language or "en"
        strings = get_strings(lang)

        normalized_text = (text_body or "").strip().lower()

        command = GLOBAL_COMMANDS.get(normalized_text)

        if command == "HELP_REQUESTED":
            await send_message(phone_number, strings["help_message"])
            return

        if command == "CANCEL_REQUESTED":
            _reset_session(db, session)
            await send_message(phone_number, strings["cancel_message"])
            return

        if command == "START_REQUESTED" and session.state != ConversationState.START:
            _reset_session(db, session)
            await send_message(phone_number, LANGUAGE_MENU)
            session.state = ConversationState.LANGUAGE_SELECTION
            _touch_session(session)
            return

        state = session.state

        if state == ConversationState.START:
            await send_message(phone_number, LANGUAGE_MENU)
            session.state = ConversationState.LANGUAGE_SELECTION

        elif state == ConversationState.LANGUAGE_SELECTION:
            await _handle_language_selection(db, session, phone_number, normalized_text)

        elif state == ConversationState.HARM_TYPE_SELECTION:
            await _handle_harm_type_selection(db, session, phone_number, normalized_text, strings)

        elif state == ConversationState.DESCRIPTION:
            await _handle_description(db, session, phone_number, text_body, strings)

        elif state == ConversationState.EVIDENCE_REQUEST:
            await _handle_evidence(
                db, session, phone_number, message_type, text_body,
                media_id, mime_type, strings
            )

        elif state == ConversationState.DISCLOSURE_LEVEL:
            await _handle_disclosure_selection(db, session, phone_number, normalized_text, strings)

        elif state == ConversationState.CONFIRMATION:
            await _handle_confirmation(db, session, phone_number, normalized_text, strings)

        else:
            _reset_session(db, session)
            await send_message(phone_number, LANGUAGE_MENU)
            session.state = ConversationState.LANGUAGE_SELECTION

        _touch_session(session)


async def _handle_language_selection(db, session, phone_number, text):
    code = LANGUAGE_CODES.get(text)
    if not code:
        await send_message(phone_number, LANGUAGE_MENU)
        return

    session.language = code
    strings = get_strings(code)
    await send_message(phone_number, strings["greeting"])
    await send_message(phone_number, strings["choose_harm"])
    session.state = ConversationState.HARM_TYPE_SELECTION


async def _handle_harm_type_selection(db, session, phone_number, text, strings):
    index_map = {str(i + 1): key for i, key in enumerate(HARM_TYPE_KEYS)}
    harm_key = index_map.get(text)

    if not harm_key:
        await send_message(phone_number, strings["invalid_input"])
        await send_message(phone_number, strings["choose_harm"])
        return

    session.harm_type = harm_key
    await send_message(phone_number, strings["describe_prompt"])
    session.state = ConversationState.DESCRIPTION


async def _handle_description(db, session, phone_number, text_body, strings):
    if not text_body or len(text_body.strip()) < 3:
        await send_message(phone_number, strings["invalid_input"])
        await send_message(phone_number, strings["describe_prompt"])
        return

    platform_hint = extract_platform_hint(text_body)
    cleaned = anonymise_text(text_body)

    session.description_encrypted = encrypt(cleaned)
    session.evidence_type = None
    if platform_hint:
        session.evidence_path = f"__platform_hint__:{platform_hint}"

    await send_message(phone_number, strings["evidence_prompt"])
    session.state = ConversationState.EVIDENCE_REQUEST


async def _handle_evidence(
    db, session, phone_number, message_type, text_body, media_id, mime_type, strings
):
    skip_words = {"skip", "tsallake", "fo", "wụfe", "ruka", "ዝለሉ", "ubo", "yeqa"}
    text_lower = (text_body or "").strip().lower()

    platform_hint = None
    if session.evidence_path and session.evidence_path.startswith("__platform_hint__:"):
        platform_hint = session.evidence_path.split(":", 1)[1]
        session.evidence_path = None

    if text_lower in skip_words:
        await send_message(phone_number, strings["skip_evidence_warning"])
        session.evidence_hash = None
        session.evidence_type = "none"
        await send_message(phone_number, strings["disclosure_prompt"])
        session.state = ConversationState.DISCLOSURE_LEVEL
        if platform_hint:
            session.report_id = f"__platform__:{platform_hint}"
        return

    if message_type == "image" and media_id:
        evidence_hash, _ = await process_image(media_id, mime_type or "image/jpeg")
        session.evidence_hash = evidence_hash
        session.evidence_type = "image"
        await send_message(phone_number, strings["evidence_received"] + strings["disclosure_prompt"])
        session.state = ConversationState.DISCLOSURE_LEVEL
        if platform_hint:
            session.report_id = f"__platform__:{platform_hint}"
        return

    if message_type == "audio" and media_id:
        evidence_hash, transcript = await process_audio(media_id, mime_type or "audio/ogg")
        session.evidence_hash = evidence_hash
        session.evidence_type = "audio"
        if transcript:
            cleaned_transcript = anonymise_text(transcript)
            session.evidence_path = f"__transcript__:{encrypt(cleaned_transcript)}"
        await send_message(phone_number, strings["evidence_received"] + strings["disclosure_prompt"])
        session.state = ConversationState.DISCLOSURE_LEVEL
        if platform_hint:
            session.report_id = f"__platform__:{platform_hint}"
        return

    await send_message(phone_number, strings["invalid_input"])
    await send_message(phone_number, strings["evidence_prompt"])


async def _handle_disclosure_selection(db, session, phone_number, text, strings):
    index_map = {
        "1": DisclosureLevel.PRIVATE,
        "2": DisclosureLevel.ANONYMOUS_RESEARCH,
        "3": DisclosureLevel.VERIFIED_PARTNER,
    }
    level = index_map.get(text)

    if not level:
        await send_message(phone_number, strings["invalid_input"])
        await send_message(phone_number, strings["disclosure_prompt"])
        return

    session.disclosure_level = level

    description_preview = "-"
    if session.description_encrypted:
        try:
            full = decrypt(session.description_encrypted)
            description_preview = full[:120] + ("..." if len(full) > 120 else "")
        except Exception:
            description_preview = "[unable to preview]"

    evidence_status = {
        "image": "📸 Image attached",
        "audio": "🎤 Voice note attached",
        "none": "⚠️ No evidence attached",
    }.get(session.evidence_type, "⚠️ No evidence attached")

    harm_label = get_harm_type_label(session.harm_type, session.language)
    disclosure_label = get_disclosure_label(level, session.language)

    confirm_text = strings["confirm_prompt"].format(
        harm_type=harm_label,
        description=description_preview,
        evidence_status=evidence_status,
        disclosure_level=disclosure_label,
    )

    await send_message(phone_number, confirm_text)
    session.state = ConversationState.CONFIRMATION


async def _handle_confirmation(db, session, phone_number, text, strings):
    yes_words = {strings["confirm_yes"].lower(), "yes", "ee", "i", "bẹẹni", "ndio", "አዎ", "hee", "yebo"}
    no_words = {strings["confirm_no"].lower(), "no", "a'a", "rara", "mbā", "hapana", "አይ", "maya", "cha"}

    if text in no_words:
        _reset_session(db, session)
        await send_message(phone_number, strings["cancel_message"])
        return

    if text not in yes_words:
        await send_message(phone_number, strings["invalid_input"])
        return

    platform_hint = None
    if session.report_id and session.report_id.startswith("__platform__:"):
        platform_hint = session.report_id.split(":", 1)[1]

    transcript_encrypted = None
    if session.evidence_path and session.evidence_path.startswith("__transcript__:"):
        transcript_encrypted = session.evidence_path.split(":", 1)[1]

    report_id = generate_report_id()

    if session.disclosure_level == DisclosureLevel.PRIVATE:
        success_msg = strings["private_success_message"].format(report_id=report_id)
    else:
        region_code = get_region_code(phone_number)
        report = Report(
            id=report_id,
            session_id=session.id,
            harm_type=session.harm_type,
            language=session.language,
            description_encrypted=session.description_encrypted,
            evidence_hash=session.evidence_hash,
            evidence_type=session.evidence_type,
            transcript_encrypted=transcript_encrypted,
            disclosure_level=session.disclosure_level,
            platform_hint=platform_hint,
            region_code=region_code,
        )
        db.add(report)
        success_msg = strings["success_message"].format(report_id=report_id)

    await send_message(phone_number, success_msg)
    _reset_session(db, session)
    session.state = ConversationState.COMPLETE
