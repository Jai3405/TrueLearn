---
title: Three-School Pilot Design
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 9 — GTM & Diligence
inputs: [06-implementation/00-implementation-plan.md, 09-ops/00-cost-model.md, 05-adr/ADR-011]
---

# Three-School Pilot Design

> Free for three schools, in exchange for evidence. This document says what evidence, how it
> is collected, what counts as success, and — the part most pilot designs omit — **what
> would make us stop.**

---

## 1. Shape

| | |
|---|---|
| **Schools** | 3, Telangana / Andhra Pradesh |
| **Cohort** | **Class 11** (`GD-17`) — no board exam, so the school will permit experimentation |
| **Size** | ~85 students per school, **~255 total** |
| **Start** | **June 2027**, with the new academic year |
| **Duration** | One full term |
| **Price** | **Free**, in exchange for §2 |
| **Commercial follow-on** | **Class 12** at list price — diligence pack §1, cost model §5 |

**Why Class 11 for the pilot but Class 12 for the sale.** Class 11 has no board exam, so a
principal can say yes without risking a results year. Class 12 has the highest stakes and the
most motivated parents, so it is where the money is. **Prove it where it is safe; sell it
where it is valuable.**

---

## 2. The exchange — what "free" buys us

Free is not a discount, it is a trade, and the trade must be in the contract:

1. **Baseline diagnostic before any tutoring** (`FR-017`). Non-negotiable — without it the
   pilot proves nothing and renewal rests on goodwill.
2. **Endline assessment** at term end, same instrument.
3. **A named comparison section** — an equivalent Class 11 section not using the product.
4. **A named counsellor or safeguarding lead**, with email and phone, re-verified each term
   (`FD-10`).
5. **A reference call** with a prospective school, and permission to name them.
6. **Thirty minutes of teacher time per fortnight** for qualitative feedback.

**If a school will not commit to 1, 3 and 4, do not run the pilot there.** A free pilot that
produces no evidence and no safeguarding route is a cost with no asset at the end of it.

---

## 3. Success criteria

Primary criteria decide whether this continues.

| # | Criterion | Target | Source |
|---|---|---|---|
| **P1** | Weekly active users | **≥35%** | `SM-L1` |
| **P2** | Session completion rate | ≥70% | Session telemetry |
| **P3** | **Confirmed answer leaks reported by teachers** | **0** | Teacher feedback + guard logs |
| **P4** | **Safeguarding misroutes** | **0** | `safeguarding_events` |
| **P5** | Schools expressing paid renewal intent | **≥2 of 3** | Exit interview |
| S1 | L3 ceiling-hit rate | <25% | Pedagogy telemetry |
| S2 | Transcription confirmed-correct | ≥85% | `FR-026` confirmations |
| S3 | Tier 2/3 review inside 60 min | 100% | `SLO-007` |
| S4 | Learning gain vs comparison section | **Report, do not target** | §4 |

**P3 and P4 are absolute.** One teacher saying *"it just told my student the answer"* ends
the product's only differentiated claim. One misroute is a child returned to an abuser.

**P5 is the commercial question and it is deliberately blunt.** Ask plainly at the exit
interview: *"Would you pay ₹6.5 lakh next year?"* A school that loves the pilot and will not
pay has told you something more useful than one that is merely polite.

---

## 4. ⚠️ The pilot cannot prove an effect size, and we should say so first

A diligence partner will probe this, so here is the arithmetic.

Detecting **d = 0.25** at 80% power and α = 0.05 requires roughly **251 students per arm —
about 500 in total.** The pilot has ~255 students, or **~127 per arm** once split against
comparison sections.

At n = 127 per arm, the smallest effect detectable at 80% power is **d ≈ 0.35.**

**The effects we would expect are smaller than that.** Cook et al. report +0.19–0.31 SD; the
Sierra Leone trial reports +0.258 SD ITT. **So the pilot is underpowered for exactly the
range where the true effect probably sits** — and a null result would be uninformative
rather than negative.

**Consequences, and they are binding:**

1. **Learning gain is a secondary outcome**, reported with confidence intervals and labelled
   indicative, not causal.
2. **No pilot effect size goes in the deck as though it were a trial result.** That is
   precisely the `CL-053` class of error the claims audit exists to prevent — and doing it
   *after* commissioning that audit would be worse than never having run one.
3. **A real effect-size claim needs ~500+ students**, i.e. six schools or a multi-term study.
   A Series-A exercise, not a pilot one.

**What the pilot is genuinely for:** does a 16-year-old use it voluntarily, does the guard
hold with real teenagers attacking it, does the safeguarding path work when a real disclosure
arrives, and will a school pay. **All four are answerable at n = 255.** None require a
p-value.

> **The discipline that makes this credible:** write the analysis plan, including S4's
> comparison, **before the baseline is collected.** Otherwise every favourable subgroup
> becomes a temptation — and the audit's whole point was that we do not do that.

---

## 5. Instrumentation, inside the `GD-07` constraint

**There is no per-student profile.** That is a schema fact, not a policy, and it shapes what
the pilot can measure.

| Collected | Granularity | Why it is lawful |
|---|---|---|
| Session count, duration, completion | **Cohort, k≥5** | DB `CHECK` constraint enforces suppression |
| Topic friction | Section × topic × week, **k≥5** | The only analytics table that exists |
| Step-down depth, L3 ceiling-hit rate | Cohort | No individual trajectory retained |
| Guard actions, empty-output rate | System-level | No student identifier needed |
| Safeguarding events | Individual, append-only | **Lawful and required** — POCSO §21 evidence |
| **Baseline and endline scores** | **Individual** | ⚠️ See below |

**The baseline/endline tension, stated openly.** Measuring learning gain per student is on
its face in tension with "no per-student profile." The resolution: baseline and endline are
**assessment records held by the school as Data Fiduciary**, not a behavioural profile built
by us from usage. We receive them as **pseudonymised pairs for analysis and never join them
to session telemetry.**

**That distinction is load-bearing and I am not certain it holds.** It goes to counsel as
part of **lawyer Q2 before the baseline is collected** — not after.

---

## 6. Stop criteria

Written now, while nobody is invested in continuing.

| Halt immediately if | Why |
|---|---|
| **Any safeguarding misroute** | A parent who may be an abuser was notified. Nothing else matters that week |
| **A confirmed answer leak reached a student** | The single differentiated claim is false |
| Tier 2/3 review breaches 60 minutes more than once | The rota does not work, and `GD-15` assumed it would |
| WAU <15% by week 4 | Students do not want it. Better to know in week 4 than in month 4 |
| A school cannot produce a named safeguarding contact | We are operating without an escalation route |

**"Halt" means stop new sessions, not abandon the school.** Existing students keep access to
`SupportMode` resources, and the school gets a written account of what happened. **A pilot
stopped well is recoverable; one quietly allowed to fail is not.**

---

## 7. Operational runway before day one

| Week (rel.) | Item | Owner |
|---|---|---|
| −8 | Contract signed, incl. the §2 exchange and the NCPCR digital-safety allocation | CEO |
| −6 | Named counsellor and Principal captured; **helplines ring-tested** | CEO |
| −4 | Roster CSV; parental consent collected and recorded | CEO |
| −4 | Published safeguarding policy live, Telugu + English | CTO |
| −2 | Baseline diagnostic administered | School |
| −2 | Teacher orientation, 30 min: what it does, what it refuses, how to report a leak | CTO |
| −1 | **Pre-registered analysis plan written and frozen** | CTO |
| 0 | Sessions open | — |

**Consent is a hard gate, not a launch task.** The API refuses to create a session without a
consent row, so a student whose parent has not consented simply cannot start. That is by
design, and it will cause friction in week 1 — plan for it rather than be surprised by it.

---

## Assumptions

| ID | Assumption | Confidence | How to kill it |
|---|---|---|---|
| `A-032` | ~85 Class 11 students per pilot school | Medium | Confirm per school — it drives the §4 power calculation |
| `A-033` | A comparison section is obtainable without the school objecting to withholding the product | **Low-Medium** | Ask early. If refused, S4 becomes pre/post only and weakens further |
| `A-034` | Baseline/endline as school-held assessment records sits outside the `GD-07` prohibition | **Low — untested** | **Lawyer Q2, before baseline collection** |

## Open Questions for Founders

| ID | Question | Why |
|----|----------|-----|
| `PQ-04` | Will the schools accept a **withheld comparison section**? | Without it there is no counterfactual and §4 weakens further |
| `PQ-05` | Who administers baseline and endline — school staff or you? | Affects both cost and the credibility of the result |
| `PQ-06` | Are you willing to **halt a pilot** on the §6 criteria, at a school you know socially? | These are family relationships. Agree it now, not during the incident |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Initial design. Three free schools, Class 11, June 2027. Five primary criteria, stop criteria, instrumentation inside `GD-07`. **States explicitly that the pilot is underpowered for the expected effect size** and forbids presenting a pilot effect size as a trial result. |

## Related documents

- [`00-diligence-pack.md`](00-diligence-pack.md) — where this evidence lands
- [`../06-implementation/00-implementation-plan.md`](../06-implementation/00-implementation-plan.md) — why June 2027
- [`../05-adr/ADR-011-safeguarding-escalation.md`](../05-adr/ADR-011-safeguarding-escalation.md) — the path `P4` measures
