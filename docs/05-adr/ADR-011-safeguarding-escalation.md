---
title: "ADR-011: Safeguarding disclosure escalation"
status: Proposed
date: 2026-09-16
deciders: [CTO, CEO]
---

# ADR-011: Safeguarding disclosure escalation

## Context

A 1:1 voice tutor talking to 13–18 year olds nightly **will** receive a disclosure of
self-harm, abuse, or acute distress. This is not a risk to mitigate, it is a certainty to
design for. There is currently no designed response, and `RISK-004` scores it L4×I5 = 20.

The product is not a counselling service, has no clinical competence, and must not
pretend otherwise.

## Decision (proposed — needs founder sign-off)

1. **Screen every student turn** before tutoring logic runs, not as a filter on the reply.
2. On detection: **halt the session terminally** (LLD §3 — `HaltedSafeguarding` has no exit
   back to tutoring).
3. Deliver a **pre-approved, non-clinical** message. The tutor does not counsel, diagnose,
   advise, or continue the lesson.
4. Notify a **named human** at the school within **15 minutes** (`NFR-011`). A named person,
   not a queue or a shared inbox.
5. Write to an **append-only** audit log that survives consent withdrawal.
6. The tutor **never claims to be human** and never offers friendship (`FR-022`).

## Open questions blocking acceptance

- **Detector: rules, model, or both?** A model-based detector is better at nuance and can
  itself fail empty (`ADR-015`). A rules layer is crude but deterministic. Probably both,
  with rules as the floor.
- **What false-negative rate is acceptable?** The honest answer is "none", which is not
  achievable — so the real question is what review process compensates.
- **Who is the named human** when a school has not designated one? No pilot may start
  without this person identified by name.
- **Out-of-hours.** This product is used at 9pm. A 15-minute notification to someone asleep
  is not a safeguarding process — what is the escalation then?

## Consequences

Some false positives will interrupt legitimate tutoring sessions. **That is the correct
trade.** A halted maths session is recoverable; a missed disclosure is not.

## Status

**Proposed, not accepted.** This is a launch precondition — it must be accepted and
implemented before one real student uses the product.
