# Spikes

Two experiments that can invalidate the architecture. Both run on a **free API tier**
with **no install step** — stdlib Python only. Run them before the TAR.

```bash
python3 spikes/spk1_leakage.py --self-check    # validates the harness, no network
python3 spikes/pq1_ocr.py --self-check         # validates the scorer, no network
```

---

## PQ-01 — Can a model read student handwriting? *(the bigger risk)*

**The question.** `FR-002` assumes a multimodal model can transcribe a Grade 10–12
student's handwritten maths at **≥92% step-level accuracy** (`NFR-002`). Nobody has
measured this. If real models manage 70% on rushed algebra in a dim room on a cheap
phone camera, the photo-capture wedge does not work and the input model has to change.

**This is the single point of failure for the product as specified.**

### Collecting the sample — the actual blocker

You need **20 photographs of real student working**. Not printed maths, not your own
neat handwriting — the real thing, because that is what the product will see.

1. Ask a school contact for 20 pages of Grade 10–12 maths homework or classwork.
2. Photograph them **the way a student would**: phone camera, held at an angle, indoor
   evening light, no tripod. Include at least a few that are genuinely messy,
   half-erased, or written in pencil on ruled paper.
3. Vary it deliberately — different students, different handwriting, both algebra and
   geometry, at least three photographed in poor light.
4. **Include pages with mistakes in them.** A model that silently "corrects" a
   student's error is worse than useless: the whole product depends on seeing the
   error the student actually made. The scorer counts a corrected step as *wrong*.

**Privacy.** These images are personal data belonging to children. Store them
**outside this repository**, get the school's permission first, remove any name
written on the page, and delete them once the measurement is done. The runner refuses
in-repo paths for this reason.

### Ground truth

Transcribe each image by hand into `truth.json`, next to the images:

```json
{
  "g10_01.jpg": ["3x + 7 = 22", "3x = 15", "x = 5"],
  "g10_02.jpg": ["(x+2)(x+3)", "x^2 + 5x + 6"]
}
```

Transcribe **what is written, including errors**. This is an hour of tedious work and
it is the whole experiment — the measurement is only as good as the ground truth.

### Run

```bash
GEMINI_API_KEY=... python3 spikes/pq1_ocr.py \
    --images ~/handwriting --truth ~/handwriting/truth.json
```

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
GEMINI_API_KEY=... python3 spikes/spk1_leakage.py
OPENROUTER_API_KEY=... python3 spikes/spk1_leakage.py --provider openrouter \
    --model meta-llama/llama-3.3-70b-instruct:free
```

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
