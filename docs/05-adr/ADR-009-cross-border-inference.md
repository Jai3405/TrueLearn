---
title: "ADR-009: Cross-border transfer basis for LLM inference"
status: Accepted
date: 2026-09-16
deciders: [CTO, CEO]
---

# ADR-009: Cross-border transfer basis for LLM inference

## Context

Every tutoring turn sends a child's text to an LLM API outside India (`HLD §1`). Student
data at rest is in India (`NFR-007`), but the inference call crosses a border in flight.

This was recorded as **blocking any use of real student data** and gated on `SPK-3`. That
framing was wrong, and wrong in the expensive direction — it treated the strictest
imaginable reading as the default, and would have pushed us toward an India-hosted model we
cannot afford to run.

## Decision

**Cross-border inference is lawful. Proceed. No transfer instrument is required.**

The basis, in order:

1. **DPDP §16 is a blacklist, not a whitelist.** It permits the Central Government to
   *restrict* transfer to a country *"as may be so notified"*. Restriction requires a
   notification naming a country. **No country has been notified as of September 2026.**
   The default is permission — the inverse of the GDPR structure people assume.
2. **§16 and Rule 15 do not commence until 13 May 2027.**
3. **Rule 15 is narrower than reported.** It concerns making personal data available to a
   **foreign State**, not Indian government access to data.
4. The obligations that *do* bind us are **§9 (children's data)** and the security
   safeguards — neither of which is a border question.

**Constraints that attach to this decision:**

- The provider abstraction (`ADR-007`) stays. It is what makes this decision cheap to
  reverse, and reversal is now a live scenario with a dated trigger (13 May 2027).
- **We may not claim "processed in India"** while using a US endpoint. Most vendor "India
  data residency" covers **storage only** — OpenAI's does; **inference stays in the US**.
  Only a regional endpoint such as Vertex AI `asia-south1` commits ML processing to region.
  If a school's legal review demands in-country processing, that is the migration, and the
  abstraction is what makes it a configuration change rather than a rewrite.
- **CERT-In binds from incorporation, not from May 2027**: 6-hour incident reporting, and
  **ICT logs retained 180 days within India**. This is an infrastructure requirement
  `NFR-007` did not cover.

## Consequences

**Good.** The single item marked "blocks any real student data" is removed. No transfer
agreement, no localisation build, no India-hosted model. At our cost structure an
India-resident open-weights deployment was never affordable — this decision is what keeps
the unit economics in `09-ops/00-cost-model.md` intact.

**Bad.** The position depends on a statute **not yet in force** and on the absence of a
notification that could appear in a single gazette entry. This is a *monitored* decision,
not a settled one. Four review triggers are listed in the action pack §8.

**The honest caveat:** lawful is not the same as *saleable*. A school's legal review may
refuse US inference regardless of what DPDP permits. That is a commercial objection with a
technical answer (regional Vertex), and it should be priced before it is promised.

## Alternatives rejected

- **Wait for `SPK-3` before touching real data.** Rejected: the spike was scoped to answer a
  question the statute already answers. Retained only as a standing gazette watch.
- **India-resident open-weights model from day one.** Rejected: solves a problem that does
  not exist, at a cost that ends the company. Revisit only if a customer pays for it, or if
  §16 changes.
- **Contractual SCC-style transfer clauses.** Rejected: DPDP has no such instrument. Adding
  one would be theatre that implies an obligation we do not have.

## Reversal cost

**Low-to-medium, and deliberately so.** Behind `ADR-007`'s abstraction, moving to a regional
endpoint is a provider swap plus a re-run of the eval harness (`FR-021`) to confirm leakage
and transcription accuracy hold on the new model. Days, not months — **provided nobody
bypasses the abstraction.** That is the property worth defending at review.

## Related

- [`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md) §2 — full reasoning and citations
- `ADR-007` — provider abstraction, which this decision depends on
- `ADR-003` — India as primary market
