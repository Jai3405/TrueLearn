---
title: SPK-4 Results — Safeguarding Detector
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 6 — Quality & Eval
inputs: [05-adr/ADR-011, 07-quality/02-test-and-eval-strategy.md, 09-ops/00-cost-model.md]
---

# `SPK-4` Results — Safeguarding Detector

> **Headline: precise rules cannot classify disclosures, and the first result saying they
> could was a tautology.** The architecture in `ADR-011` and the cost model has to change —
> rules triage, a model classifies.

---

## 1. The result that was worthless

The rules-based classifier scored **76/76** on `spikes/disclosures.json`: 0 misses, 0 false
alarms, 0 misroutes.

**That number measures nothing.** I wrote the rules and the corpus, so the patterns were
fitted to the cases. It is one person marking their own exam — and the eval strategy's own
meta-lesson, *treat a result as a harness artefact until proven otherwise*, applies with
more force to a perfect score than to a bad one.

## 2. The result that mattered

`spikes/disclosures_holdout.json` — 33 cases written deliberately in **different surface
form**: Telugu kinship terms (`chinnanna`, `amma`, `nanna`), code-switching, misspellings,
euphemism, indirect phrasing, and Indian English idiom absent from the suppressor list.

| Corpus | Missed disclosures | Misroutes | False alarms |
|---|---|---|---|
| Fitted (`disclosures.json`, 76 cases) | **0 / 34** | 0 | 0 |
| **Held-out (`disclosures_holdout.json`, 33 cases)** | **18 / 18** | 0 | 0 |

**Every held-out disclosure was missed.** All six abuse cases, all seven self-harm cases,
both threat cases, all three low-concern cases.

Examples the precise rules never saw:

- *"my chinnanna does things to me when nobody is at home"* — kinship term not in the list
- *"amma thrashes me with the belt whenever the marks come"* — verb not in the list
- *"i have been burning my hand with the iron when i get upset"* — method not in the list
- *"i already wrote the letter for my parents, just in case"* — no keyword at all

**Generalisation here is not partial. It is zero.** A regex list encodes the phrasings its
author imagined, and a distressed 16-year-old is not obliged to use them.

---

## 3. What this breaks

`ADR-011` left open: *"detector: rules, model, or both? Probably both, with rules as the
floor."* The cost model then relied on that — a per-turn LLM call costs ~$0.016/session
against a $0.015 budget, so **rules had to carry 100% of turns and a model would be
escalated to "on suspicion."**

**Rules with zero recall never produce suspicion.** There is nothing to escalate. As
written, the architecture would have shipped a safeguarding screen that caught only the
phrasings I happened to imagine — and, because misses are invisible, it would have looked
like it was working.

**This is `ADR-015` in a different costume:** a component whose failure mode is silence.

---

## 4. The fix — invert what the rules are for

Stop asking rules *"is this a disclosure?"* Ask *"is this anything other than a maths turn?"*

**Separating personal content from maths content is far easier and far more robust**, and it
degrades safely: an unfamiliar way of describing harm still escalates, because it still
isn't maths.

```
triage(turn):
    if no first-person content                 -> no escalation   # a bare problem statement
    if any harm / kin / affect / secrecy token -> escalate
    if no strong maths vocabulary              -> escalate
    else                                       -> no escalation
```

Rules **triage**. A model **classifies** what they catch.

| Corpus | Recall on disclosures | Escalation rate on benign |
|---|---|---|
| Fitted (76 cases) | **100%** (34/34) | 52.4% |
| **Held-out (33 cases)** | **100%** (18/18) | 73.3% |

**100% recall on language the net was never tuned against.** That is the property precise
rules could not deliver at any threshold.

---

## 5. The honest caveat, which is large

**At the escalation rates measured, the triage net saves almost nothing.**

| | Cost/session | vs $0.015 budget |
|---|---|---|
| Model on every turn | $0.016 | +107% |
| Triage net at 88% escalation (held-out) | $0.0141 | +94% |
| Triage net at 74% escalation (fitted) | $0.0114 | +76% |

**Both corpora are ~45% disclosures, and their benign halves are adversarial by
construction** — exam-stress idiom and maths-vocabulary collisions, chosen precisely because
they are hard. **Real traffic is nothing like this.** Most turns are *"what's the derivative
of x³"*, which carries no first-person content and never escalates.

**So the measured escalation rate is an upper bound, not an estimate.** The economics depend
on a traffic-mix assumption nobody has measured (`A-035`). If production turns are 90% pure
maths, escalation lands near 10–15% and costs ~$0.002/session. If students chat more than
they compute, the saving disappears and a per-turn model call becomes the honest budget line.

---

## 6. `A-019` is *not* closed

`A-019` — the 1% per-session flag rate that sizes the pager rota under `GD-15` — **remains
open.**

I measured the **escalation rate** (what reaches the model), not the **flag rate** (what
reaches a human). Those are separated by the model classifier, which does not exist yet.
Escalating 70% of turns to a model that flags 2% of them yields a ~1.4% flag rate — but that
2% is a guess, and always was.

**The rota cannot be sized until the classifier is built and measured.** `GD-15` deferring
rota sizing to `SPK-4` was right; `SPK-4` has moved the question rather than answered it.

---

## 7. What to change

| Document | Change |
|---|---|
| `ADR-011` | Open question resolved: **rules triage, model classifies.** "Rules as the floor" is disproven |
| `09-ops/00-cost-model.md` §1 | "Rules-first" survives, but the saving is conditional on `A-035` and may be near zero |
| `06-implementation/00-implementation-plan.md` | Slice 4 gains a model classifier; it is not rules-only |
| `02-test-and-eval-strategy.md` | Add invariant 8: **a perfect score on a corpus you authored is a tautology — always hold out** |

---

## Assumptions

| ID | Assumption | Confidence | How to kill it |
|---|---|---|---|
| `A-035` | Production turns are dominated by pure maths with no first-person content | **Unmeasured** | Instrument escalation rate from day one of the pilot. It decides whether triage saves money at all |
| `A-025` | A synthetic corpus is representative enough to size a rota | **Lower than before** — held-out results show how badly authored intuitions generalise | Re-measure on real traffic in term 1 |
| `A-036` | A model classifier will hold 0 misroutes on escalated turns | Untested — the classifier does not exist | Build it, then extend this harness |

## Open Questions for Founders

| ID | Question | Why |
|----|----------|-----|
| `QQ-01` *(restated, now urgent)* | **Will you write the hard negatives and the kinship/idiom vocabulary?** | The held-out set failed on `chinnanna`, `amma`, `nanna`, `chompestadu`. I do not have this vocabulary, and guessing at it is what produced the 0% result |
| `QQ-03` | Are you comfortable that the safeguarding screen sends most turns to a model? | It changes the data-flow story told to a school: more turns leave the device for inference, not fewer |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | First run. Precise rules: 76/76 fitted, **0/18 held-out**. Inverted triage net: **100% recall on both**. Resolves `ADR-011`'s open question against the assumption it was written on. `A-019` explicitly **not** closed. |

## Related documents

- [`02-test-and-eval-strategy.md`](02-test-and-eval-strategy.md) §4 — the spec this executes
- [`../05-adr/ADR-011-safeguarding-escalation.md`](../05-adr/ADR-011-safeguarding-escalation.md) — the ADR this amends
- [`../09-ops/00-cost-model.md`](../09-ops/00-cost-model.md) §1 — the cost claim this qualifies
