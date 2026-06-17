# AmiSafe WhatsApp Bot

**Community-led AI harm reporting via WhatsApp — built for African internet users.**

AmiSafe's WhatsApp companion bot replicates the browser extension's structured harm-capture flow for users with mobile-only internet access. A reporter submits a structured, evidence-backed, anonymised AI harm report entirely within WhatsApp — no app download, no account, no personal identifier required.

---

## What it does

1. Greets the user in their chosen language (8 African languages supported)
2. Walks them through a plain-language harm taxonomy
3. Collects mandatory evidence (image, screenshot, or voice note)
4. Lets them choose their disclosure level (private / anonymous research / verified partner)
5. Stores the report with a pseudonymous ID, encrypted at rest
6. Returns a receipt with a report reference number

**Supported languages at launch:**
Hausa · Yoruba · Igbo · Swahili · Amharic · Somali · Zulu · Nigerian Pidgin · English

**Harm taxonomy:**
Fake Image or Video · False Information · Unfair Treatment · Harassment or Intimidation · Financial Harm · Other

---

## Architecture

```
WhatsApp Cloud API
       │
       ▼
  FastAPI Webhook  ←──  Signature Verification
       │
       ▼
  Conversation State Machine (SQLite sessions)
       │
  ┌────┴─────────────────────┐
  │                          │
  ▼                          ▼
Media Processor         Anonymiser
(image/audio download)  (NER stripping, pseudonymous IDs)
  │                          │
  └────────────┬─────────────┘
               │
               ▼
    Encrypted Report Store (SQLite → swap PostgreSQL for prod)
               │
               ▼
    Aggregation Dashboard (JSON export for vetted partners)
```

---

## Setup

### Prerequisites
- Python 3.10+
- A Meta Business Account with WhatsApp Cloud API access
- A publicly accessible HTTPS endpoint (use [ngrok](https://ngrok.com/) for local dev)

### 1. Clone and install

```bash
git clone https://github.com/adegokeisrael/amisafe-whatsapp-bot.git
cd amisafe-whatsapp-bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
WHATSAPP_TOKEN=your_whatsapp_cloud_api_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=any_random_string_you_choose
ENCRYPTION_KEY=generate_with_python_-c_"from_cryptography.fernet_import_Fernet;print(Fernet.generate_key().decode())"
DATABASE_URL=sqlite:///./amisafe.db
PARTNER_API_KEY=key_for_vetted_partner_dashboard_access
```

### 3. Run locally

```bash
uvicorn main:app --reload --port 8000
```

### 4. Expose locally with ngrok (development)

```bash
ngrok http 8000
```

Copy the HTTPS URL ngrok gives you. In your Meta App Dashboard:
- Go to WhatsApp → Configuration → Webhook
- Set Callback URL to: `https://your-ngrok-url.ngrok.io/webhook`
- Set Verify Token to the value you put in `.env`
- Subscribe to: `messages`

### 5. Deploy to production

```bash
docker build -t amisafe-bot .
docker run -d -p 8000:8000 --env-file .env amisafe-bot
```

Point your domain's HTTPS to port 8000. Update the webhook URL in Meta App Dashboard.

---

## Privacy architecture

| What | How |
|---|---|
| No account required | Sessions keyed to rotating pseudonymous ID, not phone number |
| Phone number handling | Hashed with HMAC-SHA256, never stored in plaintext |
| Evidence files | Downloaded to temp storage, EXIF stripped, then encrypted before DB write |
| Text content | Named-entity recognition strips names, locations, phone numbers before storage |
| Audio | Transcribed on-server using `faster-whisper` (tiny model), audio deleted after transcription |
| Disclosure levels | Reporter explicitly chooses: Private / Anonymous Research / Verified Partner |
| Public output | Aggregate patterns only — individual reports never exposed |

---

## Report disclosure levels

| Level | What is stored | Who can access |
|---|---|---|
| **Private** | Encrypted locally, never transmitted | Reporter only (via reference ID) |
| **Anonymous Research** | Pseudonymous report + evidence hash | Vetted researchers via dashboard API |
| **Verified Partner** | Full anonymised report | Named civil society partners (Paradigm Initiative, KICTANET, etc.) |

---

## API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/webhook` | GET | WhatsApp webhook verification |
| `/webhook` | POST | Receive incoming messages |
| `/dashboard/reports` | GET | Aggregate stats (API key required) |
| `/dashboard/export` | GET | Partner data export (API key required) |
| `/health` | GET | Health check |

---

## Limitations

- Voice transcription uses `faster-whisper` tiny model: accuracy is lower for tonal languages (Yoruba, Igbo). A fine-tuned model is a roadmap item.
- WhatsApp Cloud API is rate-limited on the free tier: suitable for pilot volumes, not high-throughput deployment.
- NER anonymisation is English-biased: Hausa/Yoruba/Igbo named-entity stripping uses heuristics rather than a trained NER model. Some names may not be caught.
- The bot cannot verify that submitted images depict AI-generated content — that determination is left to the aggregation/review layer.
- Tested with: Nigerian (+234) and Kenyan (+254) numbers. Other country codes should work but have not been piloted.

---

## Roadmap

- [ ] Fine-tuned Whisper model for Hausa, Yoruba, Igbo transcription
- [ ] African-language NER model for more reliable anonymisation
- [ ] NLLB-200 translation layer so reports submitted in any language surface in cross-language pattern clustering
- [ ] WhatsApp template messages for follow-up notifications (requires Meta template approval)
- [ ] PostgreSQL migration guide for production deployments

---

## Licence

Apache 2.0 — see [LICENSE](LICENSE)

## Contributing

Pull requests welcome. Please open an issue first to discuss what you'd like to change. All contributors must agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
