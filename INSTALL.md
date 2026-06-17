# Install Guide

Step-by-step setup for a judge or practitioner with no prior context.

## 1. Get WhatsApp Cloud API access

1. Go to [developers.facebook.com](https://developers.facebook.com) and create a Meta App.
2. Add the **WhatsApp** product to your app.
3. From the WhatsApp → API Setup page, copy:
   - Temporary access token (or generate a permanent one via System User)
   - Phone Number ID
4. Note: Meta gives you a free test number for development — no business
   verification needed to start testing.

## 2. Clone and configure

```bash
git clone https://github.com/adegokeisrael/amisafe-whatsapp-bot.git
cd amisafe-whatsapp-bot
cp .env.example .env
```

Generate an encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
Paste the output into `.env` as `ENCRYPTION_KEY`.

Pick any random string for `VERIFY_TOKEN` and `PARTNER_API_KEY` — these are
shared secrets you choose yourself, not provided by Meta.

## 3. Install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run the bot locally

```bash
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/health` — you should see `{"status": "ok"}`.

## 5. Expose your local server to the internet

WhatsApp needs an HTTPS URL it can reach. For testing, use ngrok:

```bash
ngrok http 8000
```

Copy the `https://xxxx.ngrok.io` URL it gives you.

## 6. Connect the webhook

In your Meta App Dashboard:
1. Go to WhatsApp → Configuration
2. Callback URL: `https://xxxx.ngrok.io/webhook`
3. Verify Token: the same string you put in `.env` as `VERIFY_TOKEN`
4. Click "Verify and Save"
5. Under "Webhook fields", subscribe to `messages`

## 7. Test it

From the WhatsApp test number Meta gave you, send any message to your
Business test number. You should receive the AmiSafe language menu.

## 8. Run automated tests

```bash
pytest tests/ -v
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Webhook verification fails | `VERIFY_TOKEN` in `.env` doesn't match what you typed in Meta dashboard |
| No reply received | ngrok tunnel expired (free tier times out) — restart ngrok and update webhook URL |
| 401 on `/dashboard/*` | Missing or wrong `X-API-Key` header — must match `PARTNER_API_KEY` in `.env` |
| Audio transcription errors | `ffmpeg` not installed — required by `faster-whisper`. Install via `apt install ffmpeg` or use the provided Dockerfile |
