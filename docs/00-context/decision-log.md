---
title: Decision Log — ADR Register
status: living
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-07
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
---

# Decision Log — ADR Register

The running index of every architecture decision. Full ADRs live in
[`../05-adr/`](../05-adr/) once phase 4 opens; this table is the single place to see what
has been decided, what is pending, and what it would cost to undo.

**Rule:** anything expensive to reverse gets an ADR before it is built. An ADR states
context, options considered, the decision, its consequences, and an explicit **reversal
cost estimate**. A decision made in a chat message is not a decision.

---

## Status legend

| Status | Meaning |
|--------|---------|
| `Proposed` | Written, not yet ratified at a gate |
| `Accepted` | Ratified; binding on downstream work |
| `Superseded` | Replaced by a later ADR (link it) |
| `Rejected` | Considered and declined; kept for the record |
| `Pending` | Identified as needing a decision; not yet written |

---

## Register

> **TAR gate passed 2026-09-15.** The founder approved all seven subsystem calls and
> confirmed the decision weighting (build effort 30% — solo builder, no budget). The ADRs
> below move from `Pending` to `Accepted`. Full reasoning, weighted matrices and rejected
> options are in [`../03-tar/00-tar.md`](../03-tar/00-tar.md).

| ADR | Title | Status | Phase gate | Reversal cost | Decision / reference |
|-----|-------|--------|-----------|--------------|---------|
| ADR-001 | Voice: push-to-talk, device-native speech | ✅ `Accepted` | 3 | Low — full-duplex is additive later | **Vendor TTS alone is $0.030/session against a $0.017–0.033 budget.** `GD-02`, TAR §2.4 |
| ADR-016 | Transcription: multimodal LLM reads the photo inline | ✅ `Accepted` | 3 | Low — swappable behind `ADR-007` | Measured 87.5% (`PQ-01`); avoids a second vendor and a metered per-page bill. TAR §2.1 |
| ADR-017 | Hosting: managed PaaS, India region | ✅ `Accepted` | 3 | Medium | One engineer cannot also be a platform team. `NFR-007`. TAR §2.7 |
| ADR-002 | Photoreal avatar: include, defer, or drop | ✅ `Accepted` | 1 | Low to add later | **Decided `GD-01`: investor-demo build only, never in the student product at school pricing.** ~100× underwater at Indian revenue per student |
| ADR-003 | Primary market and hosting region | ✅ `Accepted` | 1 | **High** — compliance and curriculum are not portable | **Decided `O-04`: Telangana / Andhra Pradesh, India.** Hosting region follows; India DPDP is the governing regime |
| ADR-013 | Voice interaction mode | ✅ `Accepted` | 1 | Low — push-to-talk → full-duplex is additive | **Decided `GD-02`: push-to-talk for v0.** Full-duplex is ~10× underwater at Indian pricing |
| ADR-014 | Analytics granularity | ✅ `Accepted` | 1 | **High** — schema shape follows from it | **Decided `GD-07`: cohort aggregates only, no persisted per-student profile.** Avoids DPDP §9(3) by design |
| ADR-004 | Pedagogy as engineered system vs system prompt | ✅ `Accepted` | 3 | **Highest** — retrofitting evals means rebuilding the product | **Prompt + independent output guard.** Measured: weak prompt leaks 94.4%, guard holds 0%. TAR §2.2 |
| ADR-005 | Multi-tenancy and tenant isolation model | ✅ `Accepted` | 3 | **High** — extremely expensive to retrofit | **Shared Postgres + row-level security by `school_id`.** RLS in the DB, not the app. TAR §2.5 |
| ADR-006 | Canvas command protocol | ⏭️ `Moot` | — | — | **No canvas in v0** — input is a photograph (PRD §2). Revisit at v1 |
| ADR-007 | Cloud inference provider and routing strategy | ✅ `Accepted` | 3 | Low-Medium if abstracted behind a router from day one | **Thin provider abstraction, one primary.** Two measured model constraints. TAR §2.3 |
| ADR-008 | Edge/browser model | ❌ `Rejected` | 3 | Low | **Eliminated.** ~3 GB download; VAD is a 1–2 MB signal-processing task. `CL-034` |
| ADR-009 | Data residency, retention and deletion policy | `Pending` | 3 (TAR) | **High** — storage topology follows from it | `A-007`, `SPK-3` |
| ADR-010 | Identity, SSO and rostering integration strategy | ✅ `Accepted` | 3 | Medium | **CSV roster for pilot, SSO before school #2.** Reverses the phase-1 position. TAR §2.6 |
| ADR-011 | Safeguarding and self-harm disclosure escalation path | `Pending` | 2 (PRD) — **not deferrable to phase 7** | N/A — a launch precondition | Source of truth §5 #5 |
| ADR-012 | B2C tier: in or out of the first 18 months | ✅ `Accepted` | 1 | Medium | **Decided `O-05`: out.** School-paid model. B2C in India carries no education exemption under DPDP |

**Most ADRs are now decided.** Outstanding: `ADR-009` (data residency — needs `SPK-3`),
`ADR-011` (safeguarding escalation — phase 2), and `ADR-015` (empty/truncated output —
ready to accept). `ADR-006` is moot; `ADR-008` rejected.

---

## Non-architecture decisions requiring a founder call

Tracked here because they gate engineering work but are not mine to make.

All resolved 2026-09-08 — see [`03-gate-decisions.md`](03-gate-decisions.md).

| ID | Decision | Owner | Status |
|----|----------|-------|--------|
| FD-01 | Deployment claims on the public website | CEO | ✅ **Resolved** — never sent to anyone (`O-01`), so it is a housekeeping edit. Still do it |
| FD-02 | Which market the first pilots run in | CEO | ✅ **Decided: Telangana / Andhra Pradesh** (`O-04`). Inverts `A-013` |
| FD-03 | Whether both founders go full-time | Both | ✅ **Resolved** — both already full-time (`O-03`) |
| FD-04 | Budget for external counsel on children's data | CEO | ✅ **Declined** — zero budget (`O-08`). Mitigated by `GD-07`: cohort-only aggregates avoid the prohibited activity by design rather than by legal opinion |
| FD-05 | Whether the claims-audit rewrites are adopted | CEO | 🔲 **Still open** — phase 9 |
| **FD-06** | **Legal entity formation** | CEO | 🔲 **Open and blocking.** No entity anywhere (`O-09`). A school cannot contract with an individual, and processing minors' data without a Data Fiduciary puts liability on the founders personally — `RISK-023` |
| **FD-07** | **Primary device for v0** | CEO | 🔲 **Open and blocking the PRD** (`GD-10`). Founder asking school contacts this week |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-07 | CTO (incoming) | Register opened. 12 pending ADRs, 5 pending founder decisions. |
