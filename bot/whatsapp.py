"""
WhatsApp Cloud API client for AmiSafe.
Handles sending text messages and reaction confirmations.
"""

import httpx
import logging
from config import settings

logger = logging.getLogger(__name__)


async def send_message(to: str, text: str):
    """Send a plain text WhatsApp message."""
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    await _post(payload)


async def send_reaction(to: str, message_id: str, emoji: str):
    """React to a specific incoming message."""
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "reaction",
        "reaction": {"message_id": message_id, "emoji": emoji},
    }
    await _post(payload)


async def mark_read(message_id: str):
    """Mark an incoming message as read."""
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    await _post(payload)


async def _post(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                settings.whatsapp_api_url,
                headers={
                    "Authorization": f"Bearer {settings.whatsapp_token}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=10,
            )
            if resp.status_code != 200:
                logger.error(
                    f"WhatsApp API error {resp.status_code}: {resp.text}"
                )
            else:
                logger.debug(f"WhatsApp message sent: {resp.json()}")
        except httpx.RequestError as e:
            logger.error(f"WhatsApp API request failed: {e}")
