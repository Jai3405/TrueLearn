---
title: "ADR-011: Safeguarding disclosure escalation"
status: Accepted
date: 2026-09-16
deciders: [CTO, CEO]
---

# ADR-011: Safeguarding disclosure escalation

> **v0.2.0 supersedes the proposed v0.1.0 and reverses two of its six clauses.** The
> original halted the session terminally and notified a named human *at the school* within
> 15 minutes. Both are wrong. Reasoning and citations:
> [`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md) §3.

## Context

A 1:1 tutor talking to 15–18 year olds nightly **will** receive a disclosure of self-harm,
abuse, or acute distress. Certainty, not risk (`RISK-004`, L4×I5 = 20). The product has no
clinical competence and must not pretend otherwise.

Research (Sept 2026) established three things the proposed version did not know:

1. **POCSO §19 binds *"any person"* with knowledge — not schools, not companies, persons.**
   *AAA v. Linda Sema* (SC, 9 July 2026) holds that "knowledge" means receipt of credible
   information, that **internal verification before reporting is not a defence**, and that
   liability attaches to **the individual who received the information directly**.
2. **Abuse and self-harm have opposite legal characters.** Abuse is a criminal reporting
   duty. Self-harm is *not reportable to anyone* — attempted suicide is decriminalised
   (MHCA 2017 §115). One is compliance; the other is duty of care with no safe harbour.
3. **There is no named safeguarding human at an Indian school at 9pm.** No out-of-hours
   practice exists; the regulators' answer is to publish a helpline number. Many TG/AP
   private schools are state-board, so CBSE's counsellor mandate does not reach them.

## Decision

### 1. Classify by *what was disclosed*, not by severity score

A single "severity" number cannot carry this, because the correct action for a high-severity
self-harm disclosure (notify parent) is the **forbidden** action for a high-severity abuse
disclosure where the parent is implicated. Two pipes, not one ranked queue.

### 2. The tiers

| Tier | Trigger | Action | Human SLA |
|---|---|---|---|
| **0** | Any distress signal | In-session, automatic. #chatsafe-style non-clinical response, helplines on screen, **session continues** | None |
| **1** | Low concern — exam stress, bullying, no imminent risk | Review, then notify school counsellor with a factual summary, **not the transcript** | 1 business day |
| **2** | Self-harm / suicidal ideation | Notify parent (SMS + call, scripted, no transcript quoted). School counsellor next day. **112 if imminent risk and parent unreachable.** *Exception: if the transcript implicates the parent → Tier 3* | **60 min, 24×7** |
| **3** | **Sexual abuse, or parent/guardian implicated** | **DCPO reports to SJPU / local police. No verification step. School and parent are not called first.** Then Principal + CSA committee, and Childline 1098. **Parent not notified where implicated.** Transcript under legal hold | **60 min, 24×7** |
| **4** | Credible threat of harm to others | DCPO → police | **60 min, 24×7** |

### 3. The session does not terminate

**Reversed from v0.1.0.** `HaltedSafeguarding` becomes **`SupportMode`** — the tutor stops
*tutoring* and does not return to it, but stays present. It does not counsel, diagnose,
advise, or claim to be human (`FR-022`).

No major provider hard-stops on a distress disclosure. **A student who says something
frightening and watches the app close on them has been punished for disclosing.** That
builds a product which teaches concealment — worse than one that never asked.

### 4. The named human is inside this company

**Reversed from v0.1.0.** Because POCSO liability attaches to an individual and the school
is asleep:

| Role | Duty |
|---|---|
| **DCPO** (named, published) | Owns every Tier 2–4 case. **Personally makes POCSO reports to SJPU/police** |
| **Deputy DCPO** (named) | Evenings, weekends, leave. Non-negotiable — out-of-hours *is* the risk window |
| **Safeguarding Reviewer** (rota) | The human review gating every notification. **Does not investigate** |
| **Grievance Officer** (IT Rules 2021) | Public intake; routes to DCPO |

The school's counsellor and Principal are captured by **name, email and phone at contract
signature, re-verified each term**, and are a **next-business-day** destination — never the
60-minute one.

### 5. Transparency before disclosure, not after

Onboarding screen, Telugu and English, plain language: *"I'm not a secret. If you tell me
someone is hurting you, or that you might hurt yourself, a real person will see it and will
help."* Khanmigo's model. A confidentiality promise we cannot keep is the one thing that
would make this product genuinely dangerous.

### 6. Unchanged from v0.1.0

- Screen **every** student turn, before tutoring logic — not as a filter on the reply.
- **Append-only** audit log of every flag, review decision and notification, surviving
  consent withdrawal. Retained **180 days minimum, in India** (CERT-In). In a §21
  prosecution this log is the evidence that a report was made, and when.
- The tutor never claims to be human (`FR-022`).

## Consequences

**Good.** Over-reporting is free and under-reporting is a crime — POCSO §19(7) gives
good-faith immunity. The asymmetry is total, so thresholds should be set loose. False
positives now cost an interrupted tutoring turn rather than a terminated session, which is
what makes a loose threshold affordable.

**Bad, and expensive.** A 60-minute 24×7 review SLA with two founders and no budget is a
pager one of them always carries. Modelled in the action pack §3.5: viable to ~3 schools,
**breaks at ~5**, and the lever is **detector false-positive rate**, not disclosure
prevalence. Halving false positives doubles the schools two people can serve. That makes
detector precision a commercial metric and a hiring trigger, and it belongs in the cost
model.

**Unresolved and material.** Whether an unreviewed machine flag fixes the company with
"knowledge" under §19 is **not settled by any Indian authority**. If it does, the review SLA
is not an ops target — it is criminal exposure. Lawyer Q1, action pack §7.

## Alternatives rejected

- **Halt the session terminally** (v0.1.0). Rejected — see §3.
- **Route everything to the school.** Rejected: does not discharge a personal statutory
  duty, and resembles the "private inquiry before reporting" *Linda Sema* held impermissible.
- **Notify the parent on every serious disclosure.** Rejected: the parent is a common source
  of the harm. Indian guidance (NIPCCD POCSO handbook) already carves this out explicitly.
- **Restrict product hours to those we can cover.** Rejected: evening and weekend home study
  is the entire use case (`GD-02`).
- **One severity-ranked queue.** Rejected: collapses two legally opposite duties into one
  number, and the collapse fails exactly where it matters most.

## Reversal cost

**N/A — this is a launch precondition, not a tradeable decision.** It must be implemented
before one real student uses the product. Slice 4 in the implementation order.

## Open — non-blocking

- **Detector: rules, model, or both?** Probably both, rules as the floor, since a
  model-based detector can itself fail empty (`ADR-015`). Measure precision/recall in
  **`SPK-4`** — it drives the hiring cliff.
- Ring-test all helplines before launch, re-test quarterly.

## Related

- [`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md) §3 — citations, helplines, lawyer questions
- [`../04-design/00-hld.md`](../04-design/00-hld.md) §7 — critical path, corrected by this ADR
- `ADR-015` — empty output is an error, which the detector inherits
