---
title: Gate Decisions — Founder Answers, 2026-09-08
status: accepted
owner: CTO (incoming)
version: 1.0.0
last_updated: 2026-09-08
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
---

# Gate Decisions — Founder Answers

> **Authoritative record.** Where any earlier document conflicts with this one, **this one
> wins**. Phase 0 and phase 1 were written under assumptions; this is the first document
> written under answers. Several of those assumptions turned out to be wrong, and the
> corrections are recorded here rather than quietly patched.

---

## 1. Company reality — the answers that reset the plan

| ID | Question | Answer | Consequence |
|----|----------|--------|-------------|
| **O-01** | Has the website been shown outside the team? | **No — nobody outside yet** | `C-001` drops from **Critical to Low**. It is now a housekeeping edit, not a correction to anyone. Still fix it before it is ever sent |
| **O-03** | Are the founders full-time? | **Both full-time already** | `C-003` resolved. Schedules stand. But combined with `O-08`, the clock is *personal* runway |
| **O-04** | Which market for the first pilots? | **Telangana / Andhra Pradesh first** | **Inverts `A-013`.** See §2 |
| **O-06** | Hub71 status? | **Not applied** | Every UAE claim on the site is aspirational. Cohort 21 closes Feb 2027, starts Sept 2027 — a 12–24 month path |
| **O-07** | Any school commitment? | **Nothing at all** | Discovery is pure research. `A-014` confirmed |
| **O-08** | Cash position? | **No capital raised; zero budget** | No paid external counsel, no paid tooling, no contractors. Everything runs on free tiers and founder time |
| **O-09** | Legal entity? | **None anywhere** | **Blocks a real school pilot.** A school cannot contract with an individual, and processing children's data without a Data Fiduciary entity puts the exposure on the founders personally |
| **O-02, O-05, O-10** | COO's shipped systems / B2C scope / IP ownership | Superseded or deferred | `O-02` is moot — the CTO builds (§3). `O-05` resolved implicitly by the school-pricing decision. `O-10` remains open, low priority |

### The situation, stated plainly

Two full-time founders, one of whom writes the code, with **zero capital, no entity, no
customer, and no product**. That is a legitimate and common starting point. It is not the
company the deck describes, and every plan from here must be built for it rather than for
the funded version.

---

## 2. `A-013` was wrong — India first, not GCC

**Phase 1 Discovery ran on `A-013`: GCC/MENA first, India as R&D only. That assumption is
now revoked.** My GCC-first recommendation goes with it.

**A-017 (replaces A-013):** the first pilots run in **Telangana / Andhra Pradesh**, India.
GCC is deferred indefinitely.

**Why this is defensible.** With zero capital, distribution you already have beats a market
you would have to buy your way into. The CEO's family business knows these school chains;
that gets real students in front of the product in weeks rather than quarters. It is the
correct call for this company's actual constraints.

**What it costs — and this is not negotiable by preference.**

| Broken by the switch | Detail |
|---|---|
| **The $30–50/student/year price** | That is **11–18% of an entire Indian private-school annual tuition** (urban ₹31,782 / rural ₹19,554) and *above* the ₹1,440–3,000/yr enterprise ceiling that buys a full ERP **plus devices**. Mid-market Indian school ERP runs ₹9,000–20,000/year *for the whole school* — about **$0.75/student/year** |
| **The unit-economics model** | Rebuilt bottom-up from a ~$2.50–4.50/student/year revenue ceiling. This is what forced the decisions in §4 |
| **The compliance regime** | India DPDP Act becomes primary (commences **13 May 2027**). UAE Child Digital Safety Law (`RISK-005`) drops out of scope, removing the four-month deadline |
| **The competitive set** | Not Khanmigo and Google. **Physics Wallah** (listed, AI Guru already takes speech input, 2.82M queries/month), **Extramarks** (AI suite, same buyer), and the large chains that **build in-house** (Sri Chaitanya → Infinity Learn, $50M; Orchids → K12 Techno/Eduvate) |
| **The GCC findings** | The GEMS AI Hub opening, Alef's missing voice product, and the Khanmigo US-only gap are all now **parked, not deleted**. They remain the best second market |

---

## 3. `A-015` was wrong — the CTO builds

**A-015 assumed neither founder writes production code. Revoked.**

**A-018 (replaces A-015):** the incoming CTO is the sole engineer. The 90-day scope is what
**one person** can ship, on free tiers, alongside everything else a founder does.

This makes the non-goals list the most important document in the set. Every item kept is a
week not spent on the thing that gets a student in front of the product.

---

## 4. Product decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| **GD-01** | **The 3D Socrates avatar is an investor-demo build only.** It does not ship in the student product | Tavus, the only avatar vendor publishing real rates, is **$0.26–0.37/streaming minute**. A single 20-minute session costs **$5.20–7.40** against **~$3 of annual revenue per student**. At two sessions a week it is roughly **100× underwater**. Keeping it as a separate demo preserves the pitch asset and the economics |
| **GD-02** | **v0 voice is push-to-talk.** Full-duplex sub-second barge-in is deferred | Speech-to-speech at ~$0.023/min is ~**$28/student/year** against ~$3 of revenue — still ~10× underwater. Khanmigo leads the market on push-to-talk alone. Reopens if the price model changes |
| **GD-03** | **Grade band: 10, 11 and 12** | Board-exam and competitive-exam years; strongest willingness to pay in India |
| **GD-04** | **Subject: maths only** | 83% of paid private tutoring demand. ⚠️ **Note this excludes NEET entirely** — NEET is physics, chemistry and biology, with no maths. Coverage is Grade 10 board maths + JEE maths |
| **GD-05** | **Curriculum: CBSE as the base graph; AP/Telangana state board and JEE as delta mappings** | The founder answered "all of the above". Three independent graphs are not tractable for a solo builder — but JEE maths is built on CBSE Class 11–12 and state-board Grade 10 maths overlaps CBSE substantially, so one base plus deltas delivers all three honestly. **Flagged for correction if read differently** |
| **GD-06** | **Language: English only** | Most AP/Telangana private schools are English-medium. Confirms `A-005`. Do not select vendors that foreclose Telugu later |
| **GD-07** | **Analytics: cohort-only aggregates. No persisted per-student cognitive profile** | Removes the single largest legal exposure. DPDP §9(3) is an **absolute prohibition** on behavioural monitoring of under-18s with **no consent gateway**, and as a vendor we do not hold the educational-institution exemption. Teachers see "Grade 10 section B struggles with quadratic factorisation", never a named student's profile |
| **GD-08** | **90-day goal: one build serving both a real pilot and the investor demo** | Achievable only if the non-goals hold |
| **GD-09** | **Budget: zero.** `SPK-1` runs on free tiers (Gemini free tier, free OpenRouter models) | Costs time, not money |

### Still open

| ID | Open decision | Blocking | Owner |
|----|--------------|----------|-------|
| **GD-10** | **Primary device for v0** — shared Android phone / family laptop / school tablet | **Blocks the PRD.** A handwriting canvas on a 6-inch screen with a finger is a different product and would change the wedge | **CEO — asking school contacts this week** |
| **GD-11** | **Canvas engine.** The infinite-canvas override was raised but not resolved; PenEcho's AGPL-3.0 network copyleft may require publishing our source | `ADR-006` at the TAR gate. **Recommendation: MIT-licensed engine (Excalidraw or Konva)** rather than PenEcho or tldraw (not open source) | CTO |
| **GD-12** | **Pricing model.** Founder asked for a bottom-up cost model before deciding | Requires the phase-8 cost model, pulled forward | CTO |
| **GD-13** | **Entity formation.** No entity blocks any real pilot with children's data | Founder decision; ~$500 was declined under zero budget | CEO |

---

## 5. New and revised risks

| ID | Risk | L | I | Score | Note |
|----|------|---|---|------:|------|
| **RISK-023** | **No legal entity blocks the pilot.** A school cannot contract with an individual, and processing minors' data without a Data Fiduciary puts liability on the founders personally | L5 | I4 | **20** | Building and testing on synthetic data is fine. Real students are not, until `GD-13` resolves |
| **RISK-024** | **Grade 11–12 is the most contested segment in Indian edtech.** Physics Wallah is listed with an AI tutor already taking speech input; Allen owns Doubtnut; Sri Chaitanya built Infinity Learn with $50M | L4 | I4 | **16** | Grade 10 board maths is the less contested half of the band. Consider leading there |
| **RISK-025** | **Solo builder, zero budget, dual 90-day goal.** One person shipping both a real pilot and an investor demo, financed by nothing | L4 | I3 | **12** | The twelve non-goals are the mitigation. Every override costs a week |
| **RISK-005** | UAE Child Digital Safety Law | — | — | **Descoped** | Out of scope while India-first. Re-activate if GCC returns |
| **RISK-006** | India DPDP §9(3) behavioural monitoring | L4 | I4 | **16 → 8** | **Substantially mitigated by `GD-07`.** Cohort-only aggregates avoid the prohibited activity by design |
| **RISK-008** | Published claims problem | L4 | I4 | **16 → 4** | **Mitigated by `O-01`** — nothing was sent to anyone. Still fix the site |

---

## 6. What changes in the existing documents

| Document | Change |
|---|---|
| [`00-source-of-truth.md`](00-source-of-truth.md) | `O-01`–`O-10` answered; `C-001` downgraded; `C-003`, `C-004`, `C-007` resolved; `A-013`→`A-017`, `A-015`→`A-018` |
| [`../01-discovery/04-wedge-and-non-goals.md`](../01-discovery/04-wedge-and-non-goals.md) | Wedge re-aimed at India, Grades 10–12, CBSE-base. Non-goal #1 amended (avatar → demo-only build), #2 confirmed (push-to-talk), #7 **reversed** (India is now the market, not a non-goal) |
| [`../01-discovery/02-differentiation-and-moat.md`](../01-discovery/02-differentiation-and-moat.md) | The GCC distribution window — the only asset that existed today — **no longer applies**. See §7 |
| [`decision-log.md`](decision-log.md) | `FD-01`–`FD-05` resolved; `ADR-002`, `ADR-003`, `ADR-012` decided |

---

## 7. The consequence nobody has priced yet

Phase 1 concluded that exactly one defensible asset existed today: **a 12–24 month GCC
distribution window** where Khanmigo cannot sell students a seat, Google is generic, and
Alef has no voice product.

**Choosing India first gives that up.** In exchange you get distribution you actually have,
which is the right trade for a company with no capital — but it means the honest position
is now:

> We have no moat, no window, and no capital. What we have is access to schools nobody
> else is talking to, and roughly twelve months to convert that access into a curriculum
> graph and an evidence base before someone with money notices the segment.

That is a harder story than the deck tells, and it is still a fundable one — but only if
the twelve non-goals hold and the 90 days produce a real student using real software.

**The single highest-value action this week is not code.** It is `GD-10`: ask three school
contacts what device a student actually has at home. If the answer is "a shared Android
phone", the handwriting-canvas wedge does not survive, and it is far better to learn that
in week one than in month four.

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-09-08 | CTO (incoming) | Founder answers to O-01–O-10 recorded. A-013 and A-015 revoked. 9 product decisions, 4 open, 3 new risks. |
