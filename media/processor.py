"""
Media processor for AmiSafe.

Handles:
  - Downloading images and audio from WhatsApp Cloud API
  - Stripping EXIF from images
  - Transcribing voice notes using faster-whisper (tiny model, CPU)
  - Deleting raw media files after processing
"""

import os
import logging
import httpx
import aiofiles
from config import settings
from privacy.anonymiser import strip_exif, hash_file, secure_delete

logger = logging.getLogger(__name__)

# Lazy-load Whisper to avoid startup delay
_whisper_model = None


def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        logger.info("Loading faster-whisper tiny model...")
        _whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
        logger.info("Whisper model loaded.")
    return _whisper_model


async def _get_media_url(media_id: str) -> str:
    """Resolve a WhatsApp media ID to a download URL."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://graph.facebook.com/{settings.whatsapp_api_version}/{media_id}",
            headers={"Authorization": f"Bearer {settings.whatsapp_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["url"]


async def download_media(media_id: str, mime_type: str) -> tuple[str, str]:
    """
    Download a WhatsApp media file.

    Returns:
        (local_file_path, evidence_type)  where evidence_type is 'image' or 'audio'
    """
    url = await _get_media_url(media_id)

    # Determine extension from mime type
    ext_map = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "audio/ogg": ".ogg",
        "audio/mpeg": ".mp3",
        "audio/mp4": ".m4a",
        "audio/aac": ".aac",
        "audio/wav": ".wav",
    }
    ext = ext_map.get(mime_type, ".bin")
    evidence_type = "image" if mime_type.startswith("image/") else "audio"

    file_path = os.path.join(settings.media_temp_dir, f"{media_id}{ext}")

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "GET",
            url,
            headers={"Authorization": f"Bearer {settings.whatsapp_token}"},
            timeout=30,
        ) as response:
            response.raise_for_status()
            async with aiofiles.open(file_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    await f.write(chunk)

    logger.info(f"Downloaded media {media_id} → {file_path}")
    return file_path, evidence_type


async def process_image(media_id: str, mime_type: str) -> tuple[str, str]:
    """
    Download an image, strip EXIF, compute hash.

    Returns:
        (evidence_hash, cleaned_file_path)
    """
    file_path, _ = await download_media(media_id, mime_type)
    strip_exif(file_path)
    evidence_hash = hash_file(file_path)
    logger.info(f"Image processed, hash: {evidence_hash[:12]}...")
    return evidence_hash, file_path


async def process_audio(media_id: str, mime_type: str) -> tuple[str, str | None]:
    """
    Download an audio file, transcribe it with Whisper, delete raw audio.

    Returns:
        (evidence_hash, transcript_text or None)
    """
    file_path, _ = await download_media(media_id, mime_type)
    evidence_hash = hash_file(file_path)

    transcript = None
    try:
        model = _get_whisper()
        segments, info = model.transcribe(file_path, beam_size=5)
        transcript = " ".join(segment.text for segment in segments).strip()
        logger.info(
            f"Transcribed audio ({info.language}, {info.duration:.1f}s): "
            f"{transcript[:60]}..."
        )
    except Exception as e:
        logger.warning(f"Transcription failed for {file_path}: {e}")
    finally:
        # Audio file is never kept after transcription
        secure_delete(file_path)

    return evidence_hash, transcript
