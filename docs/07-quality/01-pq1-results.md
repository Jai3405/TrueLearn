---
title: PQ-01 Results — Handwriting Transcription Accuracy
status: measured
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-09
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 6 — pulled forward
---

# PQ-01 Results — Handwriting Transcription Accuracy

> **`FR-002` was the single point of failure for the photo-capture wedge.** If a model
> cannot read a student's handwritten working off a phone photo, the PRD §2 input model
> collapses and the wedge with it. It has now been measured on **real human handwriting**.

**Verdict: reachable, not doomed.** 87.5% on the cheapest model tier, against a 92%
target, with no prompt tuning, no image preprocessing and no confirmation step.

---

## 1. Headline

| Model | Accuracy | Images scored | Trustworthy? |
|---|---|---|---|
| **`gemini-flash-lite-latest`** | **87.5%** (42/48 steps) | **12/12** | ✅ **Yes** |
| `gemini-3.5-flash` | — | 0/12 | ❌ All 12 rate-limited (429) after 5 retries |
| `gemini-3.8-flash` | *(100%)* | **1/12** | ❌ **NO VERDICT** — one image is not a measurement |
| Free-tier models (OpenRouter) | ~25% | partial | ❌ Not models anyone would ship |

**`NFR-002` target: ≥92%. Result: FAIL at 87.5% — but narrowly, and on the cheapest tier.**

> The 100% for `gemini-3.8-flash` is shown in parentheses deliberately. It covered **one
> image out of twelve**; the other eleven returned 503. The completeness guard refused to
> print a verdict. Reported as a headline it would have been the most damaging number in
> this document.

---

## 2. How the test set was built

The founders cannot spend an hour hand-copying worksheets, so `make_worksheet.py` was a
dead end. `pq1_build_dataset.py` replaces it with **real human handwriting and zero
effort**:

1. Pull expressions from Google's **MathWriting** dataset — 230k human-written samples
   with LaTeX ground truth, public, no auth.
2. Filter to school-level algebra (`--strict`).
3. **Stack four into one image**, so the page reads as multi-step working.
4. Degrade it into a plausible phone photo: rotation, ruled paper, uneven lighting, blur,
   JPEG quality 55–80.

Twelve pages, 48 steps, exact ground truth, regenerable in minutes.

### What this measures, and what it does not

**Does measure:** can a model transcribe multi-line handwritten maths from a degraded
photo. That is the capability that would kill the wedge outright.

**Does not measure:** whether the model silently *corrects* a student's mistake. The
stacked lines are unrelated expressions, not a derivation containing an error. That
remains the other half of `FR-002` and still needs `make_worksheet.py` or real student
work. **A model that reads perfectly but auto-corrects errors is still useless to us**,
because seeing the actual mistake is the product.

---

## 3. Content difficulty is worth 17 points

The first run scored **68.3%** — on MathWriting's default academic content:
`4^{4^{+^{+^{n}}}}`, `[x,x+O(x^{21/40})]`, `\sqrt[55]{2}`, `(h_o)_k=h_{2k+1}`.

Almost none of that is Grade 10–12 maths, and the errors clustered exactly where school
algebra does not live: exotic single letters (`n`/`m`/`h`), three-digit numbers, nested
towers. Adding `--strict` — school variables only, no 3-digit numbers, no nested
sub/superscripts, no big-O or nth roots — lifted the same model to **85.4%**, and
normalisation fixes took it to **87.5%**.

**Lesson for any future eval: a test set that is not representative produces a number
that is not informative.** The first result understated the model by 19 points.

---

## 4. The six remaining misreads are honest

| Ground truth | Model read | Nature |
|---|---|---|
| `n\le\frac{N-1}{2}` | `m \le \frac{N-1}{2}` | `n`↔`m` — ambiguous to a human too |
| `\sqrt{\frac{16}{35}}` | `\sqrt{\frac{76}{35}}` | `1`↔`7` |
| `1/\sqrt{8\pi}` | `1/\sqrt{\pi}` | dropped a character |
| `\sqrt{2/(N-1)}` | `\sqrt{2/N-1)}` | lost a parenthesis |
| `{2^{7}}^{9}/1+23` | `2^7/1 + 2^3` | nested exponent structure |
| `0^{-}` | `\sigma^-` | genuinely odd source glyph |

No hallucinated content, no invented steps, no silent corrections in this sample. The
failures are character-level ambiguity, which is the *tractable* kind.

---

## 5. What this means for the product

**87.5% lands in the band the PRD already anticipated.** PRD §2 and `spikes/README.md`
both state: ≥92% and the wedge holds as designed; **80–92% and it holds with a
confirmation step**; below 80% and the input model must change.

So the design consequence is a **new v0 requirement**:

> **FR-026 — Transcription confirmation.** After reading the student's working, the tutor
> shows what it read and asks the student to confirm before reasoning about it. Costs one
> round-trip. Turns a silent misread into a visible, correctable one.

This is not a workaround. A tutor that says *"I've read your second line as 3x = 15 — is
that right?"* is behaving like a careful human tutor, and it converts the residual 12.5%
from a correctness risk into a UX cost.

### Model selection

| Finding | Consequence |
|---|---|
| The cheapest tier (`flash-lite`) is the only one that could be measured reliably | Good news for the cost model — it is also the cheapest option in `09-ops/00-cost-model.md` |
| Newer tiers (3.5, 3.8) are heavily rate-limited on free tiers | Cannot be evaluated without paid access. **Do not assume newer = better without measuring** |
| ⚠️ **`gemini-2.5-flash` and `-lite` are "no longer available to new users"** | The cost model quotes 2.5 Flash-Lite at $0.10/$0.40. A new account cannot use it. **`09-ops/00-cost-model.md` needs re-pricing against `gemini-flash-lite-latest`** |

---

## 6. Five measurement failures, and what they cost

Every number in this spike was wrong the first time, always in the direction of a
confident false conclusion. Recorded because the pattern matters more than any single
result.

| Observed | Looked like | Actually was |
|---|---|---|
| `0/4, +0 spurious` on every image | "models can't read handwriting; the wedge is dead" | `dots-3-note-preview` returning **empty content** — all budget spent on internal reasoning |
| `gemini-3.5-flash` 58.3% vs flash-lite 85.4% | "the newer model reads worse" | **Truncated** mid-expression at `maxOutputTokens: 800`; `finishReason` was never checked |
| `gemini-3.8-flash` **100%** | "3.8 is perfect, ship it" | **1 image of 12**; the other 11 returned 503 |
| `gemini-3.5-flash` 78.1% | "middling model" | 8 of 12 images; the rest rate-limited |
| First run 68.3% | "`FR-002` fails" | Academic content, not school maths — worth 17 points |

**Three of those five would have gone into an ADR as fact.** The countermeasures now in
both harnesses: empty-content and truncation raise rather than score; transient HTTP
errors retry with backoff; and **no verdict is printed below 90% completion**.

The `NO VERDICT` guard was ported into `pq1_ocr.py` roughly an hour before
`gemini-3.8-flash` returned its 100%. It caught it.

---

## 7. Next

| # | Action |
|---|---|
| 1 | Add `FR-026` (transcription confirmation) to the PRD as a v0 requirement |
| 2 | Re-price `09-ops/00-cost-model.md` — `gemini-2.5-flash-lite` is unavailable to new accounts |
| 3 | Measure the **silent-correction** half of `FR-002`: does the model fix a student's error? Needs `make_worksheet.py` content |
| 4 | Re-measure the newer tiers with paid access before choosing a production model |
| 5 | Test whether image preprocessing (deskew, contrast) closes the 4.5-point gap more cheaply than a confirmation turn |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-09 | CTO (incoming) | First measurement. 87.5% on real handwriting, school content, cheapest tier. `FR-002` reachable; proposes `FR-026`. |

## Related documents

- [`00-spk1-results.md`](00-spk1-results.md) — the leakage measurement
- [`../02-prd/00-prd.md`](../02-prd/00-prd.md) — `FR-002`, `NFR-002`, `PQ-01`
- [`../09-ops/00-cost-model.md`](../09-ops/00-cost-model.md) — needs re-pricing, see §5
