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
| ADR-009 | Data residency: cross-border basis for inference | ✅ `Accepted` | 7 | Low-Medium behind `ADR-007` | **Lawful. DPDP §16 is a blacklist and no country is notified**; §16 doesn't commence until 13 May 2027. [ADR-009](../05-adr/ADR-009-cross-border-inference.md) |
| ADR-010 | Identity, SSO and rostering integration strategy | ✅ `Accepted` | 3 | Medium | **CSV roster for pilot, SSO before school #2.** Reverses the phase-1 position. TAR §2.6 |
| ADR-011 | Safeguarding and self-harm disclosure escalation path | ✅ `Accepted` | 7 | N/A — a launch precondition | **5 tiers, split by abuse vs self-harm. Session no longer terminates; the named human is ours, not the school's.** [ADR-011](../05-adr/ADR-011-safeguarding-escalation.md) |
| ADR-015 | Empty or truncated model output is an error | ✅ `Accepted` | 4 | Low | Silence was scoring as good behaviour. [ADR-015](../05-adr/ADR-015-empty-model-output.md) |
| ADR-012 | B2C tier: in or out of the first 18 months | ✅ `Accepted` | 1 | Medium | **Decided `O-05`: out.** School-paid model. B2C in India carries no education exemption under DPDP |

**All ADRs are now decided.** `ADR-006` is moot; `ADR-008` rejected; every other ADR is
Accepted. `ADR-009` and `ADR-011` closed 2026-09-16 — see
[`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md).

> **`ADR-011` v0.2.0 reversed two clauses of its own proposed version**, and both had already
> propagated into the accepted HLD and LLD. The session no longer terminates on a
> disclosure, and the 15-minute named human moved from the school to us. Recorded here
> because a reversed decision that leaves no trace is how a document set starts lying.

---

## Non-architecture decisions requiring a founder call

Tracked here because they gate engineering work but are not mine to make.

Resolved 2026-09-08 — see [`03-gate-decisions.md`](03-gate-decisions.md). **Four are open
again as of 2026-09-16**: `FD-04` reopened, and `FD-08`–`FD-10` are new, all from the
safeguarding research. `FD-08` and `FD-09` block launch.

| ID | Decision | Owner | Status |
|----|----------|-------|--------|
| FD-01 | Deployment claims on the public website | CEO | ✅ **Resolved** — never sent to anyone (`O-01`), so it is a housekeeping edit. Still do it |
| FD-02 | Which market the first pilots run in | CEO | ✅ **Decided: Telangana / Andhra Pradesh** (`O-04`). Inverts `A-013` |
| FD-03 | Whether both founders go full-time | Both | ✅ **Resolved** — both already full-time (`O-03`) |
| **FD-04** | Budget for external counsel on children's data | CEO | ⚠️ **REOPENED 2026-09-16.** Previously declined on zero budget. Two questions now carry **criminal** (POCSO §19 machine-knowledge) and **₹200 crore** (DPDP §9) exposure that no amount of statute-reading resolves. **₹40–80k.** Action pack §7 |
| FD-05 | Whether the claims-audit rewrites are adopted | CEO | ✅ **Decided 2026-09-16: all rewrites adopted.** Deck and site edits listed in `10-gtm/00-diligence-pack.md` §3. ⚠️ Audit §6 predates the India pivot — market sizing must be rebuilt, not adapted |
| **FD-06** | **Legal entity formation** | CEO | ✅ **Decided 2026-09-16: Private Limited, Telangana.** ₹15k to incorporate, ~3 weeks; **₹30–45k/yr recurring because statutory audit is mandatory at zero revenue.** Execution now, not a decision. Action pack §1 |
| **FD-07** | **Primary device for v0** | CEO | ✅ **Closed 2026-09-16 (`GD-16`): mobile-web-first.** The phone is the constrained case, so the device answer stops being load-bearing |
| **FD-08** | **Who is DCPO, and who is Deputy?** | Both | ✅ **Decided 2026-09-16 (`GD-14`): the non-technical founder is DCPO, the technical founder Deputy.** Protects the critical path, and the DCPO already knows the school's people by name. **Both names must be published before launch** |
| **FD-09** | **Accept a 24×7 60-minute safeguarding pager?** | Both | ✅ **Accepted in principle 2026-09-16 (`GD-15`). Rota sized after `SPK-4`** — the flag-volume estimate is currently a guess (`A-019`) |
| **FD-10** | **Pilot school's board affiliation and counsellor name** | CEO | 🔲 **Open.** CBSE mandates a counsellor; state boards do not. Decides whether Tier 1 has anywhere to route |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-07 | CTO (incoming) | Register opened. 12 pending ADRs, 5 pending founder decisions. |
| 0.2.0 | 2026-09-16 | CTO (incoming) | **Last two ADRs closed.** `ADR-009` accepted (crossing is lawful), `ADR-011` accepted at v0.2.0 (reverses two clauses that had already reached the HLD/LLD), `ADR-015` added to the register. `FD-06` decided; `FD-04` reopened; `FD-08`–`FD-10` added. |
