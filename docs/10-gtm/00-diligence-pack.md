---
title: Technical Diligence Pack
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 9 — GTM & Diligence
inputs: [00-context/01-claims-audit.md, 09-ops/00-cost-model.md, 05-adr/ADR-011, 07-quality/02-test-and-eval-strategy.md]
---

# Technical Diligence Pack

> Written for the person at a fund whose job is to find the hole. Everything here is either
> measured, cited, or explicitly labelled as unknown.
>
> **`FD-05` decided 2026-09-16: all claims-audit rewrites adopted.** The deck and site must
> be changed to match §3 before either is shown to anyone.

---

## 1. The five-minute narrative

**The problem.** A student stuck on a maths problem at 9pm has two options: an answer engine
that shows them the solution, or nobody. Photomath and Gauth have hundreds of millions of
downloads between them and they optimise for the wrong thing — the answer. Parents pay
₹20,000–40,000 a year for maths tuition precisely because a human asks questions instead.

**Why this is hard, and why it is an engineering problem rather than a prompt.** An LLM's
default behaviour is to be helpful, and helpful means answering. **We measured it: a prompt
with no anti-answer rules leaks the answer on 94.4% of adversarial attempts.** A role-locked
prompt plus an independent output guard takes that to **0% across 36 attacks in 12
categories.** The guard inspects every reply before a student sees it, and regenerates or
blocks. That is the product.

**What we measured, not what we hope.**

| | Result |
|---|---|
| Answer leakage: weak prompt → role-locked prompt + guard | **94.4% → 0%** |
| Handwriting transcription, real human handwriting (MathWriting) | **87.5%** |
| Adversarial corpus | 36 attacks, 12 categories, CI merge gate at <5% |

**What the 87.5% forced us to build.** One line in eight is misread, so the tutor confirms
what it read before it reasons (`FR-026`). Without that it coaches working the student never
wrote, confidently — which destroys trust faster than admitting it cannot read.

**The wedge.** Grades 10–12 maths, Telangana and Andhra Pradesh, sold to schools. English
only. No avatar, no canvas, no real-time voice — each removed on arithmetic, not taste (§4).

**The thing nobody else has.** A 1:1 conversational product used by 15–18 year olds at home
in the evening **will** receive a disclosure of self-harm or abuse. We have a designed,
tiered, legally-grounded response with a named officer and verified 24×7 Telugu helplines.
**No Indian edtech has published one** — Vedantu's child-safety page does not mention POCSO
or self-harm at all, and we found nothing from PhysicsWallah or BYJU'S. It is a procurement
asset and a category-level litigation shield.

---

## 2. The questions a technical partner will actually ask

Answered as I would answer them in the room.

**"What stops the model just giving the answer?"**
An independent guard outside the model. The prompt is necessary and insufficient — measured
94.4% leakage without the guard's rules, 0% with them. The guard fails closed: if it cannot
verify a reply, the student gets a designed fallback, never an unverified answer. It runs as
a CI merge gate, so a model upgrade cannot silently re-introduce leakage.

**"Isn't this just a system prompt? Where is the defensibility?"**
The prompt is not the moat and we do not claim it is. What is hard to copy is the
**measurement apparatus and the compliance surface**: a 36-attack adversarial corpus, a
harness that refuses to report a verdict below 90% completion, and a safeguarding escalation
design grounded in POCSO and DPDP. **Our own moat analysis scores most claimed moats at
0–12 months.** The honest position is that the wedge buys time, not permanence.

**"Why won't Google or OpenAI do this?"**
They might build the tutor. They will not do Telangana state-board curriculum mapping,
school-by-school safeguarding contracts with named counsellors, or DPDP §9 children's-data
posture for a market this size. Defensibility is in the distribution and compliance layer,
not the model layer — which is also why we keep a provider abstraction and treat the model
as swappable.

**"What happens when a child discloses abuse at 9pm?"**
Five tiers, classified by *what was disclosed* rather than by severity, because Indian law
treats them oppositely. **Sexual abuse is a criminal reporting duty under POCSO §19 binding
"any person" with knowledge** — reported by our named DCPO directly to the Special Juvenile
Police Unit, with no verification step, because *AAA v. Linda Sema* (SC, 9 July 2026) holds
that checking first is not a defence. **Self-harm is reportable to nobody** — attempted
suicide is decriminalised — so that path is duty of care: stay engaged, surface 24×7 Telugu
helplines, notify a parent *unless the transcript implicates them*. The session never
terminates. Human review inside 60 minutes, 24×7.

**"Your founder is the only engineer and also the safeguarding officer. How does that not
fall over?"**
It falls over at about five schools, and we have the number. The founders carry the pager to
~3 schools; two part-time reviewers (~₹6 lakh/year) are required by school 5. That is a line
in the cost model with a hiring trigger, not a surprise. **The lever is detector
false-positive rate** — halving it roughly doubles the schools two people can cover.

**"What is your DPDP exposure on children's data?"**
The §9(3) prohibition on behavioural monitoring of under-18s is **absolute, with no consent
gateway**, and as a vendor we do not hold the educational-institution exemption. So we store
**no per-student cognitive profile at all** — the schema has no such table, deliberately.
Analytics are cohort-level with **k≥5 enforced as a database `CHECK` constraint**, not a
query filter. The prohibited activity is avoided by construction rather than by policy.

**"You send children's data to a US model. Is that lawful?"**
Yes. DPDP §16 is a **blacklist, not a whitelist** — transfer is permitted unless a country is
notified, and **none has been.** §16 does not commence until 13 May 2027. What we do not
claim is that inference happens in India: most vendor "residency" covers storage only. If a
school requires in-country processing, a regional Vertex endpoint is a configuration change
behind our provider abstraction.

**"What is the biggest thing that could kill this?"**
A safeguarding failure. Not leakage, not accuracy, not cost. One mishandled disclosure ends
the company and, far more importantly, hurts a child. It is why safeguarding is slice 4 of 7
rather than a phase-9 afterthought, and why the one metric gated at **zero** is **misroute** —
a Tier 3 disclosure classified as Tier 2, which would notify a parent who is the abuser.

**"Where are you actually weak?"**
Stated in §5, before you ask.

---

## 3. Deck and website — the claims sheet

**`FD-05` adopted: all rewrites.** The audit found **2 FALSE, 12 MISLEADING and 4
UNVERIFIABLE** across 40 claims. Nothing below is optional; a diligence partner will run
these checks.

### 3.1 Delete outright

| Claim | Why |
|---|---|
| "100% of top CS programs…" | **FALSE** |
| "YC's #1 priority" | **FALSE** — `CL-021` |
| "10× leverage for lateral thinkers" | Unsupportable |
| All four website status indicators | Imply deployments that do not exist. (`O-01`: the site has never been shown to anyone, so this is housekeeping — still do it) |
| "84% cohort coverage" | Unsupportable |
| "Live 60fps SVG" | There is no canvas (`ADR-006` moot) |

### 3.2 Replace with the defensible version

| Instead of | Say |
|---|---|
| "98% cost advantage" | **66%** — and lead with avatar-cost avoidance, which is the real and much larger lever |
| NBER "Socratic" tutoring | **+0.288 SD across 90 studies.** Drop "Socratic" — the paper does not define its subject that way |
| Bloom's 2 sigma | Cite as *framing*, and pre-empt the replication critique yourself |
| "$30–50 ACV" | Per **student** per year — and now superseded by the platform-fee structure |
| Market sizing | **Rebuild bottom-up from named Telangana/AP accounts** — see §3.3 |

### 3.3 ⚠️ The claims audit's own recommendations are partly stale

The audit was written **before the India pivot** (`ADR-003`). Its §6 advises *keeping the GCC
market sizing* (1,783 schools, 1.8M students, $14.2B tuition) — **that is now the wrong
market.** Adopting §6 verbatim would reinstate sizing for a geography we are not selling in.

**The market slide must be rebuilt from scratch for Telangana/AP, bottom-up from named
schools**, not adapted. This is the single largest remaining piece of unwritten work in the
deck, and `CL-052` (SOM incoherent by 17×) is not closed until it exists.

### 3.4 Add — the strongest citation is missing

**Bastani et al., PNAS 2025.** Unguarded AI assistance actively *harms* learning while
guardrailed AI does not. It is the best external validation of the guard that exists, and it
is absent from the current deck.

### 3.5 The honest deck is the stronger deck

> A preregistered trial validates the mechanism. A PNAS field experiment shows unguarded AI
> harms learning while guardrailed AI does not. Human tutoring works at +0.288 SD and costs
> ~$2,500 per student. We measured our own guard at 94.4% → 0% leakage. We are building the
> guardrailed version at a fraction of tuition, for the two grades where a school's
> reputation is made.

Every sentence there survives diligence. The current version does not.

---

## 4. What we removed, and the arithmetic that removed it

A partner will ask why the product is smaller than the deck. This is the answer, and it
reads as rigour rather than retreat.

| Removed | Arithmetic |
|---|---|
| **Photoreal avatar** | $0.26–0.37/streaming minute = **$5.20–7.40 per 20-minute session**, against single-digit dollars of annual revenue per student. ~**400×** the rest of session cost. Kept as an investor-demo build only |
| **Full-duplex sub-second voice** | ~$0.023/min ≈ **$28/student/year** against ~$3 of revenue at the old price. Push-to-talk ships; Khanmigo leads the market on it |
| **Infinite canvas** | A handwriting canvas on a 6-inch screen with a finger is a different product. Input is a photograph of paper |
| **Browser-resident model** | ~3 GB download. VAD is a 1–2 MB signal-processing task, not a model |

---

## 5. Where we are weak — stated before you find it

| Weakness | True? | What we are doing |
|---|---|---|
| No legal entity | **Yes** | Private Limited, Telangana. ₹15k, ~3 weeks, in progress |
| No pilot, no revenue, no signed school | **Yes** | Three free pilots, June 2027. [`01-pilot-design.md`](01-pilot-design.md) |
| One engineer, who is also Deputy DCPO | **Yes** | 3.5 build-days/week is in the plan, not hidden. Hiring trigger at school 5 |
| Safeguarding detector unmeasured | **Yes** | `SPK-4`. Its false-positive rate sets the hiring cliff |
| **No child has used this yet** | **Yes** | The most uncomfortable one. `PQ-03` — is device-native TTS acceptable to a teenager? — is still unanswered |
| Moats are 0–12 months | **Yes** | Our own analysis says so. The wedge buys time, not permanence |
| Effect size unproven by us | **Yes** | **And the pilot will not prove it** — it is underpowered by design. Pilot §4 |

**Two open legal questions we are paying counsel for**, because neither is resolvable by
reading the statute: whether a machine flag no human reads constitutes "knowledge" under
POCSO §19, and whether the DPDP educational-institution carve-out reaches an AI tutor.

---

## Assumptions

Inherits the register from
[`../00-context/00-source-of-truth.md`](../00-context/00-source-of-truth.md) and the phase
documents. **No new assumptions are introduced here, deliberately** — a diligence pack that
introduces fresh claims is a diligence pack nobody has checked.

## Open Questions for Founders

| ID | Question | Why |
|----|----------|-----|
| `GQ-01` | **Who rebuilds the Telangana/AP market sizing bottom-up?** (§3.3) | The largest unwritten piece. `CL-052` is not closed until it exists |
| `GQ-02` | Do you accept that §5 goes in front of investors **as written**? | Volunteering weakness is a credibility trade. It works only if it is complete |
| `GQ-03` | Who owns the deck and website edits in §3, and by when? | `FD-01` and `FD-05` both land here |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Initial pack. Five-minute narrative, eight diligence questions answered, claims sheet under adopted `FD-05`, removal arithmetic, stated weakness list. Flags that the claims audit's own §6 predates the India pivot and its market-sizing advice is stale. |

## Related documents

- [`01-pilot-design.md`](01-pilot-design.md) — the evidence this pack will eventually cite
- [`../00-context/01-claims-audit.md`](../00-context/01-claims-audit.md) — the 40-claim audit **(INTERNAL — never send externally)**
- [`../09-ops/00-cost-model.md`](../09-ops/00-cost-model.md) — pricing and unit economics
