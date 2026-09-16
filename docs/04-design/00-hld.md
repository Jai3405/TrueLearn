---
title: High-Level Design
status: draft
owner: CTO (incoming)
version: 0.2.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 4 — Design
inputs: [03-tar/00-tar.md, 02-prd/00-prd.md, 00-context/decision-log.md, 08-security/00-legal-and-safeguarding-action-pack.md]
---

# High-Level Design

> Implements the seven subsystem calls accepted at the TAR gate (2026-09-15). Every
> component here traces to an accepted ADR; nothing new is decided in this document.

---

## 0. Scope correction (again)

The phase-4 brief asks for sequence diagrams covering **barge-in interrupt** and **teacher
escalation**, and a **canvas command schema**. All three were removed:

| Brief asked for | Substituted with | Why |
|---|---|---|
| Barge-in interrupt path | **Photo capture → transcription → confirmation** | `GD-02` — push-to-talk, no barge-in |
| Teacher escalation path | **Cohort aggregation** | `GD-07` — no per-student profile, so no per-student escalation |
| Canvas command schema v1 | *(dropped)* | PRD §2 — input is a photograph |
| — | **Safeguarding disclosure** *(added)* | `ADR-011`, a launch precondition. **Now designed — §7** |

---

## 1. Context (C4 level 1)

```mermaid
flowchart TB
    STU["Student<br/>Grade 10-12"]
    PAR["Parent<br/>consent giver"]
    TCH["Teacher<br/>optional viewer"]
    ADM["School admin<br/>roster owner"]
    SG["Safeguarding lead<br/>named human"]

    TL["True Learn AI"]

    LLM["Multimodal LLM provider<br/>outside India"]

    STU -->|"photo + voice"| TL
    PAR -->|"consent, withdrawal"| TL
    ADM -->|"CSV roster"| TL
    TL -->|"cohort friction view"| TCH
    TL -->|"disclosure flag, 15 min"| SG
    TL <-->|"transcribe + tutor"| LLM
```

**The boundary that matters:** the LLM provider is **outside India**. Student data at rest
is in India (`NFR-007`), but every turn crosses a border in flight.

**Resolved — `ADR-009` Accepted.** DPDP §16 is a blacklist with **no country notified**, and
does not commence until **13 May 2027**. The crossing is lawful; no transfer instrument is
needed. What we may *not* do is claim inference happens in India — most vendor "residency"
covers storage only. `SPK-3` is retired to a standing gazette watch.

---

## 2. Containers (C4 level 2)

```mermaid
flowchart TB
    subgraph Device["Student device — web browser"]
        UI["Session UI<br/>camera, push-to-talk, transcript"]
        SPEECH["Web Speech API<br/>STT + TTS, on-device"]
    end

    subgraph Edge["Managed PaaS — India region"]
        API["Session API<br/>stateless"]
        TUTOR["Tutor service<br/>policy + guard"]
        SAFE["Safeguarding detector"]
        AGG["Cohort aggregator<br/>scheduled"]
        ADMIN["Admin console<br/>server-rendered"]
    end

    DB[("Postgres — India<br/>RLS by school_id")]
    OBJ[("Object store — India<br/>images, 30-day TTL")]
    LLM["LLM provider"]

    UI --> API
    SPEECH -.->|"never leaves device"| UI
    API --> TUTOR --> LLM
    API --> SAFE
    API --> DB
    API --> OBJ
    AGG --> DB
    ADMIN --> DB
```

| Container | Responsibility | Why separate |
|---|---|---|
| **Session API** | Auth, session state, orchestration | Stateless, so it scales horizontally (TAR §4) |
| **Tutor service** | Socratic policy, LLM calls, **the guard** | Isolated because it is the one component whose failure is silent |
| **Safeguarding detector** | Disclosure detection, human handoff | Must run even if the tutor path fails |
| **Cohort aggregator** | Nightly roll-up, k≥5 suppression, **discards individual signal** | Separation makes "no per-student profile" auditable |
| **Admin console** | Roster, consent, usage, export/delete | Server-rendered — no SPA (TAR §6) |

**Speech never leaves the device.** Audio is transcribed locally by the Web Speech API; only
text crosses the network. That was a cost decision (`ADR-001`) that happens to be the
strongest privacy property in the system — there is no voice recording of a child to lose,
subpoena, or breach.

---

## 3. Trust boundaries

```mermaid
flowchart LR
    subgraph B1["1 — Untrusted: student device"]
        S["Student input:<br/>photo, speech, text"]
    end
    subgraph B2["2 — Semi-trusted: our application"]
        P["Policy + guard"]
    end
    subgraph B3["3 — Untrusted: model output"]
        M["LLM response"]
    end
    subgraph B4["4 — Trusted: our data"]
        D[("Postgres RLS")]
    end
    S -->|"validate, size-cap,<br/>never interpolate into policy"| P
    P -->|"prompt"| M
    M -->|"GUARD: inspect before display"| P
    P -->|"parameterised, tenant-scoped"| D
```

Four rules, each mapping to a failure mode in TAR §5:

1. **Student input is hostile.** A 15-year-old is the most motivated adversary this system
   has. Input is data, never instruction — never concatenated into the policy prompt in a
   way that lets it redefine the tutor's role. `SPK-1` showed role reassignment was the
   attack that actually worked.
2. **Model output is untrusted.** Every response passes the guard before a student sees it.
   `F1`.
3. **Tenant isolation is enforced by the database.** RLS, not a `WHERE` clause. `F6`.
4. **Empty is not safe.** A missing model response is an error with a designed fallback,
   never a blank turn. `F2`, `ADR-015`.

---

## 4. Critical path 1 — session start

```mermaid
sequenceDiagram
    participant A as Admin
    participant P as Parent
    participant S as Student
    participant API as Session API
    participant DB as Postgres

    A->>API: upload roster CSV
    API->>DB: create students (status=pending_consent)
    API->>P: consent request per student
    P->>API: grant consent
    API->>DB: record consent (who, when, scope)
    Note over API,DB: No session may start before this row exists — FR-015
    S->>API: sign in with school code
    API->>DB: check consent + baseline
    alt baseline not captured
        API->>S: baseline diagnostic (FR-017)
        S->>API: responses
        API->>DB: store baseline
    end
    API->>S: ready
```

**Consent is a hard gate, not a banner.** The session endpoint refuses to create a session
without a consent row. Under DPDP a child is anyone under 18 and consent must be verifiable
— so this is a schema-level constraint, not UI copy.

**The baseline is captured before any tutoring** (`FR-017`). Skip it and the pilot proves
nothing and cannot be renewed on evidence.

---

## 5. Critical path 2 — the tutoring turn

```mermaid
sequenceDiagram
    participant S as Student
    participant API as Session API
    participant T as Tutor service
    participant G as Guard
    participant L as LLM
    participant DB as Postgres

    S->>API: photo of working
    API->>T: image + session context
    T->>L: transcribe (ADR-016)
    L-->>T: step sequence
    T->>API: "I read this — correct?" (FR-026)
    API->>S: confirmation
    S->>API: confirm or correct
    T->>T: find FIRST divergent step (FR-003)
    T->>L: generate Socratic question
    L-->>G: candidate reply
    G->>G: leaked answer?
    alt clean
        G-->>API: deliver
    else leaked
        G->>L: regenerate with correction
        L-->>G: second attempt
        alt still leaking
            G-->>API: GUARD_FALLBACK (fail closed)
        end
    end
    API->>S: spoken + text reply
    API->>DB: turn record
```

**Three properties worth defending at review:**

- **Confirmation before reasoning.** At 87.5% transcription accuracy, roughly one line in
  eight is misread. Without `FR-026` the tutor coaches working the student never wrote,
  confidently — which destroys trust faster than saying "I can't read this".
- **First divergent step only.** A student handed six corrections closes the app. `FR-003`.
- **The guard fails closed.** If it cannot verify a reply, the student gets the fallback.
  Never ship an unverified reply — `F1` is the failure that ends the company.

---

## 6. Critical path 3 — step-down scaffolding

```mermaid
sequenceDiagram
    participant S as Student
    participant T as Tutor service

    T->>S: question at abstraction level N
    S->>T: "I don't know" / silence >20s / low confidence
    T->>T: drop to level N-1, same concept
    T->>S: concrete instance or everyday analogy
    S->>T: still stuck
    T->>T: drop to level N-2
    T->>S: simpler still
    S->>T: still stuck
    Note over T: ceiling reached — 3 step-downs
    T->>S: "let's come back to this later" + move on
```

**The ceiling is the product, not a limitation.** `00-problem-and-personas.md` §2.1 called
step-down the anti-interrogation valve: without a ceiling the tutor becomes a hostile quiz,
which is `RISK-003` — the student abandons it. Three levels, then a graceful exit.

**Measured caveat (`SPK-1`):** with an ambiguous prompt the model *deliberated itself into
silence* on this exact path, returning empty replies. A step-down that returns nothing is
worse than no step-down. `ADR-015` makes that an error with a fallback.

---

## 7. Critical path 4 — safeguarding disclosure

```mermaid
sequenceDiagram
    participant S as Student
    participant API as Session API
    participant D as Safeguarding detector
    participant DCPO as DCPO (ours, named)
    participant EXT as Police / parent / 112
    participant SCH as School counsellor
    participant AUD as Immutable audit log

    S->>API: message containing a disclosure
    API->>D: screen (runs on every turn)
    D-->>API: flagged + tier
    API->>API: leave tutoring, enter SupportMode
    API->>S: scripted non-clinical reply<br/>+ 14416 / Vandrevala / 1098
    API->>AUD: append-only record
    alt Tier 3 — abuse, or parent implicated
        API->>DCPO: 60 min, 24x7
        DCPO->>EXT: report to SJPU / police<br/>NO verification first
        Note over DCPO,EXT: parent NOT notified where implicated
    else Tier 2 — self-harm
        API->>DCPO: 60 min, 24x7
        DCPO->>EXT: parent by SMS + call<br/>112 if imminent and parent unreachable
    else Tier 1 — low concern
        API->>SCH: next business day, summary only
    end
```

**Design constraints, all non-negotiable:**

- Screening runs on **every** student turn, before tutoring logic — not as a filter on the
  reply.
- **The session does not terminate.** The tutor stops *tutoring* and does not return to it,
  but stays present with helplines on screen. It never counsels, diagnoses, or claims to be
  human (`FR-022`).
- **Classification is by what was disclosed, not by severity.** Abuse and self-harm carry
  opposite legal duties and take different paths.
- The **named human is ours** — a DCPO, personally liable under POCSO §19. The school is a
  next-business-day destination, because **no Indian school has a safeguarding human awake
  at 9pm**.
- The audit log is **append-only** and retained **180 days in India** (CERT-In).

**`ADR-011` is now Accepted** with the full tier design. It remains a launch precondition:
it must exist before one real student uses the product.

> **Corrected 2026-09-16.** This path previously halted the session terminally and alerted a
> named human *at the school* within 15 minutes (`NFR-011`). Both were wrong — a terminal
> halt punishes a child for disclosing, and the school contact does not exist out of hours.
> See [`../08-security/00-legal-and-safeguarding-action-pack.md`](../08-security/00-legal-and-safeguarding-action-pack.md) §3.

---

## 8. Data flow and residency

| Data | Where | Retention | Notes |
|---|---|---|---|
| Audio | **Device only** | Never stored | Web Speech API transcribes locally |
| Photo of working | Object store, India | **30 days** | `FR-023` deletion on consent withdrawal |
| Transcript text | Postgres, India | Term | Tenant-scoped |
| Topic friction | Postgres, India | Aggregated nightly | **k≥5; individual signal discarded** |
| Consent records | Postgres, India | Retained | Legal-basis evidence |
| Safeguarding events | Append-only log | Retained | Not deleted by consent withdrawal |
| **In flight to LLM** | **Crosses border** | Provider policy | ✅ `ADR-009` — lawful, §16 blacklist is empty |
| **ICT / audit logs** | **India** | **180 days minimum** | **CERT-In. Binds from incorporation, not 2027** |

**The cohort aggregator is the compliance boundary.** Individual session signal enters, a
section-level row leaves, and the individual signal is discarded. That keeps `GD-07` true by
construction rather than by policy — and it deserves an explicit test, not a code comment.

---

## 9. What this design deliberately does not do

| Not present | Why |
|---|---|
| Per-student cognitive profile | DPDP §9(3) — prohibited, no consent gateway (`GD-07`) |
| Teacher alert queue | `RISK-021` — teachers abandon tools that generate work |
| Real-time / WebSocket anything | Turn-based. 90 req/s at 500k students (TAR §4) |
| Caching layer, queue, microservices | TAR §6 — nothing earns its operational cost at pilot scale |
| Canvas, avatar, browser-resident model | `ADR-006` moot, `ADR-002` demo-only, `ADR-008` rejected |

---

## 10. Open, and blocking

| ID | Item | Blocks |
|---|---|---|
| ~~`ADR-009`~~ | ~~Cross-border transfer basis~~ | ✅ **Closed** — lawful, no instrument needed |
| ~~`ADR-011`~~ | ~~Safeguarding escalation design~~ | ✅ **Closed** — designed and accepted; §7 corrected |
| ~~`FD-06`~~ | ~~Legal entity~~ | ✅ **Decided** — Pvt Ltd, Telangana. Execution ~3 weeks |
| `FD-08` | **Who is DCPO, who is Deputy?** | **Launch.** POCSO liability is personal |
| `FD-09` | Accept a 24×7 60-min pager between two founders? | **Launch** |
| `SPK-4` | Safeguarding detector precision/recall | Sizing the on-call rota |
| `TQ-01` | Does the pilot school use Google Workspace? | §4 roster vs SSO |
| `PQ-03` | Is device-native TTS acceptable to a teenager? | §2 speech decision |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Initial HLD. C4 context + containers, 4 trust boundaries, 4 critical paths (barge-in and teacher-escalation substituted per §0). |
| 0.2.0 | 2026-09-16 | CTO (incoming) | **§7 corrected — the halt was wrong.** Session no longer terminates; tiers replace a single flag; the named human moves from the school to our DCPO. `ADR-009` closed (crossing is lawful). CERT-In log residency added to §8. |

## Related documents

- [`../03-tar/00-tar.md`](../03-tar/00-tar.md) — the subsystem calls this implements
- [`01-lld.md`](01-lld.md) — schema, API contracts, policy engine
- [`../00-context/decision-log.md`](../00-context/decision-log.md) — ADR register
