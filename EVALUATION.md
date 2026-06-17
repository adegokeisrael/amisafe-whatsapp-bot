# Evaluation

This document records how the AmiSafe WhatsApp bot was tested and what the
results were. Numbers below are placeholders marked `[FILL IN]` — replace them
with your actual pilot data before submission. Leaving a metric honestly
unmeasured is preferable to inventing a number.

---

## Test environment

- WhatsApp Cloud API sandbox / production number: `[FILL IN — sandbox or live number used]`
- Test period: `[FILL IN — start date to end date]`
- Number of test participants: `[FILL IN — N]`
- Recruitment method: `[FILL IN — e.g. "recruited via X community group in Kano"]`

---

## Functional correctness

| Test case | Result | Notes |
|---|---|---|
| Full report flow completes (text-only evidence skip) | `[PASS/FAIL]` | |
| Full report flow completes (image evidence) | `[PASS/FAIL]` | |
| Full report flow completes (voice note evidence) | `[PASS/FAIL]` | |
| All 9 languages display correctly in WhatsApp client | `[PASS/FAIL]` | Tested on: `[device/OS list]` |
| Session resumes correctly after app backgrounding | `[PASS/FAIL]` | |
| Session expires correctly after TTL (30 min) | `[PASS/FAIL]` | |
| PRIVATE disclosure reports are not persisted server-side | `[PASS/FAIL]` | Verified by querying DB directly |
| EXIF metadata is stripped from submitted images | `[PASS/FAIL]` | Verified with `exiftool` before/after |
| Phone numbers never appear in plaintext in database | `[PASS/FAIL]` | Verified by DB dump inspection |

Run the automated test suite:
```bash
pytest tests/ -v
```
27/27 unit tests passing as of this writing (privacy/anonymisation module).

---

## Pilot results — reporting funnel

Replace with your actual pilot numbers. Suggested metric format, matching
what judges asked for: **baseline → result**.

| Metric | Target (from proposal) | Actual result | Baseline (if applicable) |
|---|---|---|---|
| Total reports submitted | ≥100 | `[FILL IN]` | — |
| Evidence integrity rate (% with attached evidence) | ≥90% | `[FILL IN]` | 0% (no prior reporting channel existed) |
| Median time to complete report | ≤2 min | `[FILL IN]` | N/A — no prior mobile-first channel |
| 7-day reporter retention (% who'd report again) | ≥40% | `[FILL IN]` | — |
| Languages with ≥1 completed report | ≥4 | `[FILL IN]` | — |
| Reports completed via WhatsApp vs. browser extension | — | `[FILL IN ratio]` | — |

**If any target was missed, say so plainly and explain why.** Example:
> *"We reached 64 reports against a target of 100. The shortfall was primarily
> due to limited recruitment time (9 days vs. planned 21) rather than any
> usability failure — completion rate among those who started a report was
> 81%."*

---

## Voice transcription accuracy (if used in pilot)

| Language | N test clips | Word Error Rate (WER) | Notes |
|---|---|---|---|
| Hausa | `[N]` | `[FILL IN]` | `faster-whisper` tiny model is not fine-tuned for Hausa |
| Yoruba | `[N]` | `[FILL IN]` | Tonal language — known weakness, documented in README |
| Igbo | `[N]` | `[FILL IN]` | |
| English | `[N]` | `[FILL IN]` | Baseline comparison |

---

## Anonymisation effectiveness

| Test | Result |
|---|---|
| % of submitted phone numbers correctly stripped from free text | `[FILL IN]` |
| % of submitted email addresses correctly stripped | `[FILL IN]` |
| % of titled names (Mr/Mrs/Dr/Chief etc.) correctly stripped | `[FILL IN]` |
| % of untitled names NOT caught (known limitation) | `[FILL IN]` — estimate by manual review of N=`[N]` sample reports |

This anonymisation is heuristic-based (regex + title patterns), not a trained
NER model. The honest limitation: names without an honorific title are not
reliably caught. This is flagged in the README roadmap for a trained
African-language NER model.

---

## Known failure modes observed during pilot

List anything that broke, confused users, or produced incorrect output.
Examples of the kind of honesty judges are scoring for:

- `[e.g. "3 users sent a voice note in a noisy market environment and transcription failed silently — no error message shown to user. Fixed by adding a fallback message."]`
- `[e.g. "Numbered menu selection failed when users replied with emoji digit reactions instead of typed numbers."]`

---

## What this evaluation does NOT cover

- Load testing under high concurrent volume (pilot was low-volume by design).
- Adversarial testing for coordinated false-reporting attacks (see
  Responsible Innovation section of the main submission for the proposed
  mitigation — rate limiting by device fingerprint — which was not yet
  implemented at pilot stage).
- Cross-validation of report accuracy against independently verified ground truth.
