"""
Integration tests for the AmiSafe conversation state machine.

These tests mock the outbound WhatsApp send call and the database,
exercising the full state machine end-to-end for a happy-path report.

Run with:
    pytest tests/test_conversation.py -v
"""

import os
import sys
import asyncio
import pytest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("WHATSAPP_TOKEN", "test_token")
os.environ.setdefault("WHATSAPP_PHONE_NUMBER_ID", "test_id")
os.environ.setdefault("VERIFY_TOKEN", "test_verify")
os.environ.setdefault("ENCRYPTION_KEY", "lZkbDx2lh9pTfbz4Q4kU8XwGZ7VYsK3xQbZ1Hh1vC2I=")
os.environ.setdefault("PARTNER_API_KEY", "test_partner_key")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_conversation.db")

from database.db import init_db
from database.models import ConversationState, Report
from bot.conversation import handle_incoming_message
from database.db import get_db


@pytest.fixture(autouse=True, scope="module")
def setup_database():
    init_db()
    yield


@pytest.fixture
def mock_send():
    with patch("bot.conversation.send_message", new_callable=AsyncMock) as mock:
        yield mock


@pytest.mark.asyncio
async def test_full_happy_path_text_only_skip_evidence(mock_send):
    """
    Simulates a full report: language -> harm type -> description ->
    skip evidence -> anonymous research disclosure -> confirm.
    """
    phone = "+2348099990000"  # unique per test to avoid session collisions

    # 1. First contact -> language menu
    await handle_incoming_message(phone, "m1", "text", text_body="hi")
    assert mock_send.called

    # 2. Select English
    await handle_incoming_message(phone, "m2", "text", text_body="1")

    # 3. Select harm type: False information
    await handle_incoming_message(phone, "m3", "text", text_body="2")

    # 4. Provide description
    await handle_incoming_message(
        phone, "m4", "text",
        text_body="I saw a fake video on Facebook claiming a politician said something false."
    )

    # 5. Skip evidence
    await handle_incoming_message(phone, "m5", "text", text_body="skip")

    # 6. Choose Anonymous Research disclosure
    await handle_incoming_message(phone, "m6", "text", text_body="2")

    # 7. Confirm
    await handle_incoming_message(phone, "m7", "text", text_body="yes")

    # Verify a report was persisted
    with get_db() as db:
        reports = db.query(Report).filter_by(harm_type="FALSE_INFORMATION").all()
        assert len(reports) >= 1
        latest = reports[-1]
        assert latest.disclosure_level == "ANONYMOUS_RESEARCH"
        assert latest.evidence_type == "none"
        assert latest.platform_hint == "Facebook"


@pytest.mark.asyncio
async def test_private_disclosure_not_persisted(mock_send):
    """PRIVATE disclosure reports must never be written to the Report table."""
    phone = "+2348099990001"

    await handle_incoming_message(phone, "m1", "text", text_body="hi")
    await handle_incoming_message(phone, "m2", "text", text_body="1")   # English
    await handle_incoming_message(phone, "m3", "text", text_body="3")   # Unfair treatment
    await handle_incoming_message(phone, "m4", "text", text_body="An AI hiring tool rejected my application unfairly.")
    await handle_incoming_message(phone, "m5", "text", text_body="skip")
    await handle_incoming_message(phone, "m6", "text", text_body="1")   # Private
    await handle_incoming_message(phone, "m7", "text", text_body="yes")

    with get_db() as db:
        reports = db.query(Report).filter_by(harm_type="UNFAIR_TREATMENT").all()
        # No report should exist for this phone's session since disclosure was PRIVATE
        assert len(reports) == 0


@pytest.mark.asyncio
async def test_cancel_resets_session(mock_send):
    phone = "+2348099990002"

    await handle_incoming_message(phone, "m1", "text", text_body="hi")
    await handle_incoming_message(phone, "m2", "text", text_body="1")
    await handle_incoming_message(phone, "m3", "text", text_body="stop")

    # Next message should restart at language menu, not crash
    await handle_incoming_message(phone, "m4", "text", text_body="hello again")
    assert mock_send.called


@pytest.mark.asyncio
async def test_invalid_harm_type_input_reprompts(mock_send):
    phone = "+2348099990003"

    await handle_incoming_message(phone, "m1", "text", text_body="hi")
    await handle_incoming_message(phone, "m2", "text", text_body="1")  # English
    await handle_incoming_message(phone, "m3", "text", text_body="99")  # invalid harm type

    # Should have sent an invalid_input message plus re-prompt — at least 2 sends this turn
    assert mock_send.call_count >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
