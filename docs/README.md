---
title: True Learn AI — Documentation Index
status: living
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-07
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
---

# True Learn AI — Documentation Index

Engineering and product documentation for True Learn AI, a Socratic K-12 STEM tutoring
platform sold to schools.

**Start here:** [`00-context/00-source-of-truth.md`](00-context/00-source-of-truth.md).
It is the only authoritative statement of what this product is. The pitch deck, the
blueprint PDF, and the marketing site are *inputs*, not specifications, and they
contradict each other in nine recorded places.

---

## Reading order

| Read this | If you are |
|-----------|-----------|
| **`00-context/03-gate-decisions.md`** | **Anyone. Everyone. First.** It supersedes every earlier document where they disagree |
| `00-context/00-source-of-truth.md` | Next — the reconciled baseline and contradiction register |
| `00-context/01-claims-audit.md` | An investor, or anyone about to repeat a claim in public |
| `00-context/02-engagement-plan.md` | A founder, or a new engineer wanting to know what happens when |
| `00-context/decision-log.md` | Anyone about to make an architectural decision |

---

## Status

| Phase | Directory | Status | Gate |
|-------|-----------|--------|------|
| 0 · Context | [`00-context/`](00-context/) | ✅ Delivered — `O-01`–`O-10` all answered | Passed 2026-09-08 |
| 1 · Discovery | [`01-discovery/`](01-discovery/) | ✅ Delivered — amended for India-first | Wedge approved, non-goals 1/2/7 amended |
| 2 · PRD | [`02-prd/`](02-prd/) | ✅ Delivered — `FR-026` added after `PQ-01` | ⚠️ `NFR-011` needs rewrite — see phase 7 |
| 3 · TAR | [`03-tar/`](03-tar/) | ✅ Delivered | **Passed 2026-09-15** — all 7 subsystem calls approved |
| 4 · Design + ADRs | [`04-design/`](04-design/), [`05-adr/`](05-adr/) | ✅ Delivered — **HLD/LLD at v0.2.0**, all ADRs decided | §7 of the HLD corrected 2026-09-16 |
| 5 · Implementation | [`06-implementation/`](06-implementation/) | ✅ **Delivered** — 7 slices, 5 milestones | **Gate passed 2026-09-16** — `GD-14`–`GD-17` |
| 6 · Quality & Eval | [`07-quality/`](07-quality/) | ✅ **Delivered** — strategy + 2 harnesses measuring | Approve the release gates — [`02-test-and-eval-strategy.md`](07-quality/02-test-and-eval-strategy.md) §2 |
| 7 · Security & Compliance | [`08-security/`](08-security/) | **Pulled forward — delivered** | Closes `FD-06`, `ADR-009`, `ADR-011` |
| 8 · Ops & Cost | [`09-ops/`](09-ops/) | ✅ **Delivered** — cost model v0.3.0 + SLOs | **Approve the pricing restructure** (`GD-12`) — break-even 10 schools → 3 |
| 9 · GTM & Diligence | [`10-gtm/`](10-gtm/) | ✅ **Delivered** — diligence pack + pilot design | **Approve for external use** — `GQ-02` |

**Phase 7 was pulled forward** because three of its findings were blocking earlier phases —
and one of them (`ADR-011`) **reversed a decision already baked into the accepted design**.
Start at [`08-security/00-legal-and-safeguarding-action-pack.md`](08-security/00-legal-and-safeguarding-action-pack.md).

Parallel spikes are defined in
[`00-context/02-engagement-plan.md`](00-context/02-engagement-plan.md) §5 and do **not**
wait for their phase gates. `SPK-1` (leakage) and `PQ-01` (OCR) are measured; **`SPK-3`
(legal read) is retired** — the statute answered it; **`SPK-4` (safeguarding detector
precision) is new, and it sizes the on-call rota.**

---

## Conventions

- Every document carries front matter (`status`, `owner`, `version`, `last_updated`,
  `reviewers`) and a changelog table.
- Diagrams are Mermaid, inline. No binary image assets in `docs/`.
- Identifiers are stable and cross-referenced: `C-nnn` contradictions, `A-nnn`
  assumptions, `O-nn` open questions, `CL-nnn` claims, `FR/NFR-nnn` requirements,
  `ADR-nnn` decisions, `RISK-nnn` risks, `SLO-nnn` objectives.
- Anything time-sensitive (model names, prices, regulation, competitor features) carries a
  citation and a retrieval date, or is explicitly labelled unverified.
- One commit per phase, conventional-commit format.

---

## Repository layout

```
docs/
├── README.md                     ← you are here
├── 00-context/                   ← baseline, claims audit, plan, ADR register
├── 01-discovery/                 ← problem, personas, competition, wedge
├── 02-prd/                       ← requirements and scope ladder
├── 03-tar/                       ← options analysis and capacity planning
├── 04-design/                    ← HLD and LLD
├── 05-adr/                       ← individual architecture decision records
├── 06-implementation/            ← milestones, WBS, hiring
├── 07-quality/                   ← test strategy and eval harness
├── 08-security/                  ← threat model, child safety, compliance
├── 09-ops/                       ← SLOs, observability, cost model
└── 10-gtm/                       ← diligence pack and pilot design
inputs/                           ← source PDFs and site snapshot (EMPTY — see below)
```

> **Open provenance defect:** `inputs/` is empty. The two source PDFs and a snapshot of
> the marketing site must be committed before the Discovery gate, or nothing in this
> repository can be independently re-derived. See
> [`00-context/00-source-of-truth.md`](00-context/00-source-of-truth.md) §1.1.

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-07 | CTO (incoming) | Index created; phase 0 documents landed. |
| 0.2.0 | 2026-09-16 | CTO (incoming) | Status table brought current: phases 0–7 delivered, phase 5 gate passed. `SPK-3` retired, `SPK-4` added. Phase 7 pulled forward because it reversed part of the accepted design. |
