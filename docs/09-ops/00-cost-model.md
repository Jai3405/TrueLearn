---
title: Unit Economics and Pricing Model
status: draft — DECISION REQUIRED (GD-12)
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-08
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 8 — pulled forward, because GD-12 blocks pricing
---

# Unit Economics and Pricing Model

> You asked me to model the price rather than pick one. Here is the model, the
> arithmetic behind it, and a recommendation.
>
> **Headline: variable cost is not the constraint, and the deck spent its entire
> economics slide on the wrong number.** At the decided architecture, gross margin never
> goes negative at any plausible usage level. What actually constrains this business is
> **how many schools two founders can sign**, and that is a pricing decision.

**FX assumption:** ₹88 = US$1. Not independently verified — treat INR figures as ±10%.

---

## 1. Variable cost, bottom-up

Per tutoring session, on the architecture decided in `GD-01`/`GD-02` and PRD §6.1
(photo capture, push-to-talk, device-native speech, multimodal LLM doing OCR).

Assume a representative session: 2 photographs, 8 dialogue turns, ~500 output tokens.

| Component | Basis | Cost/session |
|---|---|---|
| LLM input (images + growing dialogue context) | ~25k tokens @ $0.10/1M | $0.0025 |
| LLM output | ~500 tokens @ $0.40/1M | $0.0002 |
| ASR | Device-native (Web Speech API) | **$0.0000** |
| TTS | Device-native | **$0.0000** |
| OCR | Rides the multimodal LLM, not a metered service | $0.0000 |
| Image storage + egress | ~400 KB, 30-day retention | ~$0.0001 |
| Serverless compute | Per invocation | ~$0.0002 |
| **Subtotal** | | **~$0.003** |
| **Budgeted with headroom** | retries, failed OCR, long sessions | **$0.005** |

**All subsequent figures use $0.005/session**, which is roughly 65% padding on the
modelled cost. If reality comes in at $0.003 the conclusions get stronger, not weaker.

### What the rejected architecture would have cost

| Architecture | Cost/session | vs $0.005 |
|---|---|---|
| **Decided** (photo, push-to-talk, native speech) | $0.005 | 1× |
| With vendor TTS (Deepgram Aura-1) | $0.035 | 7× |
| With full-duplex speech-to-speech | $0.051 | 10× |
| **With a photoreal avatar** (20 min @ $0.30/min) | **$6.005** | **1,200×** |

The avatar line is the whole story. At ₹300/student/year, **a single avatar session
costs nearly twice a student's entire annual subscription.** `GD-01` was not a
preference — it was the difference between a business and an arithmetic error.

---

## 2. The counterintuitive finding

Cost is driven by **active** students; revenue is driven by **enrolled** seats. So:

> Cost per enrolled student/year = WAU% × sessions/week × 30 weeks × $0.005

| Weekly active | 2 sessions/wk | 4 sessions/wk |
|---|---|---|
| 5% | $0.015 | $0.030 |
| 20% | $0.060 | $0.120 |
| 50% | $0.150 | $0.300 |
| 100% | $0.300 | $0.600 |

Gross margin at three candidate prices:

| Price/student/yr | 5% WAU | 20% WAU | 50% WAU | 100% WAU, 4/wk |
|---|---|---|---|---|
| ₹150 ($1.70) | 99.1% | 96.5% | 91.2% | **64.7%** |
| ₹300 ($3.41) | 99.6% | 98.2% | 95.6% | **82.4%** |
| ₹600 ($6.82) | 99.8% | 99.1% | 97.8% | **91.2%** |

**Gross margin never goes negative.** To lose money on inference at ₹150/student you
would need ~340 sessions per enrolled student per year — eleven a week, every week,
from every single student. It cannot happen.

Two consequences worth stating plainly:

1. **The deck's "98% cost advantage" was answering a question that does not matter.**
   Token pricing was never going to sink this product at this architecture. The avatar
   would have, and the cost slide never mentioned it.
2. **Low engagement is good for margin and fatal for renewal.** A school paying for 400
   seats where 15% of students engage produces excellent gross margin and does not renew.
   Optimising for margin here is optimising for failure — which is why `SM-L1` (>35% WAU)
   is a *product* target, not a finance one.

---

## 3. What actually constrains the business: fixed cost

Since variable cost is negligible, break-even is entirely about covering fixed cost.

**Year-one fixed cost, realistic and deliberately modest:**

| Item | Basis | Annual |
|---|---|---|
| Curriculum / axiom graph authoring | Maths SME, part-time 6 months @ ₹40k/mo | ~$2,700 |
| Founder subsistence (two, Hyderabad) | ₹60k/mo each | ~$16,400 |
| Entity formation + annual compliance | `FD-06` | ~$700 |
| Baseline hosting, domain, tooling | | ~$400 |
| **Total** | | **~$20,200** |

**Seats needed to break even:**

| Price/student/yr | Seats to cover $20.2k | Schools needed* |
|---|---|---|
| ₹150 ($1.70) | 11,880 | **48** |
| ₹300 ($3.41) | 5,920 | **24** |
| ₹600 ($6.82) | 2,960 | **12** |
| ₹750 ($8.52) | 2,370 | **9** |
| ₹1,000 ($11.36) | 1,780 | **7** |

\* Assuming ~250 students across Grades 10–12 in a mid-size private school. Note this
is *not* total school enrolment — a 1,200-student school has roughly 250 in the target
grades, which is the number that matters and is easy to get wrong.

**This table is the actual pricing decision.** 48 schools is not a thing two founders
sign in year one. 7–12 is, given existing family relationships. The price has to be set
by the sales motion you can actually execute, not by what feels affordable.

---

## 4. Is a higher price defensible?

| Benchmark | Per student/yr | Note |
|---|---|---|
| Mid-market Indian school ERP | ~₹66 ($0.75) | ₹9–20k/yr for a whole 304-student school |
| Enterprise tier (TCS iON class) | ₹1,440–3,000 | **Includes full ERP + devices** |
| Proposed deck price | ₹2,640–4,400 | 11–18% of annual tuition — not viable |
| **Photomath Plus, paid by parents** | **₹6,160** | $69.99/yr |
| **Gauth Plus, paid by parents** | **₹8,800** | $99.99/yr |
| Urban private school tuition | ₹31,782 | The ceiling everything sits inside |

Two things jump out.

**₹600–750 sits in a genuine gap.** It is well above the ERP commodity rate, well below
the enterprise bundle, and it buys a focused product for the two grades where the school's
reputation is actually made. At ₹750 it is **2.4% of annual tuition**.

**Parents already pay 8–12× more than this for strictly worse tools.** A parent spending
₹6,160/year on Photomath is buying an answer machine. That is not an argument for B2C —
`O-05` closed that, and DPDP makes it worse — but it is an argument that the willingness
to pay exists and is currently pointed at the wrong product.

### The structure that threads the needle

**School-collected parent contribution.** The school adds ₹750/student to its fee
schedule and contracts with us as the customer. The school remains the Data Fiduciary,
so the Fourth Schedule educational-institution exemption still applies (`GD-07`), and we
remain its processor — while the money comes from the parent budget that is demonstrably
already there.

This is a commercial structure, not a legal opinion. It needs review before it is
offered to a school, and it should not appear in any pitch until it has been.

---

## 5. Recommendation

> **₹750 per student per year (~$8.52), Grades 10–12 maths, school-contracted,
> parent-funded through the school's fee schedule.**

| | |
|---|---|
| Break-even | ~2,370 seats ≈ **9 schools** |
| Gross margin at 50% WAU | **97.8%** |
| Gross margin at 100% WAU, 4 sessions/wk | **91.2%** |
| Share of annual tuition | 2.4% |
| vs what parents already pay Photomath | 12% |

**Pilot pricing: free for the first three schools**, in exchange for the baseline
diagnostic (`FR-017`), termly outcome measurement, and a reference. The evidence asset is
worth more than three schools of revenue, and free removes the procurement cycle from the
critical path entirely.

**Do not discount below ₹500.** Below that the school count needed for break-even exceeds
what two founders can sign, and a low anchor is very hard to raise later in a market where
the buyer talks to other schools.

---

## 6. What would break this model

| Assumption | Breaks if | Consequence |
|---|---|---|
| ~$0.005/session | `PQ-01` fails and OCR needs a metered service (Mathpix) or multiple retries per turn | Costs rise 3–10×. Still profitable, but the margin cushion goes |
| Device-native speech is acceptable | `PQ-03` shows students reject robotic TTS | Vendor TTS at $0.030/session ≈ 7× cost. Still >80% margin at ₹750, but it changes the LLM budget |
| ~250 students in Grades 10–12 per school | Schools are smaller than assumed | Schools-needed roughly doubles at 125/school. **Verify against a real school before committing to a price** |
| Schools will pay for a point solution | They only buy bundles | Whole GTM changes; partner or be a feature |
| Founders on ₹60k/month | Anyone needs market salary | Fixed cost roughly triples; break-even goes to ~25 schools |
| 30 teaching weeks | Board-exam years compress usage into fewer, heavier weeks | Margin improves, engagement metrics get seasonal — do not read a January dip as churn |

---

## 7. Open

> **On `CQ-01` — not a blocker.** The founders' position is that school size varies too
> much to fix this early, and that is right. The model does not need a single number; it
> needs a range, and the recommendation survives across it:
>
> | Grades 10–12 per school | Schools needed at ₹750 |
> |---|---|
> | 125 (small school) | 19 |
> | 250 (assumed) | 9 |
> | 400 (chain campus) | 6 |
>
> Even at the pessimistic end, ₹750 needs **19 schools** where ₹300 would need **47**.
> The ordering does not change, so the price decision holds without pinning the number.
> Refine it opportunistically as real schools come into view.

| ID | Question | Owner |
|---|---|---|
| **CQ-01** | Typical Grades 10–12 cohort size — refine the range above as real schools appear. Not blocking | CEO, opportunistic |
| **CQ-02** | Will a school add a line to its fee schedule for a third-party tool, or must it come from an existing budget? Determines whether §4's structure exists | CEO |
| **CQ-03** | Does the school-collected parent contribution hold up under DPDP as described? | Needs review before it is offered |
| **CQ-04** | Real `$/session` once `PQ-01` and `SPK-1` have run | CTO |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-08 | CTO (incoming) | Bottom-up model. Finds variable cost is not the constraint; recommends ₹750/student/year on a school-count basis. |

## Related documents

- [`../00-context/03-gate-decisions.md`](../00-context/03-gate-decisions.md) — `GD-12`
- [`../02-prd/00-prd.md`](../02-prd/00-prd.md) §6.1 — the cost ceiling this replaces with a real model
