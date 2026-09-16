---
title: Legal, Compliance and Safeguarding — Action Pack
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-16
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 7 — Security, Privacy & Compliance (pulled forward)
inputs: [00-context/03-gate-decisions.md, 04-design/00-hld.md, 05-adr/ADR-009, 05-adr/ADR-011]
---

# Legal, Compliance and Safeguarding — Action Pack

> Closes the three long-pole non-technical items: **`FD-06`** (entity), **`ADR-009`**
> (cross-border inference), **`ADR-011`** (safeguarding escalation). All three were
> blocking either a school contract or launch.
>
> **This is not legal advice.** §7 lists the four questions that genuinely need an Indian
> lawyer, and what they cost.

---

## 0. The headline, for someone with four minutes

| Item | Was | Now | What it costs |
|---|---|---|---|
| **`FD-06` entity** | Open, blocking every contract | **Private Limited, Telangana** | ₹15k once, **₹30–45k/yr forever** |
| **`ADR-009` cross-border** | Treated as a blocker | **Not a blocker.** Lawful today and as drafted | ₹0 |
| **`ADR-011` safeguarding** | Proposed, no design | **Designed, accepted, and it changes the product** | A 24×7 pager between two founders |

**Three things changed my mind while researching this:**

1. **The border was never the problem.** DPDP §16 is a *blacklist* and nothing is on it. I
   had `ADR-009` marked "blocks any real student data". It doesn't.
2. **The safeguarding design in the accepted HLD is wrong** — not incomplete, *wrong*. It
   halts the session on a distress disclosure. No major provider does that, and the reason
   is that halting abandons a child alone at 9pm. See §3.2.
3. **POCSO §19 binds a *person*, not a company or a school.** It cannot be contracted to
   the school, and a Supreme Court judgment from **July 2026** closes the "we checked
   first" defence. This converts safeguarding from a product-design question into a
   criminal-liability one.

---

## 1. `FD-06` — Entity

### The call: Private Limited Company, registered in Telangana

Not an LLP, not an OPC. Three reasons, in order of how much they'd hurt:

1. **An LLP cannot issue shares or convertible notes.** The convertible note is the standard
   first-cheque instrument in India. An LLP forecloses your first raise.
2. **DPIIT startup recognition requires a Pvt Ltd** (or LLP), and DPIIT recognition is a
   prerequisite for the angel-tax exemption that makes those notes workable. It is **free
   and takes ~72 hours** once incorporated — do it immediately after.
3. **An OPC allows exactly one member.** There are two of you.

A school also cannot meaningfully contract with an individual, and — the part that should
actually move you — **processing minors' data without a corporate Data Fiduciary puts DPDP
liability on the two of you personally.** The §9 penalty ceiling is **₹200 crore**. That is
the sentence to reread.

### Cost and timeline

| Item | Cost | Notes |
|---|---|---|
| DSC (2 directors) | ₹2,000–3,000 | |
| Name reservation (SPICe+ Part A) | ₹1,000 | |
| SPICe+ filing, PAN, TAN, EPFO, ESIC | ₹0–2,000 | Government fee nil below ₹15 lakh authorised capital |
| **Telangana stamp duty** | **₹500 MOA + 0.15% AOA (min ₹1,000) + ₹20** | ⚠️ **`A-016` UNVERIFIED** — MCA fee page returned 403. Confirm with the CA before filing |
| Professional / CA fees | ₹6,000–15,000 | The real variable |
| **Total to incorporate** | **₹10,000–22,000 — budget ₹15,000** | ~**3 calendar weeks** |

### The number founders get wrong

**Annual compliance is ₹30,000–45,000 per year at zero revenue.**

Because **statutory audit under s.139 of the Companies Act is mandatory for a Private
Limited regardless of turnover.** There is no small-company exemption, no "we made nothing
this year" exemption. Add AOC-4, MGT-7A, DIR-3 KYC, and an auditor's fee.

The ₹2,999 incorporation packages advertised online exclude every one of these. Budget the
recurring number before you incorporate, not after.

### Also binding from day one — and not in any other document

**CERT-In Directions (April 2022), under the IT Act** — these bind from incorporation, are
**not** deferred to 2027, and are not contingent on DPDP:

- **Report a cyber incident within 6 hours** of noticing it.
- **Retain ICT logs for 180 days, stored within India.**
- Synchronise to NIC/NPL NTP.

`NFR-007` already puts data in India. **Logs were not covered by it.** That is now a design
constraint, not a policy — see §4.

### Do this week

1. Get DSCs for both founders (1 day, online).
2. Reserve the name via SPICe+ Part A.
3. Engage a Hyderabad CA — ask for the **all-in first-year number including audit**, not the
   incorporation quote. If they won't quote the recurring figure, that answers something.
4. Immediately post-incorporation: **DPIIT recognition** (free, ~72h), then current account.

---

## 2. `ADR-009` — Cross-border inference. I was wrong about this one.

### DPDP §16 is a blacklist, and it is empty

Verbatim: *"The Central Government may, by notification, restrict the transfer of personal
data by a Data Fiduciary for processing to such country or territory outside India as may
be so notified."*

Restriction requires a **notification naming a country**. **No country has been notified as
of September 2026.** The default is permission, not prohibition — the inverse of GDPR.

Further: **§16 and Rule 15 do not commence until 13 May 2027.** And Rule 15 turns out to be
narrower than the press coverage implied — it concerns making personal data available to a
**foreign State**, not Indian government access.

**Conclusion: sending student text to a US LLM API is lawful today and remains lawful after
May 2027 as currently drafted.** `ADR-009` is accepted on that basis, with a standing
review trigger (§8).

### But there is a real architectural difference worth knowing

Residency claims are not equivalent, and the difference is exactly the one a school will
ask about:

| Provider | Storage in India | **Inference in India** |
|---|---|---|
| OpenAI (India data residency) | ✅ Yes | ❌ **No — processing stays in the US** |
| Google Vertex AI `asia-south1` | ✅ Yes | ✅ **Yes — ML processing commits to region** |

"Data residency" from most vendors means *storage*. If you ever need to say "this child's
words were never processed outside India" — and a school's legal review may well ask —
**only a regional Vertex endpoint lets you say it.**

This does not change the v0 provider choice (`ADR-007` keeps the abstraction). It changes
what you are allowed to claim, and it is the reason the abstraction exists.

### Where the actual exposure is

**Not the border. §9 children's data — ceiling ₹200 crore.**

`GD-07` already avoids the worst of it: cohort-only aggregates, no per-student profile, so
the §9(3) behavioural-monitoring prohibition is avoided *by construction*. That decision is
now doing more work than it was credited with.

The **Data Protection Board was established 13 November 2025 but remains entirely
unstaffed** — no Chairperson, no Members as of August 2026 (`A-017`). Enforcement risk is
low *today*. Do not build on that; it is a staffing gap, not a legal position, and it can
close in a single gazette notification.

---

## 3. `ADR-011` — Safeguarding. This is the section that changes the product.

### 3.1 The legal ground, plainly

**Sexual abuse disclosure → a criminal reporting duty that binds a person.**

POCSO §19(1) binds *"any person"* with knowledge. Not schools. Not institutions. Persons.
§21(1): failure is **up to six months' imprisonment, fine, or both.**

**[AAA v. Linda Sema, 2026 LiveLaw (SC) 659, decided 9 July 2026](https://www.livelaw.in/supreme-court/supreme-court-revives-pocso-case-against-school-headmistress-for-not-reporting-child-sex-abuse-says-doing-own-verification-no-excuse-540636)** settles two points that land directly on our architecture:

1. **"Knowledge" = awareness from receipt of credible information.** A child telling an
   authority figure is enough.
2. **You may not verify first.** A private inquiry before reporting is **not a defence.**

And the Court imposed §21 liability **only on the individual who received the information
directly.** Liability attaches to *the human who reads the transcript.*

Three consequences we cannot design around:

- **You cannot contract this to the school.** An MSA clause saying the school handles
  reporting does not protect the employee who read it. Every commercial instinct will want
  that clause. It does not work.
- **Routing to the school does not discharge the duty** — and looks uncomfortably like the
  "private verification" the Court just held impermissible.
- **Good-faith immunity exists** (§19(7)). Over-reporting is free. Under-reporting is a
  crime. The asymmetry is total, and it should drive every threshold we set.

**Self-harm / suicidal ideation → no mandatory report to anyone.**

Attempted suicide is decriminalised — Mental Healthcare Act 2017 §115. No Indian statute
imposes a duty to warn on a non-clinician. This is a **duty of care**, not a compliance
obligation.

**That makes it more dangerous, not less. There is no safe harbour to hide in.**

**`JJ Act §32 does not apply to us.`** It concerns taking physical *custody* of an
abandoned or lost child. A remote software product never does. I had this listed as a
possible basis; it isn't one. Don't build on it.

### 3.2 The design error in the accepted HLD

`HLD §7` and `LLD §3` make `HaltedSafeguarding` a **terminal state** — the tutor stops dead.
I wrote that, and it is wrong.

**No major provider halts on a distress disclosure.** OpenAI, Meta and Khan Academy all
stay engaged, de-escalate, and surface resources. Character.AI is the counter-example, and
what it actually did was *remove the product for minors entirely* after a wrongful-death
suit — it did not hard-stop sessions.

The reason is not product-metrics softness. **A 16-year-old who says something frightening
at 9pm and watches the application close on them has been punished for disclosing, and
learns not to do it again.** We would have built something worse than silence: a system that
teaches concealment.

**Corrected:** the session does not terminate. The tutor stops *tutoring* — it does not
return to algebra, does not counsel, does not diagnose — and stays present with a scripted
non-clinical response and live helplines on screen. See `ADR-011` for the state change.

### 3.3 The other design error: there is no named human at the school

`ADR-011` as proposed required notification to *"a named human at the school within 15
minutes"* (`NFR-011`). Research says that person does not exist:

- **There is no out-of-hours safeguarding practice in Indian schools.** The regulators'
  answer to the 9pm problem is *publish a helpline number*, not *staff a rota*. Supreme
  Court guidance in *Sukdeb Saha* requires helpline numbers displayed prominently — not
  night cover.
- **CBSE's own national counselling line is 09:30–17:30, Mon–Fri, five months a year.** If
  the national board can't staff nights, a single school in Khammam cannot.
- **Schools explicitly disclaim it** — published policies state responsibility "ceases
  immediately after school hours".
- **Many of our target schools have no counsellor at all.** CBSE mandated a Counselling &
  Wellness Teacher (1:500) from **19 Jan 2026** — but **many Telangana/AP private schools are
  affiliated to the state boards, not CBSE**, so the mandate doesn't reach them (`A-018`,
  unverified share — confirm per school at onboarding).
- Telangana's own Child Protection Officer order (May 2026) covers **government** high
  schools only. Not our customers.

**`NFR-011` as written is unachievable.** Corrected in `ADR-011`: the named human is
**inside our company**, the school is a **next-business-day** handoff.

### 3.4 What we build

Full design in [`../05-adr/ADR-011-safeguarding-escalation.md`](../05-adr/ADR-011-safeguarding-escalation.md). The shape:

**Classify by *what was disclosed*, not by a severity score** — because abuse and self-harm
have completely different legal characters and must go down different pipes.

| Tier | Trigger | Response | Human SLA |
|---|---|---|---|
| **0** | Any distress signal | In-session, automatic, always. Helplines on screen. Session continues | None — no human latency |
| **1** | Low concern (exam stress, bullying, no imminent risk) | Queue for review | 1 business day |
| **2** | Self-harm / suicidal ideation | Parent notified by SMS+call, scripted. School counsellor next day. **112 if imminent and parent unreachable** | **60 min, 24×7** |
| **3** | **Sexual abuse, or parent/guardian implicated** | **DCPO reports to SJPU/police. No verification. No calling the school or parent first** | **60 min, 24×7** |
| **4** | Credible threat to others | DCPO → police | 60 min, 24×7 |

**The rule that must never be violated:** never route a disclosure of abuse-at-home to the
person at home. This is not my invention — the NIPCCD POCSO handbook already encodes it
("*unless a teacher or staff member is suspicious that a parent/guardian/caregiver is
abusing the child*"). It becomes a hard branch in code, not a guideline.

### 3.5 The cost nobody wants to hear: a 24×7 pager between two founders

Tier 2/3 needs 60-minute human review, 24 hours a day. There are two of you and no budget.

**At pilot scale this is feasible. It has a hard cliff.** The driver is not disclosure
prevalence — it's **detector false-positive rate**:

Assume (`A-019`, must be measured, not guessed) a **1% per-session flag rate**, 200 students,
3 sessions/week:

| Schools | Students | Flags/week | Verdict |
|---|---|---|---|
| 1 (pilot) | 200 | **~6** | Two founders can carry this |
| 3 | 600 | ~18 | Painful but survivable |
| **5** | **1,000** | **~30 (4+/day, incl. nights)** | **Breaks** |
| 10 | 2,000 | ~60 | Needs paid staff |

**So: the on-call rota is viable to roughly 3 schools and must be funded by school #5.**
That is a hiring trigger with a number on it, and it belongs in the cost model — it is a
real per-school cost that [`../09-ops/00-cost-model.md`](../09-ops/00-cost-model.md)
currently does not carry.

**The lever that moves the cliff is detector precision.** Halving the false-positive rate
doubles the school count you can serve with the same two people. That makes detector
precision a *commercial* metric, not just a quality one — and it is the strongest argument
for the eval harness earning its keep here as much as on leakage.

Cheaper alternative considered and **rejected**: restrict product availability to hours we
can cover. It kills the product — evening and weekend home study *is* the use case
(`GD-02`, the whole wedge). Not viable.

### 3.6 Helplines — verified, and two you must not ship

Surface these three, in Telugu and English, on every Tier 0+ trigger:

| # | Service | Number | Hours | Why |
|---|---|---|---|---|
| 1 | **Tele-MANAS** | **14416** | **24×7** | Government (MoHFW), Telugu, free, TG + AP cells live |
| 2 | **Vandrevala Foundation** | **9999 666 555** | **24×7×365** | Telugu, **and WhatsApp** |
| 3 | **Childline** | **1098** (with **112**) | **24×7** | Child-protection emergencies |

**Emergency: 112** — imminent threat to life where a parent is unreachable.

**The WhatsApp property on Vandrevala is the single most important cell in this table.** A
teenager in a shared family room at 9pm cannot make a voice call. If the home is the source
of harm, a phone number they must speak into is not a resource — it is a trap. Ship the
WhatsApp path first-class, not as a footnote.

**Daytime only, label the hours:** Roshni Trust Hyderabad — 8142020033 / 8142020044,
Mon–Sat 10:00–19:00, Telugu. Never the primary evening option.

**Do not ship:**
- **iCALL (9152987821)** — closes 21:00 and **has no Telugu**. Wrong on both axes for this cohort.
- **KIRAN (1800-599-0019)** — **`A-020` UNVERIFIED**, reported merged into Tele-MANAS. No
  2025–26 government source confirms it runs independently.

**Ring-test every number before launch and re-test quarterly.** Two of seven had conflicting
numbers across current sources. A dead helpline in a crisis screen is worse than no helpline.

### 3.7 We would be first, and that is worth money

**No Indian edtech has published a real safeguarding policy.** Vedantu's child-safety page is
the only Indian example found — it has a hotline and a 7-day resolution SLA, but **no
reference to POCSO, no mandatory-reporting procedure, and no self-harm or abuse disclosure
path at all.** Nothing found from PhysicsWallah or BYJU'S.

Publishing a real one is a **procurement differentiator** — and under *Sukdeb Saha*
Guideline V, arguably required anyway. It is also, bluntly, the reason no Indian precedent
will protect us in court: we'd be the first to be tested.

---

## 4. What this changes in already-accepted documents

| Document | Change | Severity |
|---|---|---|
| `04-design/00-hld.md` §7 | Halt is **not** terminal; school is not the 15-min recipient | **Corrects an accepted design** |
| `04-design/01-lld.md` §3 | `HaltedSafeguarding` → `SupportMode`, not a terminal state | Schema + state machine |
| `02-prd/00-prd.md` `NFR-011` | 15-min-to-school is unachievable → 60-min-to-DCPO, 24×7 | Requirement rewrite |
| `09-ops/00-cost-model.md` | Add safeguarding on-call as a per-school cost; hiring trigger at school #5 | Unit economics |
| `04-design/01-lld.md` §1 | Logs retained 180 days **in India** (CERT-In) | New constraint |
| Every doc citing `ADR-009` as blocking | It no longer blocks | Unblocks work |

---

## 5. New assumptions

| ID | Assumption | Confidence | How to kill it |
|---|---|---|---|
| `A-016` | Telangana stamp duty ₹500 MOA + 0.15% AOA + ₹20 | **Low** — MCA page 403'd | CA confirms at filing |
| `A-017` | DPB unstaffed → low near-term enforcement | Medium | Gazette watch; do not rely |
| `A-018` | A material share of TG/AP target schools are state-board, not CBSE, so have no mandated counsellor | Medium | Ask each school at onboarding |
| `A-019` | Detector fires on ~1% of sessions | **Unmeasured — a guess** | Measure in `SPK-4`. Drives the hiring cliff |
| `A-020` | KIRAN helpline is merged into Tele-MANAS | Low | Ring it |
| `A-021` | *Sukdeb Saha* binds us as an "educational institution" | Low — untested | Lawyer Q3. **Assume yes and comply; it's cheap** |

---

## 6. Do this, in this order

**This week, no lawyer needed:**
1. DSCs + name reservation. Engage a Hyderabad CA; demand the **recurring** number.
2. **Ring-test all five helplines.** One hour of work, and it gates launch.
3. Ask the pilot school, in writing: **board affiliation, and the name/email/phone of their
   counsellor or safeguarding lead.** If the answer is "we don't have one", that is a finding,
   not a dead end — it changes who Tier 1 routes to.
4. Name the **DCPO and Deputy** between the two of you. Publish both. This is `FD-08`.

**Before one real student:**
5. Implement Tier 0 + the abuse/self-harm split (slice 4, phase 5).
6. Immutable audit log, 180-day retention, stored in India.
7. Published safeguarding policy page, Telugu + English.

**Before school #5:** fund the on-call rota.

---

## 7. The four questions that need an Indian lawyer

Roughly **₹40,000–80,000** for a written opinion from a Hyderabad firm with a tech/data
practice. `FD-04` declined external counsel on zero budget. **I am formally reopening it for
Q1 and Q2**, because both carry criminal or ₹200-crore exposure and neither is resolvable by
reading the statute.

**Q1. Does a machine flag that no human reads constitute "knowledge" under POCSO §19?**
*This question determines the architecture.* If an unreviewed queue fixes the company with
knowledge, then our review SLA is not an ops target — **it is criminal exposure**, and "we
had no 24×7 rota" becomes an admission. *Linda Sema* concerned a human headmistress; **no
Indian authority addresses machine-mediated knowledge.** Sub-question: does passing a
disclosure to the school's counsellor discharge our §19 duty? *My reading is no* — which is
why the DCPO reports directly. Confirm it.

**Q2. Under DPDP: who is the Data Fiduciary for transcripts, does the "educational
institution" carve-out reach an AI tutor, and can we lawfully withhold a transcript from a
parent we suspect of abusing the child?**
The Fourth Schedule exempts educational institutions from verifiable parental consent and
the behavioural-monitoring ban — but commentators agree *"the boundary of 'education' is not
crisply defined"*. **Whether it covers us decides if you need DigiLocker-grade verifiable
parental consent for every student** — a material product surface. And **the entire Tier 3
design depends on being able to say no to a parent**; the NIPCCD carve-out permitting that is
*guidance, not statute*. Full compliance bites 13 May 2027 — there is time, and no excuse.

**Q3. Do the *Sukdeb Saha* guidelines bind a vendor as an "educational institution", and
where does liability sit if we detect at 9pm and the school does nothing by Monday?**
The judgment binds *"all educational institutions … training centers, coaching institutes"*
— an **Andhra Pradesh** case, our market, decided under Article 21. NCPCR says digital-space
safety is *the school's* responsibility (JJ Act §75) — but we are the party that saw it first
and had the means to act.

**Q4. Can a school-vendor agreement validly allocate the POCSO §19 duty to the school?**
*My reading is that it cannot* — the duty is personal and statutory. Confirm **before the MSA
template goes out**, because every commercial instinct in the building will be to write that
clause.

**Two things to track, not pay for:**
- Whether the **National School Mental Health Policy** has actually published (draft reviewed
  6 June 2026). It is the instrument most likely to define a referral pathway we can integrate.
- Whether **Telangana** has notified coaching-centre rules equivalent to AP's GO 9 (27.03.2026).
  None found. *Sukdeb Saha* required all States to notify within two months of 25 July 2025 —
  so either Telangana is non-compliant or it isn't indexed anywhere reachable.

---

## 8. Review triggers

Re-open `ADR-009` immediately if any of these fire:

- **Any country is notified under DPDP §16** (gazette watch).
- **13 May 2027** — §16 and Rule 15 commence. Re-read both against the then-current text.
- A **Significant Data Fiduciary** designation lands on us (Rule 13 brings localisation
  obligations that §16 does not).
- The Data Protection Board is **staffed** and begins issuing orders.

---

## Assumptions

Carried in §5 above (`A-016`–`A-021`), and inheriting `A-000`–`A-012` from
[`../00-context/00-source-of-truth.md`](../00-context/00-source-of-truth.md).

All legal findings in this document were retrieved **September 2026** against primary
sources where reachable. Items marked UNVERIFIED are where a primary source was not
reachable; none of them are load-bearing for the decisions taken.

## Open Questions for Founders

| ID | Question | Why it matters |
|----|----------|----------------|
| `FD-04` **reopened** | Will you fund ₹40–80k for a written opinion on Q1 and Q2? | Q1 is criminal exposure; Q2 is ₹200 crore |
| `FD-08` | **Which of you is DCPO, and which is Deputy?** | POCSO liability attaches to a named individual. It cannot be "the company" |
| `FD-09` | Do you accept a 24×7 60-minute pager between the two of you until school #5? | It is the only way to launch without funding |
| `FD-10` | Does the pilot school have a counsellor, and what board is it affiliated to? | Decides whether Tier 1 has anywhere to go |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-16 | CTO (incoming) | Closes `FD-06`, `ADR-009`, `ADR-011`. Corrects two errors in the accepted HLD (terminal halt; school as 15-min recipient). Adds CERT-In obligations, absent from all prior documents. |

## Related documents

- [`../05-adr/ADR-009-cross-border-inference.md`](../05-adr/ADR-009-cross-border-inference.md)
- [`../05-adr/ADR-011-safeguarding-escalation.md`](../05-adr/ADR-011-safeguarding-escalation.md)
- [`../00-context/decision-log.md`](../00-context/decision-log.md)
- [`../04-design/00-hld.md`](../04-design/00-hld.md) — §7 corrected by this document
