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

| ADR | Title | Status | Phase gate | Reversal cost | Related |
|-----|-------|--------|-----------|--------------|---------|
| ADR-001 | Real-time voice loop: build vs buy | `Pending` | 3 (TAR) | **High** — 2–4 months to rewrite mid-flight | `D-1`, `SPK-2`, `C-006` |
| ADR-002 | Photoreal avatar: include, defer, or drop | `Pending` | 3 (TAR) | Low to add later; low to drop later | `D-1` |
| ADR-003 | Primary market and hosting region | `Pending` | 1 (Discovery) | **High** — compliance and curriculum work is not portable | `D-2`, `C-004`, `O-04` |
| ADR-004 | Pedagogy as engineered system vs system prompt | `Pending` | 2 (PRD) | **Highest** — retrofitting evals means rebuilding the product | `D-3`, `A-008`, `SPK-1` |
| ADR-005 | Multi-tenancy and tenant isolation model | `Pending` | 3 (TAR) | **High** — extremely expensive to retrofit | Engagement plan §4 "near miss" |
| ADR-006 | Canvas command protocol and schema versioning | `Pending` | 4 (Design) | Medium — a versioned schema makes migration tractable | `01-claims-audit.md` (parser fragility) |
| ADR-007 | Cloud inference provider and routing strategy | `Pending` | 3 (TAR) | Low-Medium if abstracted behind a router from day one | `C-008` |
| ADR-008 | Edge/browser model: scope, or eliminate | `Pending` | 3 (TAR) | Low | `C-008` |
| ADR-009 | Data residency, retention and deletion policy | `Pending` | 3 (TAR) | **High** — storage topology follows from it | `A-007`, `SPK-3` |
| ADR-010 | Identity, SSO and rostering integration strategy | `Pending` | 3 (TAR) | Medium | Source of truth §5 #1 |
| ADR-011 | Safeguarding and self-harm disclosure escalation path | `Pending` | 2 (PRD) — **not deferrable to phase 7** | N/A — a launch precondition | Source of truth §5 #5 |
| ADR-012 | B2C tier: in or out of the first 18 months | `Pending` | 1 (Discovery) | Medium | `C-007`, `O-05` |

No ADR has been accepted yet. Phase 0 produces no architecture decisions by design — it
establishes what is true before anything is decided.

---

## Non-architecture decisions requiring a founder call

Tracked here because they gate engineering work but are not mine to make.

| ID | Decision | Owner | Blocking | Status |
|----|----------|-------|----------|--------|
| FD-01 | What happens to the deployment claims on the public website | CEO | Any further outbound; investor conversations | **Open — time-sensitive** (`C-001`) |
| FD-02 | Which single market the first three pilots run in | CEO | `ADR-003`, and therefore most of the TAR | Open (`O-04`) |
| FD-03 | Whether both founders go full-time, and when | Both | Every schedule in phase 5 | Open (`O-03`) |
| FD-04 | Budget approval for external counsel on children's data | CEO | `SPK-3` | Open |
| FD-05 | Whether the claims audit's rewrites are adopted in investor materials | CEO | Phase 9 | Open |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-07 | CTO (incoming) | Register opened. 12 pending ADRs, 5 pending founder decisions. |
