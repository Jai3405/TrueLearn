---
title: Recommended Wedge and v1 Non-Goals
status: draft — GATE DECISION REQUIRED
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-08
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 1 — Discovery
---

# Recommended Wedge and v1 Non-Goals

> **This is the gate deliverable.** Everything downstream — the PRD, the architecture, the
> hiring plan, the cost model — is derived from the decision on this page. It is also the
> most opinionated document in the set, and the one most worth arguing with.

---

## 1. The recommendation, in one paragraph

> **Build the maths tutor that watches the page.**
>
> A Grade 9–11 **maths-only** after-school companion for **GCC international schools**, in
> which the student works a problem on a drawable canvas and the tutor reads their working
> **line by line as they write it** — catching the error at the moment it happens, asking
> the next question instead of supplying the next step, and never handing over the answer
> under a leakage guarantee the school can verify and the student cannot switch off. Voice
> is the input layer, not the headline. Sold to **school groups**, not schools. Value
> reaches the student and the parent with **zero teacher action required**.

---

## 2. Why this wedge and not the deck's

| Dimension | The deck's positioning | Recommended wedge | Why |
|---|---|---|---|
| Subject | "K-12 STEM" | **Maths, Grade 9–11** | Maths is **83% of UAE paid private tutoring** demand; science 58%. One subject makes the axiom graph tractable |
| Hook | 3D Socrates avatar + voice | **The tutor reads the student's own working** | Every incumbent renders visuals *at* the student; almost none read the student's handwriting. It is the one capability that is both differentiated and attacks the 15%-engagement problem — you don't have to *decide* to ask |
| Enforcement | A system prompt | **A measured leakage SLO** | A prompt is worth 0 months (`02-differentiation-and-moat.md` §2). A verifiable guarantee is counter-positioning a general assistant structurally cannot copy |
| Buyer motion | Schools | **School groups (B2O)** | Alef sells 5 groups / 28 schools in one announcement. GEMS alone is 90+ schools, 200k students — roughly the entire claimed SOM from one relationship |
| Engagement driver | Teacher dashboard | **Parent + cohort social proof** | Parent WTP moves **+60%** on perceived peer adoption and is **unmoved** by safety evidence. And 27–67% of school software licences go unused when a teacher must drive them |
| Teacher role | Core of the value prop | **Optional beneficiary** | `RISK-021`. The dashboard is what gets *sold*; it must never be what makes the product *work* |
| Market | GCC + Telangana/AP + SE Asia | **UAE first, one country** | Khanmigo cannot sell students a seat in GCC; India prices at ~10× below the model and has a listed incumbent with voice already shipping |

---

## 3. What makes this defensible for long enough

Restating the honest position: **the window is distribution, the moat is what we build
during it.**

- **The window (12–24 months):** Khanmigo's student product is US-only. Google is free but
  generic, with no curriculum depth. Alef owns Abu Dhabi's school day to 2033 and has **no
  voice product**. GEMS is publicly soliciting partners.
- **The moat we must build inside it:** the enforced-withholding guarantee with its eval
  harness, and the curriculum-mapped axiom graph for one board. Neither exists. Neither is
  currently funded. Both take 2–3 years to mature and start paying back inside twelve
  months.

If the window is spent building the avatar, the window closes and nothing durable has been
built. That is pre-mortem Narrative 1, and it is the most likely way this company fails.

---

## 4. The v0 definition — what "pilot-ready" means

Three schools in one UAE group, one year group, one subject, one term.

**Must have:**

1. Student draws or writes maths working on a canvas; the tutor reads it and responds to
   *their* reasoning, not to a typed question.
2. Enforced answer-withholding with a **measured leakage rate under 5%** against the
   adversarial suite, reported per tenant.
3. Push-to-talk voice in and spoken response out, with a **text-parity path** (WCAG 2.2 AA;
   a voice-only product is a procurement blocker and excludes deaf/HoH students).
4. SSO + automated rostering (Google Workspace for Education first — it is the GCC
   substrate).
5. **UAE Child Digital Safety Law compliance**: age verification, verifiable parental
   consent, consent withdrawal, privacy-by-default. **Deadline 1 January 2027.**
6. DPA, subprocessor list, data-residency statement, DPIA.
7. Safeguarding disclosure detection and a named-human handoff.
8. Baseline attainment capture **before** the first session, or the pilot proves nothing.
9. A teacher *mirroring* view — openable, never required.

**Success criteria for the pilot** — set now, so we cannot move them later:

| Metric | Threshold | Why this number |
|---|---|---|
| Weekly active students / eligible | **> 35%** | Khanmigo achieves ~15%. Below 30% we have not beaten the incumbent's core weakness and the wedge is wrong |
| Median session length | > 8 minutes | Below this, students are bouncing off the refusal |
| Answer-leakage rate | **< 5%** | The brand promise, measured |
| Sessions ending in student abandonment to another tool | Instrumented, < 25% | Substitution to Gauth is the real competitor |
| Teacher actions required for value delivery | **0** | Architectural, not aspirational |
| Renewal intent at term end | 2 of 3 schools | The only commercial signal that matters |

---

## 5. What we deliberately will NOT build in v1

Each of these is defensible to build eventually. None earns its place before a pilot.

| # | Not building | Why not | Revisit when |
|---|---|---|---|
| 1 | **The photoreal 3D Socrates avatar** | Avatar minutes are **~13× the entire voice+LLM pipeline** ($0.26–0.37/min vs ~$0.023/min); it adds a render hop to the interrupt path and an accessibility burden. And MagicSchool — 10,000 schools — reportedly **de-anthropomorphised its student tutor in Feb 2026 citing parasocial risk**. The market is retreating from this, not advancing toward it. It is a pitch asset, not a learning asset | Never as default. Optional demo skin only |
| 2 | **Sub-second full-duplex barge-in** | The hardest engineering in the product, and **Khanmigo ships push-to-talk and leads the market**. We do not know that barge-in changes any outcome. `SPK-2` measures the floor first | After `SPK-2`, if measurement shows it moves engagement |
| 3 | **The browser-resident Gemma model** | ~3 GB first-load on managed Chromebooks and iPads, no published TTFT, WebGPU unavailable on much of the fleet — and the job it was assigned (VAD) is a 1–2 MB signal-processing task | Probably never. Use a real VAD |
| 4 | **The 20,000 × 20,000 infinite canvas** | A vanity spec. A student works one problem on roughly one screen. The size buys nothing and drags in an **AGPL-3.0 dependency** that is a Series-A and procurement blocker | If a real user need for spatial navigation appears |
| 5 | **PenEcho as the canvas engine** | AGPL-3.0-only network copyleft on the core dependency. Use an MIT-licensed engine (Excalidraw, Konva) or buy the commercial licence with its cost in the model. **tldraw is not open source** | `ADR-006` at the TAR gate |
| 6 | **The B2C tier** | 4–10× channel arbitrage against the B2B seat, and in India it makes us a Data Fiduciary with **no exemption path** under DPDP §9(3). One motion, one buyer | 18+ months, if ever |
| 7 | **India as a market** | $40/student/year is **11–18% of an entire Indian private-school tuition**; the top of the enterprise band is ~$16–34 and buys a full ERP. Physics Wallah already ships an AI tutor with speech input; the big chains build in-house | After UAE is proven, at a different price and cost structure |
| 8 | **Physics, chemistry, biology** | Maths is 83% of the demand. Each subject multiplies the axiom-graph cost, which is the expensive asset | v2, after maths coverage is deep |
| 9 | **A teacher alerting queue** | Between 27% and 67% of school software licences go unused; a typical teacher already touches 50 tools a year and 70% had no say in choosing them. An alert queue is how this product dies quietly | Never as a requirement. Mirroring view only |
| 10 | **The Feynman reverse-teaching mode** | Genuinely good pedagogy, and not a wedge. It adds eval surface area before we have proven the core loop holds | v2 |
| 11 | **Arabic-language tutoring** | GCC *international* schools teach in English (`A-005`). Adding a language before proving the loop doubles the eval and vendor surface | v2 — but do not select vendors that foreclose it |
| 12 | **Native mobile apps** | Web on school-managed devices is where the pilot lives | After web retention is proven |

**The uncomfortable arithmetic:** items 1–5 are most of what the deck is about. That is the
finding, not an accident — and it is the difference between shipping a pilot next term and
shipping a demo next year.

---

## 6. What would make me wrong

Stated as falsifiable claims, so this can be argued with rather than believed:

1. **If students will not adopt a tool that refuses them** — if `SPK-1` shows we can hold
   the line but `DQ-01` shows nobody chooses it — then the wedge is wrong and the honest
   product is a *teacher* tool, not a student one.
2. **If a head of school will mandate use** (`DQ-04`), the engagement bar drops sharply and
   the parent/social-proof strategy becomes secondary.
3. **If barge-in measurably transforms engagement** in `SPK-2`, item 2 in the non-goals
   moves up the list and the media investment is justified.
4. **If GEMS or a comparable group signs first**, the B2O thesis is confirmed and the whole
   plan accelerates — that single relationship is worth more than the stated SOM.
5. **If Khanmigo opens student access outside the US**, the window closes early and the
   wedge must narrow to curriculum depth and compliance faster than planned.

---

## 7. What I need at this gate

1. **Approve or reject the wedge** — maths-only, Grade 9–11, UAE international-school
   groups, canvas-first, teacher-optional.
2. **Approve or reject the twelve non-goals.** Item 1 (the avatar) and item 2 (barge-in)
   are the ones I expect argument on, and they are the ones with the largest cost
   consequence.
3. **Confirm `A-013`** — GCC-first, India R&D-only — or reject it and I will rework the
   pricing and compliance workstreams.
4. **Start `SPK-3` this week**, scoped **UAE-first**. The Child Digital Safety Law deadline
   is 1 January 2027 and there is no vendor approval list to shelter behind.
5. **Run `SPK-1`.** Two to three days, ~$50. If the model cannot hold the line, none of
   the above matters and we need to know before the PRD.
6. **Make the GEMS introduction.** Their AI Hub is publicly soliciting partners; it costs
   an email and is the highest-leverage action available to the CEO this month.

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-08 | CTO (incoming) | Wedge recommended, v0 defined with pilot success thresholds, 12 non-goals, 5 falsifiers. |

## Related documents

- [`00-problem-and-personas.md`](00-problem-and-personas.md)
- [`01-competitive-teardown.md`](01-competitive-teardown.md)
- [`02-differentiation-and-moat.md`](02-differentiation-and-moat.md)
- [`03-risks-and-premortem.md`](03-risks-and-premortem.md)
