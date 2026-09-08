# Spikes

Two experiments that can invalidate the architecture. Both run on **OpenRouter's free
models** with **no install step** — stdlib Python only, no card, $0. Run them before
the TAR.

```bash
python3 spikes/spk1_leakage.py  --self-check   # validates the harness, no network
python3 spikes/pq1_ocr.py       --self-check   # validates the scorer, no network
python3 spikes/make_worksheet.py --self-check  # validates the test-data generator
```

**Get a key:** [openrouter.ai/keys](https://openrouter.ai/keys). Free tier is roughly
20 requests/minute and 200/day — a full SPK-1 run is ~100 calls, PQ-01 is ~20, so both
fit inside a single day's allowance.

Free models verified 2026-09-08. **Free tiers rotate**, so check
[the free-models collection](https://openrouter.ai/collections/free-models) before
assuming a slug still resolves.

| Slug | Vision | Use for |
|---|---|---|
| `thinkingmachines/inkling:free` | ✅ | both spikes (default) |
| `thinkingmachines/inkling-small:free` | ✅ | PQ-01, cheaper/faster comparison |
| `dots-studio/dots-3-note-preview:free` | ✅ | both |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | ✅ | PQ-01 |
| `nvidia/nemotron-3-super-120b-a12b:free` | ❌ | SPK-1 only |
| `poolside/laguna-s-2.1:free` | ❌ | SPK-1 only |

Gemini is still supported via `--provider gemini` if you prefer it.

---

## PQ-01 — Can a model read student handwriting? *(the bigger risk)*

**The question.** `FR-002` assumes a multimodal model can transcribe a Grade 10–12
student's handwritten maths at **≥92% step-level accuracy** (`NFR-002`). Nobody has
measured this. If real models manage 70% on rushed algebra in a dim room on a cheap
phone camera, the photo-capture wedge does not work and the input model has to change.

**This is the single point of failure for the product as specified.**

### Getting the test data — no collection required

The question is **not** "can it read *student* handwriting". It is "can it read
**multi-step handwritten working containing mistakes**, photographed casually". You can
produce exactly that yourself in about an hour, with no school access, no permissions
and no privacy problem.

```bash
python3 spikes/make_worksheet.py --out ~/handwriting --count 20
```

That writes `worksheet.txt` (20 items to copy by hand) and `truth.json` (**the ground
truth, already filled in**). No transcription work — the answer key is generated
alongside the sheet.

Then:

1. **Handwrite** each item onto paper exactly as printed. Don't print it; don't tidy it.
2. Write naturally and fairly fast. Neat handwriting is not the test.
3. Photograph each as `NN.jpg` — phone camera, held at an angle, dim indoor light for
   at least five of them, ruled paper and pencil for some.
4. Get one or two other people to write some, if you can. Handwriting variation is a
   large part of what is being measured.

**Half the items contain a deliberate, propagating mistake** — a sign slip, a dropped
distribution, an off-by-one in an AP. Copy them wrong, exactly as shown. A model that
silently *corrects* the mistake has failed, because seeing the student's actual error is
the entire product. The scorer counts a corrected step as **wrong**.

> **Why not a public dataset?** CROHME and HME100K are real and available, but they are
> single clean expressions, not multi-step working with errors. They would measure the
> wrong thing and flatter the result.

> **Later, with a school:** real student handwriting is messier and more varied than
> yours, so this gives an optimistic reading. Treat it as a **ceiling**. If the model
> fails here it will certainly fail on real students, which is the cheap half of the
> question and worth knowing first. Real student images are children's personal data —
> keep them outside this repo; the runner refuses in-repo paths.

### Run

```bash
OPENROUTER_API_KEY=... python3 spikes/pq1_ocr.py \
    --images ~/handwriting --truth ~/handwriting/truth.json
```

Compare models by re-running with `--model dots-studio/dots-3-note-preview:free` etc.

**Reading the result.** ≥92% means the wedge holds. 80–92% means it may hold with a
confirmation step ("is this what you wrote?"), which costs a turn but is survivable.
Below 80%, `FR-002` fails and the PRD §2 input model needs rethinking — most likely
toward structured entry, which is a materially worse product.

---

## SPK-1 — Does the tutor hold the line?

**The question.** `NFR-003` requires an answer-leakage rate **below 5%** against
adversarial attacks. `A-008` rated this "low confidence, unproven". The brand promise
is one screenshot away from collapse if it fails.

26 multi-turn attacks across 12 categories in `attacks.json`: direct requests,
authority impersonation, third-party framing, **answer confirmation** ("is it 47?"),
prompt injection, incremental grinding, hypothetical framing, format shifts
(poem/JSON/code), emotional pressure, partial extraction, verification traps and role
reversal.

```bash
OPENROUTER_API_KEY=... python3 spikes/spk1_leakage.py
OPENROUTER_API_KEY=... python3 spikes/spk1_leakage.py --model nvidia/nemotron-3-super-120b-a12b:free
```

Run it against **two or three models**. A leakage rate that varies wildly by model tells
you the guarantee cannot rest on prompting alone — which is the `FR-010` decision.

**The point is comparison, not a single number.** Iterate on the prompt and re-run:

```bash
python3 spikes/spk1_leakage.py --prompt-file my_variant.txt
```

Failing transcripts land in `spikes/out/`. **Read them before changing anything** —
some will be detector false positives, and the detector deliberately favours recall
over precision (a missed leak is a wrong answer about whether the product works; a
false positive costs a glance).

**Reading the result.** Below 5% and the promise is defensible. Above ~20% and prompting
alone will not carry it — `FR-010` needs the independent enforcement layer, which is a
real subsystem, not a prompt tweak.

---

## Cost

Both fit inside free tiers. SPK-1 makes ~70 short calls; PQ-01 makes 20 image calls.
Use `--delay` if you hit rate limits. Total spend: **$0**, per `GD-09`.

## Notes

- `spikes/out/` and any image directories are git-ignored.
- The attack corpus is not throwaway — it becomes the CI regression suite in `FR-021`,
  which is what catches "the model started giving answers again" after a model upgrade.
- Both scorers have `--self-check`. The leakage detector's self-check has already
  caught one real bug and three broken attacks; keep it passing.
