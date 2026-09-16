---
title: SLOs, Observability and Incident Response
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 8 — Ops & Cost
inputs: [09-ops/00-cost-model.md, 05-adr/ADR-011, 06-implementation/00-implementation-plan.md]
---

# SLOs, Observability and Incident Response

> Written for a team of one. Every number here is one a single engineer can actually hold,
> which is why some of them are lower than they would be on a slide.

---

## 1. The window that changes everything

**Students use this between roughly 16:00 and 23:00 IST.** Outside that window the product
is idle.

That single fact is the most useful thing in this document, because it means **downtime is
not uniformly expensive.** An outage at 03:00 costs nothing. An outage at 20:00 on a
Wednesday costs a day's usage and a founder's credibility with a school.

So availability is **window-weighted**, maintenance goes in the dead window, and — see §4 —
almost nothing is allowed to wake anyone up.

---

## 2. Service level objectives

| ID | Objective | p50 | p95 | p99 | Why this number |
|---|---|---|---|---|---|
| `SLO-001` | Session start (sign-in → ready) | ≤1.5s | ≤4s | ≤8s | Includes the consent check, which is a DB read |
| `SLO-002` | **Transcription** (photo → "I read this, correct?") | ≤4s | ≤10s | ≤20s | A multimodal call over ~25k tokens. The slowest thing in the product, and the student is watching |
| `SLO-003` | Tutoring turn (text → reply rendered) | ≤2s | ≤5s | ≤10s | Turn-based, not conversational — a 2s pause reads as thinking, not as broken |
| `SLO-004` | **Safeguarding screen added latency** | ≤20ms | **≤100ms** | ≤250ms | Runs on **every** turn before tutoring. This is what forces the rules-first floor |
| `SLO-005` | Availability, **16:00–23:00 IST** | — | **99.0%** | — | ~2.1 hours/month of evening budget. See §2.1 |
| `SLO-006` | Availability, outside that window | — | 95.0% | — | Deliberately loose. Maintenance lives here |
| `SLO-007` | **Tier 2/3 safeguarding human review** | — | **≤60 min, 24×7** | — | **No error budget.** `ADR-011`. The only 100% target here |
| `SLO-008` | Empty tutor turn rate | — | **0** | — | `ADR-015`. Non-zero means a provider adapter forgot |
| `SLO-009` | Guard fallback rate | — | <2% | — | Rising = the prompt is drifting from the model |
| `SLO-010` | Transcription accuracy | — | ≥85% | — | Below this, `FR-026` confirmation is carrying the product |

### 2.1 Why 99.0% and not 99.9%

**99.9% would be a lie.** It allows 26 minutes of downtime per month and assumes someone is
awake to fix things. There is one engineer, who is also the Deputy DCPO, and `GD-15` already
has them carrying one pager. Adding an infrastructure pager would cost build days
(`A-022` — 3.5/week) to protect a window where a fast-follow fix the next morning is a
perfectly acceptable outcome.

**99.0% across the evening window is honest and defensible**, and a school will accept it
because it is stated rather than discovered. Revisit at ~10 schools, which is also when the
safeguarding reviewers arrive and there is someone else awake.

---

## 3. What to instrument

### 3.1 Compliance telemetry — non-negotiable

| Signal | Why it exists |
|---|---|
| Every safeguarding flag: tier, category, `parent_implicated`, detected/reviewed/notified timestamps | **This is the POCSO §21 evidence.** In a prosecution it shows a report was made, and when |
| Every consent grant and withdrawal | `FR-015` lawful-basis evidence |
| Every cross-tenant access denial | An RLS denial spike means either a bug or an attack |
| Every deletion job completion | `FR-023` — 30 days, provable |
| **ICT logs, 180 days, stored in India** | **CERT-In. Binds from incorporation, not 2027** |

### 3.2 Pedagogy telemetry — and the constraint people miss

`GD-07` prohibits a per-student cognitive profile. **So pedagogy telemetry must be
cohort-level or session-anonymous. There is no "track this student's mastery over time."**

That is a real constraint and it rules out the obvious metrics. What survives:

| Metric | Reads as |
|---|---|
| **L3 ceiling-hit rate** | **The single best pedagogy signal available.** How often scaffolding ran out and the tutor had to say "let's come back to this" |
| Step-down depth distribution | Mostly L0 = questions too easy. Mostly L2–L3 = pitched too hard |
| Turns to resolution | Rising = the Socratic loop is grinding rather than guiding |
| Abandonment point in session | Where students quit is where the product is worst |
| Session completion rate | `SM-L1` engagement input |

**The ceiling-hit rate deserves a dashboard of its own.** Leakage says the tutor never
cheats; the ceiling-hit rate says whether it ever actually *helps*. **A product with 0%
leakage and a 60% ceiling-hit rate is a machine that reliably refuses to teach** — and no
metric currently in the PRD would catch that.

### 3.3 Cost telemetry — FinOps for a product whose cost is invisible in code review

| Control | Trigger |
|---|---|
| Per-session cost as a first-class metric | 7-day rolling mean **>$0.020** (33% over the $0.015 budget) → ticket |
| Per-student daily session cap | Hard limit. Protects against a retry loop or a bored student |
| Token count per turn, tracked against dialogue length | Context grows with the conversation — the mechanism that silently triples bills |
| Model identifier logged on every call | So a provider silently re-pointing `-latest` is visible |

**Why this matters more here than in a normal product:** a prompt change adding 300 tokens
of instruction is a one-line diff that reviews as trivial and multiplies the bill across
every turn of every session. **There is no compiler for that.** The cost metric is the only
thing that catches it.

---

## 4. Alerting — one thing pages at 3am

**This is an opinionated section and I will defend it.**

| Severity | What | When |
|---|---|---|
| 🔴 **PAGE, 24×7** | **A Tier 2/3 safeguarding flag unreviewed for 45 minutes** | Always. Fires 15 min before `SLO-007` breaches |
| 🟠 **PAGE, 16:00–23:00 IST only** | Total outage, or error rate >25% | Evening window only |
| 🟡 **Ticket, next morning** | Elevated errors, guard fallback >2%, empty-output non-zero, cost drift, failed deletion job | Queued |
| ⚪ **Dashboard** | Everything else | Reviewed weekly |

**Exactly one condition wakes a human at 3am, and it is a child in distress.**

Everything else waits, because **founder sleep is on the critical path.** The implementation
plan budgets 3.5 focused build days a week; a pager firing for a failed deploy at 02:00
costs most of the next one and saves nothing, since nobody is using the product at 02:00.

**The failure mode this prevents is alert fatigue on the one alert that matters.** If the
safeguarding page is the only page, it gets answered. If it arrives alongside six
infrastructure alerts a week, eventually it doesn't — and that is the exact failure
`ADR-011` exists to prevent.

---

## 5. Incident response

### 5.1 Severity

| Sev | Definition | Response |
|---|---|---|
| **SEV-0** | A safeguarding disclosure was missed, misrouted, or a parent was notified against the Tier 3 rule | **Immediate.** DCPO leads, not the engineer. Preserve everything. Assume a legal obligation |
| **SEV-1** | Cross-tenant data exposure, consent-gate bypass, or data loss | Immediate. **The CERT-In 6-hour clock may be running** — §5.2 |
| **SEV-2** | Product down in the evening window | Same evening |
| **SEV-3** | Degraded quality — leakage regression, transcription drop | Next business day |

**SEV-0 is not an engineering incident.** It is led by the DCPO (`GD-14`); the engineer's
job is preservation and reconstruction, not remediation. Write that down before it happens,
because the instinct under pressure will be to start fixing code.

### 5.2 The CERT-In six-hour clock

**A reportable cyber incident must be reported within 6 hours of *noticing* it.**

The operative word is *noticing*, and it means **you must have a defined noticing process**,
not merely good intentions. Minimum viable version for a two-person company:

1. Auth-anomaly and RLS-denial alerts route to the ticket queue and are **reviewed daily**,
   not weekly.
2. Any SEV-0 or SEV-1 starts a written timeline **at the moment of discovery**, timestamped.
3. The CERT-In reporting template and contact route are prepared **before launch**, not
   drafted during an incident.

Six hours is not long, and most of it will go on deciding whether something is reportable —
so pre-agreeing that borderline cases get reported is the cheap way to stay inside it.

### 5.3 Disaster recovery

| | Target | Note |
|---|---|---|
| **RPO** | ≤24h | Managed Postgres PITR. Honest for one engineer at pilot scale |
| **RTO** | ≤4h | Evening window; longer overnight is acceptable |
| **Never lose** | `safeguarding_events`, `consents` | **Legal evidence, not product data.** Verify they are in the backup set specifically |

**Test the restore once before the pilot and write down how long it took.** An untested
backup is not a backup, and the number you measure is the only honest RTO you have.

---

## 6. What this deliberately does not do

| Not doing | Why |
|---|---|
| Distributed tracing | One service, turn-based. Structured logs with a session ID answer the same questions |
| Multi-region failover | India region only (`ADR-017`). A second region doubles the compliance surface for a pilot |
| 24×7 infrastructure on-call | §4. One engineer, and the product is idle at night |
| Synthetic monitoring outside the window | Would generate alerts nobody should act on |
| Custom metrics platform | Managed PaaS defaults plus a weekly dashboard. TAR §6 |

---

## Assumptions

| ID | Assumption | Confidence | How to kill it |
|---|---|---|---|
| `A-029` | Usage concentrates in 16:00–23:00 IST | Medium-High | Measure in the first fortnight. **If usage is flat across the day, `SLO-005`/`SLO-006` and the whole alerting design need revisiting** |
| `A-030` | A rules-first safeguarding floor can hold `SLO-004` at ≤100ms p95 | Medium | `SPK-4`. If it cannot, the per-turn model call returns and §1 of the cost model breaks |
| `A-031` | Managed PaaS PITR gives ≤24h RPO without extra tooling | Medium-High | Verify at M0, not at the first incident |

## Open Questions for Founders

| ID | Question | Why |
|----|----------|-----|
| `OQ-01` | **Is 99.0% evening availability acceptable to state in a school contract?** | I would rather publish a number we hold than one that sounds better. If a school demands 99.9%, that is a funded-headcount conversation |
| `OQ-02` | Who answers the safeguarding page when the DCPO is on a flight? | `ADR-011` names a Deputy. Confirm the handover is explicit, not assumed |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Initial SLOs, window-weighted availability, alerting policy where only a safeguarding flag pages at night, CERT-In 6-hour process, DR targets. Adds `SLO-001`–`SLO-010`, `A-029`–`A-031`. |

## Related documents

- [`00-cost-model.md`](00-cost-model.md) — the $0.015/session budget this monitors
- [`../05-adr/ADR-011-safeguarding-escalation.md`](../05-adr/ADR-011-safeguarding-escalation.md) — `SLO-007`, the only 100% target
- [`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md) §1 — CERT-In obligations
