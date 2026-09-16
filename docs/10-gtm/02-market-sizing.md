---
title: Market Sizing — Telangana and Andhra Pradesh, Bottom-Up
status: draft — INCOMPLETE, see §5
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 9 — GTM & Diligence
inputs: [00-context/01-claims-audit.md, 09-ops/00-cost-model.md, 10-gtm/00-diligence-pack.md]
---

# Market Sizing — Telangana and Andhra Pradesh, Bottom-Up

> Replaces the deck's GCC sizing, which `ADR-003` made obsolete, and addresses `CL-052`
> (SOM incoherent by 17×).
>
> **Two figures here are verified. Everything else is an assumption with an ID.** That is
> deliberate: `CL-052` was caused by a number nobody could re-derive, and repeating the
> error in a different geography would be worse than leaving the slide blank.

---

## 1. What is actually verified

| Figure | Value | Source |
|---|---|---|
| Telangana, total schools | **41,762** (2025-26; down from 43,154) | Union education ministry UDISE+ release, [Deccan Chronicle](https://www.deccanchronicle.com/southern-states/telangana/udise-report-telangana-enrolment-rises-29-despite-fewer-schools-girls-outperform-boys-1969193) |
| Telangana, total enrolment | **76,76,413** (+2.9% YoY) | Same |
| Telangana private-school share | Highest among major states | [UDISE+ coverage](https://www.isignal.in/education/why-4-in-10-indian-children-go-to-private-schools-988762) |
| National private-unaided enrolment | 36.8% (2024-25), up from 33.2% (2017-18) | Prof. Arun C Mehta, [UDISE+ analysis](https://educationforallinindia.com/analysis-of-udise-2024-25-data-by-prof-arun-c-mehta/) |

**What is NOT verified, and I could not obtain:** Telangana's private-unaided *school count*,
either state's enrolment split by grade, Andhra Pradesh's totals, and the CBSE-vs-state-board
split. The UDISE+ dashboard exposes these; the published summaries do not, and the full
booklet PDF exceeded what I could retrieve. §5 lists exactly what to pull.

---

## 2. The chain, with every assumption exposed

**Telangana only.** Andhra Pradesh is not modelled here because I have no verified anchor for
it — see §5.

| Step | Value | Basis |
|---|---|---|
| Total enrolment | **76.8 lakh** | ✅ Verified |
| × private unaided share | **~29%** → 22.3 lakh | `A-037` — TG is the highest-private major state; national is 36.8% |
| × share in Classes 10–12 | **~15%** → **3.3 lakh** | `A-038` — **weakest link.** Enrolment falls sharply after Class 10 |
| = **Serviceable market, TG** | **≈ 3.3 lakh students** | |
| ÷ ~250 students in Classes 10–12 per school | **≈ 1,300 schools** | `A-039`; `CQ-01` already ranges this 125–400 |

**`A-038` is where this could be badly wrong.** If Classes 10–12 are 12% of enrolment rather
than 15%, the market is 2.7 lakh; at 20% it is 4.5 lakh. **A ±35% swing on one unverified
assumption** — precisely the kind of thing that produced `CL-052`. Do not put a point
estimate on a slide until §5 is done.

---

## 3. The reframe that makes this defensible

**For this business, market size is nearly irrelevant to planning, and saying so is stronger
than a big number.**

Break-even is **3 schools** (cost model §5). Against ~1,300 addressable schools in Telangana
alone:

| | |
|---|---|
| Schools needed to break even | **3** |
| Share of the Telangana serviceable market | **0.23%** |
| Students needed | ~750 of ~330,000 |
| Schools for a ₹1 crore revenue year | ~15 (**1.2%**) |

> **We need one-quarter of one percent of the private schools in one state to be
> sustainable.**

That sentence survives diligence in a way no TAM figure does, because **it is robust to
`A-038` being wrong by a factor of two in either direction.** At 0.12% or 0.46%, the
conclusion is identical.

**This is the honest inversion of `CL-052`.** The audit found the SOM incoherent by 17×
because it was built top-down to look large. A number built bottom-up to look *small* is both
more credible and more useful — the binding constraint was never how many schools exist, it
is **how many two founders can sign.**

---

## 4. What the deck should say

**Delete the TAM/SAM/SOM funnel.** It is the most-scrutinised slide in any deck, `CL-052` is
arithmetic rather than opinion, and the funnel format invites exactly the top-down inflation
that caused the error.

**Replace it with three lines:**

1. **~1,300 private schools in Telangana teach Classes 10–12** *(derived, `A-037`–`A-039`,
   pending §5 verification)*.
2. **We break even at 3 of them.**
3. **Here are the 8 we can reach through existing relationships, by name** ← *the founders
   must supply this; it is the only part that cannot be researched.*

**Line 3 is the entire slide.** A named list of 8 reachable schools is worth more to an
investor than any market-size figure, because it is the only evidence that distribution is
solvable by these two people. Every seed investor in education has seen a TAM slide; almost
none have seen a named-accounts list.

---

## 5. To finish this — a 30-minute job on the UDISE+ dashboard

`https://dashboard.udiseplus.gov.in` exposes state reports. Pull, for **both Telangana and
Andhra Pradesh**:

| # | Figure | Kills |
|---|---|---|
| 1 | Schools by management — private unaided count | `A-037` |
| 2 | **Enrolment by grade, Classes 9–12** | **`A-038` — the weakest link** |
| 3 | AP total schools and enrolment | The AP gap entirely |
| 4 | Private-unaided enrolment share, per state | `A-037` |
| 5 | CBSE-affiliated school count per state | `A-018` — decides whether a counsellor exists to escalate to |

**Item 5 is not only a market number.** `A-018` determines whether a pilot school has a
mandated counsellor at all, which decides whether `ADR-011` Tier 1 has anywhere to route. It
is a safeguarding input that happens to live in a market dataset.

**Until items 1–4 are pulled, no number in §2 goes in front of an investor.** §3's
break-even framing can, because it does not depend on them.

---

## Assumptions

| ID | Assumption | Confidence | How to kill it |
|---|---|---|---|
| `A-037` | ~29% of Telangana enrolment is private unaided | Medium — TG is the highest-private major state; national is 36.8% | UDISE+ item 1/4 |
| `A-038` | Classes 10–12 are ~15% of total school enrolment | **Low — the weakest link.** ±35% swing on the answer | **UDISE+ item 2** |
| `A-039` | ~250 students in Classes 10–12 per private school | Medium — `CQ-01` ranges it 125–400 | Confirm against real schools |
| `A-040` | AP is broadly comparable to TG in private-school structure | **Unverified** — larger population, likely lower private share | UDISE+ item 3 |

## Open Questions for Founders

| ID | Question | Why |
|----|----------|-----|
| `GQ-01` *(partially closed)* | **Name the 8 schools you can reach through existing relationships** | §4 line 3. The only part of this document that cannot be researched, and the only part an investor will actually weigh |
| `GQ-04` | Will you pull the five UDISE+ figures in §5? | ~30 minutes. Until then §2 stays internal |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Bottom-up replacement for the obsolete GCC sizing. Two verified anchors, four flagged assumptions. Reframes SOM as **share-required-to-break-even (0.23%)**, robust to the weakest assumption being wrong by 2×. Recommends deleting the TAM/SAM/SOM funnel in favour of a named-accounts list. |

## Related documents

- [`00-diligence-pack.md`](00-diligence-pack.md) §3.3 — why the claims audit's own advice was stale here
- [`../00-context/01-claims-audit.md`](../00-context/01-claims-audit.md) — `CL-052`
- [`../09-ops/00-cost-model.md`](../09-ops/00-cost-model.md) §5 — the 3-school break-even this leans on
