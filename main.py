"""
AmiSafe WhatsApp Bot — FastAPI application entry point.

Exposes:
  GET  /webhook            — WhatsApp webhook verification challenge
  POST /webhook             — receives incoming WhatsApp messages
  GET  /health               — health check
  GET  /dashboard/reports     — aggregate stats (partner API key required)
  GET  /dashboard/export      — anonymised report export (partner API key required)
"""

import logging
from fastapi import FastAPI, Request, Response, Query, HTTPException, Header
from fastapi.responses import JSONResponse

from config import settings
from database.db import init_db
from bot.conversation import handle_incoming_message
from aggregation.dashboard import get_aggregate_stats, export_reports

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("amisafe")

app = FastAPI(title="AmiSafe WhatsApp Bot", version="1.0.0")


@app.on_event("startup")
async def on_startup():
    init_db()
    logger.info("AmiSafe bot started. Database initialised.")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "amisafe-whatsapp-bot"}


@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta calls this once when you configure the webhook URL."""
    if hub_mode == "subscribe" and hub_verify_token == settings.verify_token:
        logger.info("Webhook verified successfully.")
        return Response(content=hub_challenge, media_type="text/plain")
    logger.warning("Webhook verification failed.")
    raise HTTPException(status_code=403, detail="Verification failed")


@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receives all incoming WhatsApp events.
    We only act on actual user messages; delivery/read receipts are ignored.
    """
    body = await request.json()

    try:
        entry = body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages")

        if not messages:
            # Status update (delivered/read) — nothing to do
            return JSONResponse(content={"status": "ignored"}, status_code=200)

        message = messages[0]
        phone_number = "+" + message["from"] if not message["from"].startswith("+") else message["from"]
        message_id = message["id"]
        message_type = message["type"]

        text_body = None
        media_id = None
        mime_type = None

        if message_type == "text":
            text_body = message["text"]["body"]
        elif message_type == "interactive":
            # Button/list replies — extract the underlying id/title as text
            interactive = message.get("interactive", {})
            if interactive.get("type") == "button_reply":
                text_body = interactive["button_reply"]["title"]
            elif interactive.get("type") == "list_reply":
                text_body = interactive["list_reply"]["title"]
        elif message_type == "image":
            media_id = message["image"]["id"]
            mime_type = message["image"].get("mime_type", "image/jpeg")
        elif message_type == "audio":
            media_id = message["audio"]["id"]
            mime_type = message["audio"].get("mime_type", "audio/ogg")
        else:
            # Unsupported type (video, document, location, etc.)
            text_body = ""

        await handle_incoming_message(
            phone_number=phone_number,
            message_id=message_id,
            message_type=message_type,
            text_body=text_body,
            media_id=media_id,
            mime_type=mime_type,
        )

    except (KeyError, IndexError) as e:
        logger.warning(f"Malformed webhook payload, ignoring: {e}")
    except Exception as e:
        logger.exception(f"Error processing webhook: {e}")
        # Still return 200 — WhatsApp will retry on non-200, we don't want retries
        # for application-level errors that won't resolve on retry.

    return JSONResponse(content={"status": "received"}, status_code=200)


# ─────────────────────────────────────────────────────────────────────────────
# Partner dashboard endpoints
# ─────────────────────────────────────────────────────────────────────────────

def _check_partner_key(x_api_key: str | None):
    if x_api_key != settings.partner_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.get("/dashboard/reports")
async def dashboard_reports(x_api_key: str = Header(None)):
    """Aggregate statistics only — never individual report content."""
    _check_partner_key(x_api_key)
    return get_aggregate_stats()


@app.get("/dashboard/export")
async def dashboard_export(
    x_api_key: str = Header(None),
    disclosure_level: str = Query("VERIFIED_PARTNER"),
):
    """
    Anonymised report export for vetted partners.
    Only returns reports at ANONYMOUS_RESEARCH or VERIFIED_PARTNER disclosure level —
    PRIVATE reports are never persisted server-side and cannot be exported.
    """
    _check_partner_key(x_api_key)
    return export_reports(disclosure_level)
