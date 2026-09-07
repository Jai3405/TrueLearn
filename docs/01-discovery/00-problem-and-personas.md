---
title: Problem Statement and Jobs-to-be-Done
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-08
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 1 — Discovery
---

# Problem Statement and Jobs-to-be-Done

> Evidence in this document was verified in phase 0 and carries `CL-nnn` references into
> [`../00-context/01-claims-audit.md`](../00-context/01-claims-audit.md). Nothing here
> rests on a claim that failed that audit.

---

## 0. Assumptions this phase runs on

The phase-0 gate closed without answers to `O-01`–`O-10`. Discovery proceeds under these
stated assumptions rather than stalling. Each is cheap to correct; none is silent.

| ID | Assumption | If wrong |
|----|-----------|----------|
| **A-013** | GCC/MENA international schools are the primary market; India is R&D only | Re-price everything, re-do the compliance workstream, change the curriculum target (`CL-055`, `D-2`) |
| **A-014** | No signed school LOI or MoU exists today | Discovery is customer *research*, not validation; the pilot design in phase 9 changes shape |
| **A-015** | Neither founder writes production code for this system | Determines the first hire and the 90-day scope |
| **A-016** | The company is pre-revenue, pre-entity, and not yet in Hub71 | Runway and the UAE timeline (`CL-004`) |

---

## 1. The problem, stated honestly

### 1.1 What is actually established by evidence

**High-dosage human tutoring works, and it is not cheap.** Across 90 randomised
experiments, tutoring produces a pooled **+0.288 SD** (Nickow, Oreopoulos & Quan, *AERJ*
2024 — `CL-017`). The Chicago Saga trial found **+0.19 to +0.31 SD** on maths tests and
**+0.50 SD** on maths grades, halving course failures — at roughly **$2,500–$3,800 per
student per year** (Cook et al. 2015 — `CL-019`).

That cost is the entire problem. It is Bloom's "2 sigma problem" restated at the effect
size that actually replicates: we have known for forty years how to teach children well,
and we cannot afford to do it for all of them.

**The substitute students actually reach for makes things worse.** This is the most
important finding available and it is not in the current deck. In a PNAS field experiment
with ~1,000 high-school maths students, those given an unguarded GPT-4 interface scored
**17% worse on a subsequent unassisted exam than students who had no AI at all**. A
guardrailed version giving hints instead of answers **eliminated that penalty** (Bastani
et al., PNAS 2025 — `CL-024`).

Read that carefully, because it defines both the opportunity and its ceiling: **guardrails
demonstrably prevent harm. They are not yet demonstrated to beat no-AI.** Any positioning
that claims otherwise is ahead of the evidence.

**Scaffolding-first AI does produce gains in the right setting.** A preregistered RCT of
Gemini Guided Learning across 48 Sierra Leonean maths classrooms (N = 1,763) found
**+0.258 SD** (95% CI [0.027, 0.488], p = 0.029), with the model posing scaffolding
questions in 76.4% of messages against direct solutions in 2.1% (`CL-010`–`CL-016`). Two
honest caveats: it was **teacher-led and in-classroom**, not after-school and 1:1, and
gains were **larger for higher-baseline students** — it widened the gap rather than
closing it.

### 1.2 The reframe that matters

The naive problem statement — *"students lack access to good tutoring"* — is wrong, and
building against it produces a product nobody needs. Students have unlimited access to AI
tutoring right now, free, on the phone in their pocket.

The real problem is a **selection** problem, not an access one:

> Between the end of the school day and bedtime, a student faces a homework task and
> chooses between a tool that ends the task in nine seconds and a tool that ends it in
> twenty-five minutes with understanding. They choose the nine seconds, every time,
> because that is what the task rewards. The school cannot see the choice, cannot
> influence it, and finds out months later in an exam hall.

Three consequences follow, and they are the actual product requirements:

1. **The harm is invisible until it is expensive.** Teachers discover the gap at
   assessment, when remediation costs the most. There is real signal here: 59% of 337 US
   higher-education leaders report cheating has risen since generative AI, and blue-book
   sales are up 80% at UC Berkeley and 30% at Texas A&M (`CL-021`). Note the honest
   version — 78% of UK universities still run online exams. This is a transition in
   progress, which is what makes it a market.
2. **Banning does not work and schools know it.** The device is in the home, the account
   is personal, and the homework channel is unobservable by design.
3. **Therefore the school's job is not "provide a tutor."** It is *"give me observability
   and influence over the four hours I don't control, without adding work for my
   teachers."* That is a fundamentally different product, and it is the one the buyer
   pays for.

### 1.3 The tension at the centre of this company

State it plainly, because every design decision downstream is shaped by it:

> **The product's core promise is directly opposed to its primary user's primary job.**

The student's job at 9pm is *finish this and stop*. The product's promise is *I will not
let you finish quickly*. Nobody voluntarily chooses the slower path at 9pm on a Tuesday
when a free alternative finishes the task instantly.

This is survivable, but only if it is designed for rather than wished away. Three
possible resolutions, and the company must pick one consciously:

| Resolution | Mechanism | Risk |
|-----------|-----------|------|
| **Mandate** — the school requires it | B2B contract, teacher assigns through it | Engagement is coerced. Retention and "velocity of mastery" metrics measure compliance, not value. Renewal depends on teacher perception, not student love |
| **Make the slow path faster** | For *some* tasks — a concept you're stuck on, exam revision — guided beats solved on wall-clock time to actually being done | Narrow. Requires knowing which tasks, which is a Discovery question we have not answered |
| **Make the slow path more pleasant** | Voice + canvas is genuinely lower-friction than typing maths into a text box | Real, but a thin moat — see [`02-differentiation-and-moat.md`](02-differentiation-and-moat.md) |

**The deck implicitly chooses mandate, and never says so.** That choice makes the teacher
and the head of school the real users, the student a captive one, and every engagement
metric suspect. It needs to be a stated decision, not an accident.

---

## 2. Jobs-to-be-Done

Four personas as briefed, plus one the brief omits that actually signs the contract.

### 2.1 The student — Layla, 14, Grade 9, Dubai international school

Captive user. Owns adoption in practice: a tool teenagers refuse to open does not survive
renewal regardless of what the contract says.

**Functional job:** *When I'm stuck on physics homework at 9pm and my parents are asleep, I
want to get unstuck without waiting until tomorrow, so I can finish and go to bed.*

**Emotional job:** *When I don't understand something everyone else seems to get, I want to
ask a stupid question without anyone knowing I asked it.* This is the strongest genuine
pull in the entire product and it is underexploited in all three source documents. A
private, patient, unjudging thing to ask is worth more to a 14-year-old than any
pedagogical mechanism.

**Social job:** *I want to not look lazy or stupid — to my teacher, my parents, or my
friends.*

**What she hires today:** Photomath/Gauth-class solvers (instant, free); ChatGPT (instant,
free, more flexible); a group chat with friends who have finished; YouTube; occasionally a
paid human tutor if the family can afford one.

**She fires our product when:** it is slower than the alternative *and* the extra time
doesn't visibly pay off; it makes her feel interrogated when she is already stuck and
tired; it takes more than a few seconds to start; it gets her in trouble; it doesn't work
on her actual device or her actual home wifi.

> **Design consequences.** The `Step-Down` mechanism is not a nice-to-have — it is the
> anti-interrogation safety valve, and it is the difference between "patient tutor" and
> "hostile quiz". Time-to-first-useful-response is an adoption metric, not a performance
> metric. And a "stuck" student is an emotional state before it is a cognitive one; the
> product must recognise frustration, not just incorrectness.

---

### 2.2 The teacher — Mr. Haddad, Grade 9 physics, 5 sections, ~140 students

**Not** the buyer, but holds a veto and drives renewal. Chronically short of time.

**Functional job:** *When I plan Monday's lesson, I want to know which specific concepts my
class actually failed on over the weekend, so I can reteach the right thing instead of
guessing.*

**Second functional job:** *When a student is quietly falling behind, I want to find out in
week 2, not at the end of term.*

**Emotional job:** *I want to feel like a better teacher, not a monitored one.* An
analytics dashboard that reads as surveillance of his class's failures — or of his
teaching — gets ignored, and he tells the head of school it isn't useful.

**Social job:** *I don't want to be the teacher who let AI cheat happen on his watch.*

**What he hires today:** marking; a show of hands; the class WhatsApp group; his own
memory; the LMS gradebook.

**He fires our product when:** it generates more than a couple of items a week that need
his attention; it tells him things he already knows; it is a separate login from the
system he already lives in; it produces an escalation he cannot act on in under five
minutes; it is ever wrong about a student in a way a parent then quotes back at him.

> **Design consequences, and these are hard constraints.** The escalation threshold is a
> *teacher-attention budget*, not a statistical threshold — S2's "3–4 consecutive Socratic
> failures" is a model-side trigger with no reference to how many alerts a human can
> absorb. Budget it explicitly: **≤3 escalations per teacher per week**, each resolvable
> in **≤5 minutes**, each stating a specific concept and a specific suggested action.
> Precision matters more than recall — a false escalation costs more trust than a missed
> one. And every escalation must be defensible to a parent, because eventually one will be.
>
> **Amended 2026-09-08 after the regional evidence scan — this is stronger than a budget.**
> Between **27% and 67%** of school software licences are never meaningfully used; a
> typical educator already touches **50 distinct tools a year** from a district catalogue
> of ~3,000; **70%** of teachers had no input into the tools they are handed; and LMS
> platforms have measurably left teachers *more* burnt out, not less. A teacher-facing
> alerting queue is the single most reliable way for this product to die quietly between
> purchase and renewal.
>
> **The rule is therefore: teacher-optional by construction.** Value must reach the
> student and the parent with **zero teacher action on the critical path**. Teachers get a
> *mirroring* view they may open, never an *alerting* queue they must clear. Note the
> tension this creates with the deck, which makes the teacher dashboard the core B2B
> value: the dashboard is what gets **sold**, but it must never be what makes the product
> **work**. See `RISK-021`.

---

### 2.3 The school IT / admin — Ms. Fernandes, IT Manager, 3-school group, ~2,400 students

Gatekeeper. Cannot say yes on her own; can absolutely say no, and her no is final.

**Functional job:** *When a new tool is proposed, I want to onboard 2,400 accounts without
manual work and offboard them in June, so I don't spend my summer on spreadsheets.*

**Risk job:** *When I approve a tool that records children's voices, I want to be able to
show the board exactly where that data lives and who can see it, so it is not my job on
the line.*

**Emotional job:** *I want fewer systems, not more.*

**What she hires today:** Google Workspace for Education or Microsoft 365 — both of which
now include AI at no incremental cost (claims audit §5, omission #2); the existing LMS; a
vendor security questionnaire.

**She fires our product when:** there is no SSO; rostering is manual; there is no DPA, no
data-residency answer, no subprocessor list; it needs a browser extension or an install
she has to push to managed devices; it breaks on the school's actual locked-down
Chromebooks or managed iPads; students can sign up with personal accounts.

> **Design consequences.** SSO and rostering (LTI 1.3 / OneRoster / Google Workspace /
> Entra) are **pilot-blocking, not v2**. A DPIA, a subprocessor list and a data-residency
> statement are sales collateral that engineering must produce. And `A-002` — which
> devices, which browsers — is unanswered and gates whether a ~3 GB browser-resident model
> (`CL-033`) is viable at all.

---

### 2.4 The parent — Mr. and Mrs. Rao, two children, paying ~$8,000/year in fees each

Not the payer in B2B, but the consent-giver, the complaint channel, and the reason the
head of school cares.

**Functional job:** *When my child struggles, I want them to get help I cannot give them
myself, so their grades don't slip.*

**Financial job:** *When I am already paying $8,000 in fees, I want the school to solve
this rather than me paying a private tutor on top.* This is the single strongest
willingness-to-pay argument the company has, and it argues for B2B: the parent has
*already* decided to pay, and a $40 seat inside fees is 0.5% of tuition (`CL-055`).

**Anxiety job:** *I want to know my child isn't just outsourcing their brain to a machine,
and I want to know what the machine is recording.*

**What they hire today:** private tutors (the direct substitute, and expensive); after-school
centres; the parent's own evening; resignation.

**They fire our product when:** the child is upset by it; they discover voice recordings
they didn't know about; the school raises fees to pay for it; the child's grades don't
move.

> **Design consequences.** Parental consent is a legal requirement, not a courtesy — and
> under India's DPDP Act it is verifiable consent for **anyone under 18** (`CL-060`).
> There must also be a parent-facing story, even in B2B, because parents will ask what is
> being recorded. Answering that well is a sales asset.

---

### 2.5 The persona the brief omits — the economic buyer

**Dr. Suleiman, Head of School / Director of Curriculum, or the group's academic director.**
IT is the gatekeeper; *this* person signs.

**Functional job:** *When I set next year's academic priorities, I want a measurable
improvement in Grade 9–11 STEM outcomes without hiring three more STEM teachers I cannot
find, so I can defend the results to my board and my parents.*

**Competitive job:** *I want to be able to say we do something the school down the road
does not.* In the GCC international-school market, where 1,783 schools compete for
1.8M students on reputation and results, differentiation is a purchasing motive in its
own right.

**Risk job:** *I do not want to be in a newspaper story about AI and children.*

**They fire our product when:** it cannot show an outcome by the end of the pilot year; a
teacher tells them it created work; a parent complains; the renewal price rises.

> **Design consequence, and it sets the phase-9 pilot design.** The buyer needs *evidence*
> at renewal. Instrumentation for a defensible outcome measurement is not a phase-9
> afterthought — the baseline must be captured before the first session, or the pilot
> proves nothing and the second year does not happen.

---

## 3. What the personas jointly demand

Ranked by how many personas block on each. Anything blocking two or more is not v2 work.

| Requirement | Blocks | Phase |
|-------------|--------|-------|
| SSO + automated rostering | IT (hard veto), teacher, buyer | v0 — pilot-blocking |
| Data residency, DPA, subprocessor list, DPIA | IT, parent, buyer | v0 — pilot-blocking |
| Teacher-attention budget: ≤3 actionable escalations/week | Teacher, buyer | v0 |
| Fast, low-friction start on the school's real devices | Student, IT | v0 |
| Step-Down as an anti-interrogation valve | Student, parent | v0 — this is the retention mechanism |
| Baseline capture for outcome measurement | Buyer | v0 — must precede first session |
| Safeguarding / disclosure escalation path | Parent, buyer, teacher | v0 — launch precondition |
| Accessibility (WCAG 2.2 AA; deaf/HoH in a voice-first product) | IT, buyer, parent | v0 — procurement blocker |
| Parent-facing transparency view | Parent | v1 |
| Cohort friction analytics beyond individual escalation | Buyer | v1 — and see `CL-060` |

**The uncomfortable read:** almost nothing on the v0 list is the thing the deck is excited
about. The avatar, the 20,000 × 20,000 canvas, the browser-resident model and the
sub-second barge-in appear nowhere in what any persona blocks on. That does not make them
worthless — it makes them *not the wedge*. See
[`04-wedge-and-non-goals.md`](04-wedge-and-non-goals.md).

---

## 4. Open questions this phase could not answer

Answering these requires talking to actual humans, which no amount of desk research
substitutes for.

| ID | Question | Who to ask | Blocks |
|----|----------|-----------|--------|
| DQ-01 | Which homework tasks would a student genuinely rather do guided than solved? | 10 students, Grade 9–11 | The wedge; whether resolution (2) in §1.3 exists at all |
| DQ-02 | How many alerts per week will a teacher tolerate before ignoring all of them? | 5 teachers | Escalation threshold design |
| DQ-03 | What killed the last edtech tool this school bought? | 3 heads of school, 3 IT managers | The whole risk register |
| DQ-04 | Would a school mandate after-school use, or only recommend it? | 3 heads of school | `§1.3` — whether the mandate resolution is even available |
| DQ-05 | What does the school already pay per student for software, in total? | 3 IT/finance | Whether $30–50 fits an existing budget line or needs a new one |

**Recommendation:** ten student conversations and five teacher conversations, before the
PRD gate. The CEO's family-business relationships with school chains are the company's
only distribution asset — this is what they are for, and using them for research now costs
nothing and de-risks everything downstream.

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-08 | CTO (incoming) | Initial problem statement and 5 personas. Assumptions A-013–A-016 recorded. |

## Related documents

- [`../00-context/00-source-of-truth.md`](../00-context/00-source-of-truth.md) — baseline, `A-nnn` register
- [`../00-context/01-claims-audit.md`](../00-context/01-claims-audit.md) — evidence behind every citation here
- [`01-competitive-teardown.md`](01-competitive-teardown.md)
- [`04-wedge-and-non-goals.md`](04-wedge-and-non-goals.md)
