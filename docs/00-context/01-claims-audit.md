---
title: Claims Audit — Investor Diligence Pre-Mortem
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-07
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
classification: INTERNAL — not for external distribution
---

# Claims Audit — Investor Diligence Pre-Mortem

> **What this is.** Every factual, market and technical claim in the pitch deck (S1) and
> the live marketing site (S3), checked against primary sources, and marked. This is the
> document a diligence partner would produce about you. It is better to have it first.
>
> **What this is not.** It is not an attack on the founders' judgment. The striking
> finding is that the *research* is largely sound — the flagship RCT citation is real,
> preregistered, and quoted verbatim; the technical product names all exist. The damage
> is concentrated in a small number of rhetorical embellishments and one arithmetic
> failure, sitting next to good evidence. **That is the most dangerous configuration
> there is**, because a partner who catches one invented statistic stops believing the
> nine real ones beside it.

---

## Method and honesty notes

Verified 2026-09-07 against primary sources. Every verdict carries a URL.

| Verdict | Meaning |
|---------|---------|
| **VERIFIED** | Confirmed at a primary source. Safe to repeat as written. |
| **PARTIALLY TRUE** | The core is real; a specific number, label or attribution is wrong. |
| **MISLEADING** | Every individual word may be defensible; the impression created is not. |
| **UNVERIFIABLE** | No primary source found. Not proven false — proven unsupported. |
| **FALSE** | Contradicted by evidence. |

**Two corrections to my own earlier reasoning, recorded because they matter:**

1. I suspected the AEA registry ID was fabricated or misattributed. **It is not.** I
   fetched the registry entry directly and confirmed it. Details in `CL-010`.
2. I flagged the identical p-value (0.029) on two different estimates as statistically
   suspicious. **That was wrong, and the arithmetic disproves it** — see `CL-013`. If a
   partner raises it, you now have the answer. Do not raise it yourself as a concern.

**Provenance caveat.** The AEA registry entry (`CL-010`) I fetched and read personally.
The remaining verifications were performed by research agents against the URLs cited;
each URL is reproduced so any claim can be re-checked in under a minute. Vendor list
prices in §3 were retrieved 2026-09-07 and change frequently — re-verify before they
enter a cost model.

---

## Executive summary — the scoreboard

| Category | Claims | Verified | Partially true | Misleading | Unverifiable | False |
|----------|-------:|--------:|--------------:|-----------:|------------:|------:|
| Traction & status | 5 | 0 | 0 | **4** | 1 | 0 |
| Research & evidence | 14 | 7 | 3 | 2 | 1 | 1 |
| Technical | 11 | 5 | 3 | 3 | 0 | 0 |
| Market & financial | 10 | 1 | 3 | 3 | 2 | 1 |
| **Total** | **40** | **13** | **9** | **12** | **4** | **2** |

### The seven edits to make before the next investor conversation

Ranked by how fast a partner finds them and how much damage each does.

| # | Fix | Claim | Time to detect |
|---|-----|-------|----------------|
| 1 | Remove every "DEPLOYED / ACTIVE / CONNECTED" status and the "84% Cohort coverage" figure from the website | `CL-001`–`CL-003` | Instant — it's the page header |
| 2 | Delete "100% of top CS programs and school boards are reverting to paper exams" | `CL-021` | ~2 minutes |
| 3 | Delete "YC's #1 priority"; YC does not rank RFS entries | `CL-020` | ~30 seconds for anyone YC-adjacent |
| 4 | Rebuild the $12M SOM — it contradicts itself by ~17× before you check the market | `CL-052` | ~5 minutes with a calculator |
| 5 | Replace "98% cost advantage" with 66%, or name the model that actually costs $0.25 | `CL-053` | ~5 minutes |
| 6 | Stop calling the NBER meta-analysis "Socratic", and cite the published 0.288 SD not the preprint 0.37 SD | `CL-017` | ~3 minutes |
| 7 | Delete "10x leverage for lateral thinkers" or label it a hypothesis | `CL-022` | Instant — it has no source |

### The one finding that is not a claims problem

**`CL-035`: PenEcho is licensed AGPL-3.0-only.** This is not a wording issue. It is a
Series-A diligence blocker and an enterprise-procurement blocker, and nobody has priced
the commercial licence. See §3 and `ADR-006`.

---

## 1. Traction and status claims

**This is the section that matters most, and it is the only section where the problem is
not fixable by rewording — it requires taking things down.**

### CL-001 — "HUB71+ UAE DEPLOYED SOCRATIC ENGINE v4"

*Source: S3, persistent site header.* · **Verdict: MISLEADING**

No source establishes that any system is deployed, that any UAE school uses it, or that
Hub71 has admitted the company. S2's own deliverable checklist is entirely unchecked
(see `00-source-of-truth.md` §2.8).

Separately, Hub71 **is not a deployment venue**. It is an Abu Dhabi accelerator that
invests AED 250,000 cash via SAFE plus AED 250,000 in kind, in exchange for equity, and
provides desks and compute credits ([hub71.com/program/hub71-plus-ai](https://www.hub71.com/program/hub71-plus-ai)).
Being in Hub71 means an accelerator invested in you. It involves zero schools and zero
students. Filing it under traction describes an investment as a sale.

The live Hub71 site shows **Cohort 21 closing February 2027 and launching September
2027** ([hub71.com/faqs](https://www.hub71.com/faqs)) — so even on the optimistic path,
the Abu Dhabi presence is a 12–24 month plan, not a current state.

> **Defensible rewrite:** "Applying to Hub71's AI programme in Abu Dhabi (Cohort 21).
> Product in active development; first school pilots targeted for [date]."

---

### CL-002 — "Grade 9: Capillary action block | 84% Cohort coverage"

*Source: S3, Pillar III.* · **Verdict: MISLEADING — remove immediately**

Presented in a live-status panel as an operational metric from a running cohort. No
school, no cohort size, no denominator, no date. If this is illustrative, nothing on the
page says so.

This is the single most damaging item in the source set, because it is a *specific
quantitative claim about real children*. An investor who funds partly on the strength of
"we have cohort data" and later learns there was no cohort has a misrepresentation
grievance that survives into the subscription agreement's representations and warranties.

> **Defensible rewrite:** Either delete, or place inside a panel labelled — in text the
> reader cannot miss — **"ILLUSTRATIVE MOCK-UP — NOT REAL STUDENT DATA."**

---

### CL-003 — `AUDIO FEED: STREAMING_ACTIVE` · `CANVAS FEED: PENECHO_SYNC` · `TEACHER COHORT FEED: CONNECTED` · `GEOGRAPHIC ARBITRAGE: DEPLOYED`

*Source: S3, all four architecture pillars.* · **Verdict: MISLEADING**

Four system-status indicators for systems that do not exist. Present tense, terminal
styling, and the word DEPLOYED are all doing work here that the underlying reality does
not support.

> **Defensible rewrite:** `STATUS: IN DEVELOPMENT` · `STATUS: DESIGN TARGET` ·
> `STATUS: PLANNED — PILOT Q_ 2027`. Investors fund pre-product companies every day.
> They do not fund founders whose public claims fail a five-minute check.

---

### CL-004 — "Corporate HQ: Abu Dhabi, UAE (ADGM / Hub71+ AI)" and "R&D Center: India Operations"

*Source: S3.* · **Verdict: UNVERIFIABLE — likely aspirational**

Stated in the present tense as existing corporate infrastructure. `O-06` and `O-09` ask
whether either exists. Two facts that bear on it:

- The discounted ADGM Tech Startup Licence **requires a Hub71 approval letter** —
  applications without one have not been accepted since July 2024
  ([adgm.com/business-areas/tech-startup](https://www.adgm.com/business-areas/tech-startup)).
  The entity plan and the accelerator plan are therefore a *single* dependency, not two
  independent options.
- Realistic ADGM first-year all-in cost is **US$20,000–22,000** (licence + one investor
  visa + Al Maryah Island workspace + UAE-resident signatory), against a headline
  government fee of ~$1,000–1,500. Budget the real number.

> **Defensible rewrite:** "Intended HQ: ADGM, Abu Dhabi, contingent on Hub71 admission.
> Engineering to be based in India."

---

### CL-005 — Founder bios imply full-time commitment

*Source: S1 slide 12, S3.* · **Verdict: MISLEADING by omission**

Both bios say the founder "works at" another company, present tense; the site says the
CEO is "committing to relocation" — future tense. Neither states full-time status.
Investors assume full-time unless told otherwise, and discovering otherwise late is a
trust event. See `C-003` / `O-03`.

> **Defensible rewrite:** State it plainly, whatever the answer is. "Both founders go
> full-time on close of the round" is a perfectly fundable sentence.

---

## 2. Research and evidence claims

**Headline: the research is in better shape than the rest of the deck.** The flagship
citation is real and quoted accurately. Four claims need fixing; one is false.

### CL-010 — AEA Registry ID `AEARCTR-0016651` and its attribution

*Source: S1 slides 7, 14.* · **Verdict: VERIFIED** (title is a paraphrase)

**I fetched this registry entry personally.** [socialscienceregistry.org/trials/16651](https://www.socialscienceregistry.org/trials/16651)
returns a real, **completed** trial:

- **Registered title:** "Rapid Evaluation of the Impact of Gemini Guided Learning on
  Students' Mathematics Scores in Junior Secondary Schools in Sierra Leone"
- **PIs:** Natalia Valdes Aspillaga; María José Ogando Portela (Fab Inc); Usman Khawar (Fab Inc)
- **Design:** 48 sections (16 JSS1, 32 JSS2) across 12 schools; 24 treatment / 24 control
- **Intervention:** 6 Oct – 12 Dec 2025. Status: Completed.

The deck's "48 classrooms" and "N = 1,763" both check out — 1,763 is the report's
analysed sample (registration planned ~2,000; endline 1,637; balanced panel 1,423).

Two precision defects: the deck's title is a paraphrase of the report's actual title
(*"Teaching with Gemini: Measuring the impact of Guided Learning on student mathematics
progress in Sierra Leone"*), and the registry lists the affiliation as **Fab Inc** while
the report bylines **Fab AI**. Both organisations are real and share personnel; this is
not an error, but know the answer if asked.

> **Defensible rewrite:** "LearnLM Team, Google & Fab AI (2026). *Teaching with Gemini:
> Measuring the impact of Guided Learning on student mathematics progress in Sierra
> Leone.* Preregistered RCT, AEA RCT Registry AEARCTR-0016651. N = 1,763 students, 48
> classrooms, 12 junior secondary schools, Sierra Leone."

---

### CL-011 — "Google DeepMind & Fab AI Randomized Controlled Trial (May 2026)"

*Source: S1 slides 10, 14.* · **Verdict: VERIFIED — with one disclosure to make proactively**

The report is public: [storage.googleapis.com/deepmind-media/LearnLM/learnLM_sierraleone_may26.pdf](https://storage.googleapis.com/deepmind-media/LearnLM/learnLM_sierraleone_may26.pdf),
dated 2026-05-15, bylined "LearnLM Team, Google & Fab AI". Partners: Google DeepMind,
Fab AI ([fab-ai.org](https://www.fab-ai.org/)), EducAid (implementation), Laterite
(research), Oxford MeasurEd (blinded assessment).

**The disclosure to make yourself:** this is a **vendor-authored technical report, not
peer-reviewed**. Google is both the tool provider and a study author. Independent blinded
assessment by Oxford MeasurEd mitigates this; it does not remove it. Say so before a
partner does — volunteering a limitation buys more credibility than the citation itself.

---

### CL-012 to CL-016 — The five specific figures

*Source: S1 slides 4, 7, 10, 14.* · **Verdict: ALL FIVE VERIFIED VERBATIM**

| ID | Claim | Report text | Verdict |
|----|-------|-------------|---------|
| CL-012 | ITT +0.258 SD (p = 0.029) | "+0.258 standard deviations… 95% CI [0.027, 0.488], *p* = 0.029" | ✅ Exact |
| CL-013 | TOT ≥12h +0.380 SD (p = 0.029) | "+0.380 SD (treatment on the treated; 95% CI [0.040, 0.719], *p* = 0.029)" | ✅ Exact |
| CL-014 | "1.2 to 1.7 years of extra academic progress" | "roughly 1.2 to 1.7 years of extra learning progress" | ✅ Exact |
| CL-015 | Scaffolding 76.4% / direct solutions 2.1% | "posing scaffolding questions (76.4% of its messages)… direct solutions (2.1%)" | ✅ Exact |
| CL-016 | Direct answers 5.0% / understanding 91.4% | "seeking direct answers (5.0% of conversations by volume)… developing their understanding and skills (91.4%)" | ✅ Exact |

**On the duplicate p-value — my earlier concern was wrong.** The TOT is a Wald/IV
estimator: the ITT rescaled by the compliance rate. Both the point estimate and its
standard error scale by the same constant, so the t-statistic — and the p-value — are
unchanged *by construction*. Check it: 0.380 / 0.258 = 1.473, and the CI width ratio
0.679 / 0.461 = 1.473. Identical. This is arithmetic, not p-hacking. **Do not raise this
as a concern; do have this answer ready.**

**Four real weaknesses in these numbers, which you should know before a partner tells you:**

1. **The ITT is marginal.** 95% CI [0.027, 0.488] — the lower bound is a whisker from zero.
2. **The TOT is weaker than it looks.** "≥12 hours" is post-treatment selection; dosage
   correlates with attendance, device access and teacher engagement.
3. **"1.2–1.7 years" is a benchmark conversion**, not a measured outcome — it rests on
   Evans & Yuan's effect-size translation for low-income contexts.
4. **The intervention widened attainment gaps.** Higher-baseline students benefited more
   (+0.195 SD per baseline SD, p = 0.002). ⚠️ **If you also pitch equity or closing
   achievement gaps, your headline citation contradicts your narrative.** Decide which
   story you are telling before a partner decides for you.

**And the attribution risk that matters most:** `CL-015` and `CL-016` describe **Gemini
Guided Learning's** behaviour in a **teacher-led classroom** intervention in Sierra Leone.
They are not measurements of True Learn AI, and the study is not of an after-school 1:1
voice tutor. See `CL-023`.

> **Defensible rewrite (use the ITT only; drop the TOT — it buys nothing and invites the
> compliance question):** "In a preregistered RCT of Gemini's Guided Learning across 48
> Sierra Leonean maths classrooms (N = 1,763), AI-supported teaching raised maths
> outcomes by **+0.258 SD** (95% CI [0.027, 0.488], p = 0.029) — which the authors
> benchmark at roughly 1.2–1.7 years of additional progress in a low-income context.
> Interaction logs showed the model posed scaffolding questions in 76.4% of messages
> versus direct solutions in 2.1%. *Vendor-authored, not peer-reviewed; the confidence
> interval is wide; gains were larger for higher-baseline students.*"

---

### CL-017 — NBER WP 27476: "96 RCTs", "+0.37 SD", "+0.37 to +0.50 SD", "Socratic tutoring"

*Source: S1 slides 7, 11, 14.* · **Verdict: PARTIALLY TRUE — three separate defects**

**Right:** the paper number, authors (Nickow, Oreopoulos & Quan), title and 2020 date are
correct, and the preprint does report 0.37 SD across 96 studies
([nber.org/papers/w27476](https://www.nber.org/papers/w27476), [edworkingpapers.com/ai20-267](https://edworkingpapers.com/ai20-267)).

**Defect 1 — you are citing a superseded number.** The paper was published, *retitled*,
in the *American Educational Research Journal* (2024) as **"The Promise of Tutoring for
PreK–12 Learning"**, with a peer-reviewed pooled effect of **0.288 SD across 90 studies**
([journals.sagepub.com/doi/10.3102/00028312231208687](https://journals.sagepub.com/doi/10.3102/00028312231208687),
[eric.ed.gov/?id=EJ1406037](https://eric.ed.gov/?id=EJ1406037)). Note the authors
themselves softened the title from "Impressive Effects" to "Promise". Quoting the higher
preprint figure when a lower published one exists reads as cherry-picking even when it
isn't.

**Defect 2 — "+0.50 SD" is unsupported.** No 0.50 SD pooled figure appears in either
version. The number appears to have migrated from Cook et al. (`CL-019`), where it is a
*grades* effect from a different study with a different population. **Delete it.**

**Defect 3 — "Socratic" is FALSE.** The paper defines its subject as "one-on-one or
small-group instructional programming by teachers, paraprofessionals, volunteers, or
parents". It analyses provider type, grade, frequency and setting. It contains **no
analysis of Socratic method, guided discovery, or dialogic questioning**, and does not
treat pedagogical style as a moderator. Calling it evidence for "Socratic tutoring"
misrepresents the paper's construct — and it is the claim most load-bearing for your
positioning, which makes it the worst one to get wrong.

> **Defensible rewrite:** "Nickow, Oreopoulos & Quan (2024), *The Promise of Tutoring for
> PreK–12 Learning*, American Educational Research Journal (earlier NBER WP 27476),
> meta-analysed 90 randomised tutoring experiments and found a pooled effect of **+0.288
> SD**. *This establishes the value of high-dosage human tutoring — the cost problem we
> address. It does not evaluate Socratic method specifically.*"

---

### CL-018 — Bloom (1984), "The 2 Sigma Problem"

*Source: S1 slide 14.* · **Verdict: Citation VERIFIED. The finding is NOT REPLICATED.**

Citation is exact: Bloom, B. S. (1984), *Educational Researcher*, 13(6), 4–16
([journals.sagepub.com/doi/10.3102/0013189X013006004](https://journals.sagepub.com/doi/10.3102/0013189X013006004)).

**What a partner will hit you with.** Per von Hippel's review in *Education Next*
([educationnext.org](https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/)):
the finding rests on **two small dissertations by Bloom's own PhD students**, on 4th/5th/8th
graders, lasting **about three weeks**; one was never published. **It has never been
replicated.** It was not tutoring alone — it bundled mastery learning, extra testing and
feedback. Nickow et al.'s meta-analysis found no two-sigma effect. Modern consensus is
**about one-third of a standard deviation.**

Every serious EdTech investor has seen 2-sigma used badly, and several now treat it as a
negative signal.

> **Defensible rewrite (turns a liability into a credibility win by pre-empting the
> critique):** "Bloom's 1984 '2 sigma problem' framed our category's central question:
> individual tutoring beats classroom instruction but does not scale economically. The
> original 2 SD figure came from two small, short, largely unpublished studies and **has
> never been replicated**; modern meta-analyses put high-quality tutoring nearer **+0.3
> SD**. We build against the replicated number."

---

### CL-019 — Cook et al. (2015), "Not Too Late"

*Source: S1 slide 14.* · **Verdict: VERIFIED — your cleanest citation. Lead with it.**

Authors, year, title and both effect sizes are exact: maths test scores **+0.19 to +0.31
SD**, maths grades **+0.50 SD**, maths course failures halved; 2,718 male 9th/10th graders
across 12 Chicago public high schools, ~$3,800/participant (~$2,500 at scale)
([ipr.northwestern.edu](https://www.ipr.northwestern.edu/our-work/working-papers/2015/ipr-wp-15-01.html)).

One hygiene fix: the publisher is **Institute for Policy Research, Northwestern
University, WP-15-01** — not NBER.

This citation best supports a cost-per-student argument, which is your actual thesis.
Reserve caveat: it is in-person human tutoring with a specific male, urban, high-school
population; generalisation to AI delivery is an assumption, not a finding.

---

### CL-020 — Y Combinator RFS "The Primer" as YC's "#1 priority"

*Source: S1 slide 11.* · **Verdict: PARTIALLY TRUE — "#1 priority" is FALSE**

Verified at [ycombinator.com/rfs](https://www.ycombinator.com/rfs): "The Primer" exists,
is in the **Fall 2026** edition (the deck's "Fall '26" is right), is authored by **Andrew
Miklas**, and does open with the *Diamond Age* framing.

**The falsehood:** YC's RFS entries are **not numbered, ranked, or prioritised**. "The
Primer" appears *first in display order* among **13 entries**. Display order is not a
ranking and YC never presents it as one. "YC's #1 priority" is a fabricated hierarchy —
and it is the least necessary embellishment in the deck, because the true version does
the same rhetorical work and any YC-adjacent investor can check it in thirty seconds.

> **Defensible rewrite:** "Y Combinator's **Fall 2026 Request for Startups** opens with
> 'The Primer' — a call for production-ready adaptive AI tutoring for children, inspired
> by *The Diamond Age*. It is listed first among YC's 13 requests."

---

### CL-021 — "100% of top CS programs and school boards are reverting to paper exams due to lost trust in digital homework"

*Source: S1 slide 2.* · **Verdict: FALSE. Fix this one first.**

Three defects in one sentence: "100%" is untrue, "top CS programs" is a specificity
nobody has measured, and "school boards" imports K-12 evidence that does not exist in
the sources.

**The best available data says close to the opposite.** A freedom-of-information study
reported by *Times Higher Education* (June/Aug 2026) found **78% of UK universities were
still using online exams, 70% had no plans to phase them out, and only 3% planned to
eliminate them entirely**
([timeshighereducation.com](https://www.timeshighereducation.com/depth/are-universities-returning-person-exams-combat-ai-cheating)).

**What is genuinely true, and is a better pitch:** blue book sales up **80% at UC
Berkeley**, **~50% at University of Florida**, **30% at Texas A&M**
([insidehighered.com](https://www.insidehighered.com/news/faculty-issues/curriculum/2025/06/17/amid-ai-plagiarism-more-professors-turn-handwritten-work),
[csmonitor.com](https://www.csmonitor.com/USA/Education/2025/0523/college-ai-blue-book-finals));
named universities reintroducing invigilated exams (Bath, Birkbeck, Durham, Cardiff,
Swansea); and **59% of 337 US higher-education leaders** saying campus cheating has risen
since generative AI (Elon University/AAC&U, Dec 2024).

> **Defensible rewrite:** "Trust in unsupervised digital assessment is eroding measurably.
> 59% of 337 US higher-education leaders say cheating has risen since generative AI. Blue
> book sales are up 80% at UC Berkeley and 30% at Texas A&M, and universities including
> Bath, Durham and Cardiff are reintroducing invigilated exams. *The shift is real but
> partial — 78% of UK universities still run online exams — which is precisely why this
> is an open market rather than a closed one.*"

An unfinished transition is a market. A completed one is not. The honest version is the
stronger pitch.

---

### CL-022 — "10x Leverage for Lateral Thinkers"

*Source: S1 slide 4 (rendered as a headline stat).* · **Verdict: UNVERIFIABLE — rhetorical**

Both halves fail. The "10x" originates in **Sackman, Erikson & Grant (1968)**, a study
that was not measuring productivity differences at all — it compared online vs batch
programming, and its ratios were best-vs-worst, not best-vs-median
([construx.com](https://www.construx.com/blog/the-origins-of-10x-how-valid-is-the-underlying-research/)).
"Lateral thinking" as a construct was never empirically validated
([aeon.co](https://aeon.co/essays/lateral-thinking-is-classic-pseudoscience-derivative-and-untested)).
There is no measured population of lateral thinkers, so there is no measurable 10×.

Presented as a large numeral on a slide beside real citations, it borrows their
credibility — and forfeits it for them when checked.

> **Defensible rewrite:** Delete it, or label it: "Our design bet: tools that support
> exploratory, first-principles reasoning compound in value for the users who reason that
> way. *A product hypothesis we intend to test, not a published result.*"

---

### CL-023 — "True Learn AI implements this exact verified pedagogical architecture"

*Source: S1 slide 7 footnote.* · **Verdict: MISLEADING — the highest-leverage attribution risk in the deck**

The Sierra Leone trial evaluated **Gemini Guided Learning, teacher-led, in classrooms, on
a maths curriculum, in Sierra Leone**. True Learn AI is an **after-school, 1:1, voice-first
avatar tutor with a spatial canvas**. Those are different interventions in different
settings with different delivery models. "This exact verified architecture" claims an
equivalence the study cannot support, and it converts a legitimately strong citation into
an overreach.

> **Defensible rewrite:** "The mechanism this trial validates — scaffolding questions in
> place of direct solutions — is the mechanism our product is built around. Our own
> efficacy is unproven and will be measured in our first pilots."

That sentence is more persuasive to a sophisticated investor than the current one,
because it demonstrates you know the difference.

---

### CL-024 — "LLM 'Brain Rot': legacy AI chatbots… causing extreme cognitive decline in students"

*Source: S1 slide 2.* · **Verdict: PARTIALLY TRUE — overstated language, real underlying evidence**

There is genuine evidence, and it is better than the phrasing suggests:

- **Bastani et al., PNAS (2025)** — ~1,000 Turkish high-school maths students. Students
  given unguarded GPT-4 scored **17% worse** on a subsequent unassisted exam than students
  who never had AI. A guardrailed hint-giving "tutor" version **eliminated that penalty**
  ([pnas.org/doi/10.1073/pnas.2422633122](https://www.pnas.org/doi/10.1073/pnas.2422633122)).
  **This is the single best citation available for your thesis and it is not in the deck.**
- **MIT Media Lab, "Your Brain on ChatGPT"** — N = 54, EEG, essay writing, **not
  peer-reviewed**. The authors' term is **"cognitive debt"**, not damage or decline
  ([media.mit.edu](https://www.media.mit.edu/publications/your-brain-on-chatgpt/)).

"Extreme cognitive decline" is not what either study found. "Brain rot" reads as
unserious in an investor deck.

⚠️ **Read the Bastani result carefully before you cite it**, because it cuts both ways:
the guardrailed tutor **neutralised the harm; it did not beat the no-AI control.** You can
defensibly claim "Socratic AI beats answer-giving AI". You cannot yet claim "Socratic AI
beats no AI" — and a partner who has read the paper will know that.

> **Defensible rewrite:** "Design determines whether an AI tutor helps or harms. In a PNAS
> field experiment (~1,000 students), unguarded GPT-4 access left students **17% worse** on
> a later unassisted exam than peers with no AI at all; a guardrailed version that gave
> hints instead of answers eliminated the penalty (Bastani et al., 2025). We build for the
> guardrailed condition."

---

### CL-025 to CL-027 — Three smaller research claims

| ID | Claim | Verdict | Note |
|----|-------|---------|------|
| CL-025 | "Traditional MOOCs / Videos: +0.08 SD" *(S1 slide 7 chart)* | **UNVERIFIABLE** | No citation given anywhere. Either source it or remove the bar |
| CL-026 | "Severe teacher shortages… acute lack of STEM educators" *(S1 slide 2)* | **PARTIALLY TRUE** | Widely reported and plausible, but uncited in the deck. Add a UNESCO or regional ministry citation |
| CL-027 | "YouTube / Khan Academy: Low (<10% completion)" *(S1 slide 8)* | **MISLEADING** | The sub-10% completion statistic belongs to **MOOCs**, not Khan Academy or YouTube. Conflating them is an error a partner in EdTech will catch instantly |

---

## 3. Technical claims

**Good news: every product named in the stack actually exists.** My prior suspicion that
"Gemma 4 E2B" was a confusion with Gemma 3n was **wrong**. The problems here are prices,
one licence, and two design errors.

### CL-030 — "Gemini 3.5 Flash" at "$0.25/1M tokens"

*Source: S2 §4, table.* · **Verdict: PARTIALLY TRUE — name correct, price wrong by 6×/36×**

`gemini-3.5-flash` is real. Its list price is **$1.50 input / $9.00 output per 1M
tokens**, not $0.25 ([ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing),
retrieved 2026-09-07).

$0.25 is the input price of **Gemini 3.1 Flash-Lite** — a different, weaker model
($0.25 in / $1.50 out). **Either the model name or the price is wrong; they cannot both
be right.** This matters more than a typo, because the entire cost model rests on it.

Two traps worth knowing: **Gemini 3.8 / 3.7 / 3.6 Flash are all currently cheaper than
3.5 Flash** ($0.75/$3.75 promotional) — Google's version numbers are not a price ladder,
so "we chose 3.5 Flash for cost" has chosen the most expensive Flash model. And
**Gemini 2.5 Flash-Lite at $0.10/$0.40 is cheaper than everything in the proposed stack.**

---

### CL-031 — "DeepSeek V4"

*Source: S2 §4.* · **Verdict: VERIFIED — with a billing model nobody has accounted for**

Real, as two SKUs: `deepseek-v4-pro` (flagship) and `deepseek-v4-flash`
([api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing)).

⚠️ **DeepSeek bills peak/off-peak — costs swing 2× by time of day**, with peak windows
01:00–04:00 and 06:00–10:00 UTC weekdays. For an after-school tutoring product serving
GCC and Indian evening traffic, the peak window overlap needs modelling. Any flat-rate
cost model is wrong.

---

### CL-032 — "Gemma 4 E2B / E4B"

*Source: S2 §4, S3 hero stat.* · **Verdict: VERIFIED — and a genuine point in the deck's favour**

Gemma 4 shipped 2026-04-02 with real E2B and E4B variants, successors to Gemma 3n's,
under **Apache 2.0** — clean for commercial use
([ai.google.dev/gemma/docs/core/model_card_4](https://ai.google.dev/gemma/docs/core/model_card_4)).

One correction for internal understanding: **"E" means *effective* parameters, not
billions.** E2B is a **5.1B-parameter model** that behaves memory-wise like 2.3B. Anyone
reading "E2B" as "2 billion, so about 1 GB" is off by roughly 3×.

---

### CL-033 — "Runs in Browser via WebGL / ONNX / Transformers.js"

*Source: S2 §4.* · **Verdict: PARTIALLY TRUE — technically real, practically marginal**

ONNX builds and WebGPU demos exist
([onnx-community/gemma-4-E2B-it-ONNX](https://huggingface.co/onnx-community/gemma-4-E2B-it-ONNX)).
But the **first-load download is ~2.9–3.2 GB** for the multimodal E2B (third-party
figure; the model card states no total — treat as unverified). Throughput ~20–25 tok/s on
an M3 MacBook. **No published time-to-first-token figure exists anywhere.**

For a K-12 product on school-issued tablets and home broadband in India and the GCC, a
multi-gigabyte first-visit download is a first-session experience measured in **minutes**.
Open questions nobody has answered: what happens with no WebGPU (Safari/iOS variability),
what happens under 4 GB available VRAM, and what the real second-visit cache-hit rate is.

---

### CL-034 — "Local Gemma model → Function: Sub-second VAD"

*Source: S2 §4 architecture diagram.* · **Verdict: MISLEADING — an architectural error, not a claim error**

Voice activity detection is a signal-processing task. Purpose-built VAD models (Silero,
WebRTC VAD) are **1–2 MB** and run in **single-digit milliseconds**. Routing VAD through a
multi-gigabyte browser-resident LLM is wrong on latency, wrong on memory, and wrong on
power draw — on a tablet it is also a battery problem.

This is the clearest sign in the document set that the edge/cloud split was designed for
the pitch rather than the runtime. Fixable, and cheap to fix now. It becomes expensive
when it turns into a hiring requirement or an investor commitment. Tracked as `ADR-008`.

---

### CL-035 — "the open-source PenEcho canvas engine (20,000 × 20,000 pixels)"

*Source: S2 §2.2.* · **Verdict: VERIFIED — 🚩 but the licence is the real story**

PenEcho is real ([github.com/penecho/penecho](https://github.com/penecho/penecho),
~2.3k stars), and the **20,000 × 20,000 canvas with 512 × 512 tile allocation only where
ink exists is accurate**. The architectural claim checks out. Good.

**The problem: PenEcho is GNU AGPL-3.0-only**, with a separate commercial licence
available. AGPL §13's network-copyleft provision means that if you run a *modified*
PenEcho as a hosted service, you must offer the complete corresponding source of your
modified version to every user who interacts with it over the network. For a company whose
product *is* a hosted modified canvas, that plausibly means **publishing your
differentiating source code**.

This is routinely a Series-A diligence blocker and an outright disqualifier in enterprise
and district procurement review.

**Three questions, in order, before another line of canvas code is written:**
1. Are we modifying PenEcho or consuming it unmodified? (Unmodified hosting is far safer.)
2. What does the commercial licence cost, and is it in the cost model? (It is not.)
3. Has counsel reviewed AGPL exposure across the whole dependency tree?

**Alternatives and their licences**, for the TAR: Excalidraw (MIT) and Konva (MIT) are the
only clean picks. **tldraw is *not* open source** — it is source-available under a
proprietary licence requiring a paid commercial licence for production, with a mandatory
watermark on the free tier ([tldraw.dev/community/license](https://tldraw.dev/community/license)).
Tracked as `ADR-006`.

---

### CL-036 — "Sparse Tile Cropping… cuts input token overhead by 75%"

*Source: S1 slide 10, S2 §2.2, S3 Pillar II.* · **Verdict: MISLEADING — the mechanism described does not do what is claimed**

Four problems, of which the fourth is a conceptual error:

1. **No stated baseline.** 75% *versus what?* A native-resolution full-screen capture?
   Nobody sends those — you downscale first. Without a baseline the number is unfalsifiable.
2. **Token cost is a step function of tile count, not of pixel area.** Vision models
   tokenize images in fixed-size tiles at a fixed token cost per tile. A single
   full-canvas capture is downscaled into a bounded number of tiles. **N sparse
   512 × 512 crops each pay full tile price** — so when a student's ink is spread across
   the canvas, sparse cropping can cost the *same or more* than one downscaled capture.
   The saving is real only when ink is concentrated in one region, which is precisely the
   case where a downscaled full capture was already cheap.
3. **Input image tokens are the wrong thing to optimise.** In this product the dominant
   costs are output tokens (spoken text plus draw commands) and the audio pipeline. Even
   a genuine 75% cut to input image tokens moves a small share of the bill. See `CL-053`.
4. **WebP has nothing to do with token count.** Image format determines *bytes on the
   wire*; the model decodes to pixels before tokenizing. Choosing WebP saves bandwidth,
   not tokens. The claim as written conflates compression with tokenization.

> **Defensible rewrite:** "We send only the canvas regions containing student ink rather
> than full-canvas captures, reducing bandwidth and bounding vision-token cost per turn.
> *We will publish measured figures against a downscaled-full-capture baseline once
> instrumented.*"

Then actually measure it. If the number turns out to be real, it becomes a much stronger
claim for having a baseline attached.

---

### CL-037 — The `[DRAW: {...}]` inline regex parser as production reference code

*Source: S2 §4.2, shipped as `/lib/stream-parser.ts`.* · **Verdict: MISLEADING — will fail in production as written**

S2 presents this as implementable reference code. It is not. Seven defects, of which #2
is fatal and guaranteed:

1. **Multi-line JSON fails entirely.** `.` does not match newlines without the `s` flag.
   Any pretty-printed emission is silently dropped.
2. **🔴 Chunk-boundary loss — this will happen on every session.** The function is called
   per stream chunk with no accumulation buffer. When `[DRAW: {"type":"sc` lands at the
   end of one SSE chunk, the trailing-text branch checks `!remainingText.includes("[DRAW:")`
   and **discards it**; the next chunk begins mid-JSON, never matches, and is emitted as
   **visible transcript text — the student sees raw JSON in the subtitles.** LLM stream
   chunks do not respect token boundaries, so this is not an edge case.
3. **Legitimate text is discarded** with it, because the guard drops the whole remainder.
4. **Strings containing `}]` truncate the match early**, producing invalid JSON — entirely
   plausible in a maths tutor emitting expressions as labels.
5. **Parse failures are logged and swallowed.** The drawing silently does not happen: no
   retry, no fallback, no user-visible degradation, and no telemetry.
6. **No command IDs** → no idempotency, no ordering guarantee, no replay after a
   reconnect, no undo. A student whose network blips loses the board.
7. **Control commands share a channel with untrusted-influenced text.** Student speech and
   canvas OCR feed the model context; mixing rendering commands into that same text stream
   is a structurally unsound trust boundary.

**The fix is not a better regex.** Use structured output / tool-calling with a **versioned
schema**, framed out-of-band from the prose channel — distinct SSE event types
(`event: text` / `event: draw`) or a parallel data channel — plus monotonic command IDs, a
session command log for reconnect replay, schema validation at the boundary, and a
declared fallback render path when validation fails. Tracked as `ADR-006`; full schema
lands in the phase-4 LLD.

---

### CL-038 to CL-040 — Three remaining technical claims

| ID | Claim | Verdict | Note |
|----|-------|---------|------|
| CL-038 | "LATENCY <450ms VAD" *(S3)* | **MISLEADING** | Not a specification. Conflates ≥4 distinct measurements — see `C-006`. Real VAD detection is 10–30 ms; if 450 ms refers to that, it is a poor number presented as a headline |
| CL-039 | "Live 60fps SVG" *(S1 slide 8 competitive table)* | **UNVERIFIABLE** | A performance claim about an unbuilt product, made in a table comparing it to shipped competitors |
| CL-040 | "Zero Server Cost for UI Triggers" *(S1 slide 8)* | **MISLEADING** | A ~3 GB client model has real CDN egress cost and a real first-session UX cost. Moving compute to the client moves the cost; it does not delete it |

---

## 4. Market and financial claims

### CL-050 to CL-051 — TAM "$20B+" and SAM "$2.5B"

*Source: S1 slide 9.* · **Verdict: TAM defensible / SAM UNVERIFIABLE**

Published K-12 edtech figures range from **$32B** (The Business Research Company, 2025)
to **$187B** total edtech (Grand View) to **$404B** (HolonIQ) — a 10× spread driven by
whether hardware, connectivity and services are counted. At $20B for "K-12 digital
learning software", the deck's TAM is *below* even the narrowest published figure, so it
survives — but it is unfalsifiable, and therefore carries no information.

The $2.5B SAM has no shown derivation. A partner will ask how you got there.

**So-what:** TAM is not where this deck breaks. Don't spend meeting time defending it.

---

### CL-052 — "$12M ARR SOM — 1,000 premium K-12 private school chains in GCC, Telangana, AP & SE Asia"

*Source: S1 slide 9.* · **Verdict: FALSE — it contradicts itself before you check the market**

**Test 1 — revenue per chain.** $12,000,000 ÷ 1,000 = **$12,000 per chain per year**. At
$30/student that is **400 students per chain**; at $50, **240 students**. A GCC
international school averages ~1,010 students (1.8M students ÷ 1,783 schools, ISC
Research). So the SOM has each *multi-school chain* deploying to **a quarter of one
school**.

**Test 2 — invert it.** 1,000 chains × 5 schools × 1,000 students × $40 = **$200M ARR**,
not $12M. The model is internally inconsistent by roughly **17×**.

**Test 3 — the account universe does not exist.** ISC Research counts **616 school groups
operating 4,861 international schools worldwide**. The deck claims 1,000 premium chains in
*a subset of regions* — **62% more chains than exist globally**
([iscresearch.com](https://iscresearch.com/how-are-international-school-groups-developing/)).

Stated fairly: ISC's definition excludes large Indian domestic chains (Narayana, Sri
Chaitanya, DAV). But those are precisely the price-sensitive chains that cannot pay
$30–50/seat (`CL-055`). The chains that *can* pay the price are inside the 616; the ones
outside it can't.

> **Defensible rewrite:** Rebuild bottom-up as *named target accounts × real seat counts ×
> real price*. "We have identified 30 school groups in the UAE and Saudi Arabia
> representing ~X seats; at $40/seat, capturing 20% over three years is $Y ARR." If you
> cannot name 30 accounts, the number is decoration and a partner will treat it as such.

---

### CL-053 — "98% Cost Reduction" / "-98% Cost"

*Source: S1 slides 8, 10, S2 §4.1, S3 hero stat.* · **Verdict: FALSE as constructed — the real figure is 66%**

The comparison fails on three independent counts.

**1. The $15 baseline is a retired price.** $15/1M is the input price of **Claude Opus
4.1**, retired. Current flagship **Claude Opus 5 is $5/1M input, $25 output**
([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing),
retrieved 2026-09-07). And **no current GPT-4-family model costs $15/1M** — GPT-4o is
$2.50/$10.00, GPT-4.1 is $2.00/$8.00
([developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing)).
Lumping "Claude Opus / GPT-4" at a single $15 figure is not a real price for either.

**2. It conflates input and output pricing.** $15 is an *input* price; $0.25 is also an
*input* price. Comparing input-to-input and presenting it as total cost hides the output
side, which is **6× the quoted rate** on their own chosen model.

**3. $0.25 is not the price of the model they named.** See `CL-030`.

**The honest arithmetic** (blended at a 3:1 input:output ratio, typical for tutoring
dialogue; cached input excluded):

| Comparison | Blended /1M | Reduction |
|---|---|---|
| The deck's claim | $15.00 → $0.25 | 98% |
| **Named model vs current flagship** (Gemini 3.5 Flash $3.375 vs Opus 5 $10.00) | $10.00 → $3.38 | **66%** |
| Intended model vs current flagship (Gemini 3.1 Flash-Lite $0.5625 vs Opus 5 $10.00) | $10.00 → $0.56 | **94%** |
| Cheapest model vs retired baseline | $30.00 → $0.56 | 98% |

**98% is reachable only by comparing the cheapest available model against a retired
flagship.** The defensible number is **66%**. If you switch to Flash-Lite, 94% is real —
but then name Flash-Lite and be ready to defend its capability on Socratic dialogue with
evals.

**And the deeper problem: the cost slide optimises the wrong line item.** Verified
figures for this stack, retrieved 2026-09-07:

| Component | Cost | Source |
|---|---|---|
| Speech-to-speech LLM (Gemini 3.1 Flash Live) | **~$0.023/min** | [ai.google.dev](https://ai.google.dev/gemini-api/docs/pricing) |
| Talking-head avatar (Tavus, the only vendor publishing real rates) | **$0.26–$0.37/min** | [tavus.io/pricing](https://www.tavus.io/pricing) |
| TURN relay (Cloudflare Realtime) | $0.05/GB, 1 TB/mo free | [developers.cloudflare.com](https://developers.cloudflare.com/realtime/sfu/pricing/) |
| TURN relay (Twilio) | $0.40/GB US, $0.60–0.80/GB APAC | [twilio.com](https://www.twilio.com/en-us/stun-turn/pricing) |

**The avatar costs roughly 13× the entire voice-and-reasoning pipeline.** A cost slide
that spends its whole argument on token prices while the avatar dominates the bill is
optimising the wrong thing — and it is the strongest quantitative support for the
recommendation in `02-engagement-plan.md` §4 (`D-1`) to ship audio-first without a
photoreal avatar. Note also that Twilio TURN is 8–16× Cloudflare's price; at India/APAC
volumes that single swap saves more in absolute terms than the entire LLM debate at low
usage.

> **Defensible rewrite:** "Our inference stack costs **~66% less** than a frontier-model
> equivalent at current list prices, and our architecture avoids the per-minute avatar
> rendering costs that dominate competing voice-AI products. Full unit economics per
> student-hour in [`09-ops/`]."

---

### CL-054 to CL-058 — Pricing and channel claims

| ID | Claim | Verdict | Evidence and so-what |
|----|-------|---------|----------------------|
| **CL-054** | "75% Input Token Reduction" as a headline economic advantage | **MISLEADING** | See `CL-036`. Also note it is presented in S1 slide 8 as one of three pillars of the cost advantage, alongside two others that are also wrong (`CL-040`, `CL-053`) |
| **CL-055** | "$30–$50 / student / year" B2B | **PARTIALLY TRUE — viable in GCC, not in India** | **GCC: fine.** $14.2B GCC tuition ÷ 1.8M students = ~$7,889 average tuition; $40 is **0.51%** of that. **India: not fine.** ₹3,520 (=$40) is **11–18% of an entire annual private-school tuition** (urban ₹31,782 / rural ₹19,554), and *above* the ₹1,440–3,000/yr top-of-market enterprise band that buys a **full ERP + device bundle**. Mid-market Indian school ERP runs ₹9,000–20,000/year *for the whole school* — about **$0.75/student/year** at AP's 304-student average. The deck prices one product for two markets that differ ~10× in willingness to pay. Directly implicates `C-004` / `D-2` |
| **CL-056** | "$15–$25 / month" B2C | **MISLEADING — and probably unlawful in India** | Two problems. (a) $180–300/yr against a $30–50/yr B2B seat is a 4–10× channel arbitrage. (b) See `CL-060` — B2C makes the company a Data Fiduciary under India's DPDP Act with **no Fourth Schedule exemption**, triggering both verifiable parental consent for every under-18 **and** the absolute §9(3) bar on behavioural monitoring |
| **CL-057** | "ChatGPT / Claude — Answer Machine? **Yes** (cognitive offloading)" *(S1 slide 8)* | **MISLEADING — materially out of date** | Both products now ship explicit study/learning modes that withhold direct answers. The "blue ocean" slide rests on a competitive picture that has moved. Worse, **Khanmigo is absent from the table entirely** — see §5 |
| **CL-058** | "sold to school chains as their official 24/7 after-school AI teaching assistant" | **UNVERIFIABLE** | No school has agreed to this. Present tense describes a plan. See `O-07` |

---

### CL-060 — The Cohort Friction Map vs India's DPDP Act (a claim the deck does not make, and must)

**Verdict: the flagship B2B feature is prima facie restricted in one of the two home
jurisdictions.** Not a claims defect — a **product-legality** finding, surfaced here
because it invalidates `CL-055`/`CL-056` and belongs in front of the founders now.

India's **DPDP Rules 2025 were notified 13–14 November 2025**. Core obligations —
including children's data — **commence 13 May 2027**, roughly 20 months out
([pib.gov.in](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)).

**Section 9(3):** *"A Data Fiduciary shall not undertake tracking or behavioural
monitoring of children or targeted advertising directed at children."*
([dpdpa.com/dpdpa2023/chapter-2/section9.html](https://www.dpdpa.com/dpdpa2023/chapter-2/section9.html))

Three things make this bite:
- A **"child" is anyone under 18**, not 13.
- §9(3) is an **absolute prohibition with no consent gateway** — you cannot consent your
  way out of it.
- The Fourth Schedule exemption exists but is granted to **"educational institutions"** —
  a class an edtech *vendor* does not belong to
  ([dpdpa.com/schedule/schedule4.html](https://www.dpdpa.com/schedule/schedule4.html)).

**Consequences:** in **B2B**, the company may shelter as a *Data Processor* under the
school's exemption — but only with processing purpose-locked to that school's educational
activity: no secondary use, no cross-tenant model training on identifiable student
behaviour, no product analytics built on child profiles. That is an architectural
constraint (per-tenant partitioning of the profiling store) that must be designed in from
the start. In **B2C there is no exemption path at all.**

This is `SPK-3` in the engagement plan, and it is why that spike starts this week.

---

## 5. Material omissions

Not false claims — absences a diligence partner will notice.

| # | Omission | Why it will be asked about |
|---|----------|---------------------------|
| 1 | **Khanmigo is absent from the competitive table** | It is the direct analogue — an AI Socratic tutor from Khan Academy — at **$5–$15/student/year** ([blog.khanacademy.org](https://blog.khanacademy.org/becoming-a-khan-academy-districts-partner/)). That makes the proposed price **2–10×** the closest competitor's. Omitting the nearest competitor from a "Blue Ocean" slide is the single most conspicuous gap in the deck |
| 2 | **Google and Microsoft give AI to schools inside existing bundles** | Gemini for Education is free at the Fundamentals tier; Microsoft Copilot Chat is free with A1/A3/A5. Against a school that already licenses Workspace or M365, the incumbent price is **zero** |
| 3 | **No data-protection or child-safety position anywhere** | Selling software that records minors' voices into GCC and Indian schools without a stated privacy posture will stop procurement before price is discussed |
| 4 | **No efficacy plan for the company's own product** | Every cited study measures someone else's intervention. There is no stated plan to measure True Learn AI's |
| 5 | **No accessibility position** | A voice-first product excludes deaf/HoH students by default. WCAG 2.2 AA is a procurement requirement in international schools |
| 6 | **No competitor named from the GCC or India** | The two named target markets have local incumbents; the deck engages with none |
| 7 | **PenEcho's AGPL obligation is not disclosed** | The core canvas dependency carries a network-copyleft licence with an unpriced commercial alternative (`CL-035`) |

---

## 6. What survives, and what to say instead

The deck's honest version is a good deck. This is the claim set I would take to a partner:

| Keep | Fix | Delete |
|------|-----|--------|
| The Sierra Leone RCT ITT (+0.258 SD) with limitations volunteered | "98% cost advantage" → **66%**, and lead with avatar-cost avoidance | "100% of top CS programs…" |
| Cook et al. (+0.19–0.31 SD tests, +0.50 SD grades, ~$2,500/student) | NBER → **0.288 SD, 90 studies**, drop "Socratic" | "YC's #1 priority" |
| Bastani et al. PNAS 2025 (**add this — it is your best citation and it is missing**) | Bloom → cite as framing, pre-empt the replication critique | "10x leverage for lateral thinkers" |
| Zero-direct-answers positioning and Step-Down scaffolding | SOM → rebuild bottom-up from named accounts | All four site status indicators |
| GCC market sizing (1,783 schools, 1.8M students, $14.2B tuition) | Price → separate GCC and India tiers | "84% Cohort coverage" |
| Apache-2.0 Gemma 4 edge model as a real cost lever | "$30–50 ACV" → "per student per year" | "Live 60fps SVG" |

**The honest deck is stronger than the current one.** It says: a real preregistered trial
validates our mechanism; a PNAS field experiment shows unguarded AI actively harms
learning while guardrailed AI does not; human tutoring works at +0.288 SD but costs
$2,500 per student; the GCC has 1.8M international-school students paying $7,900 average
tuition; and we are building the guardrailed version at 0.5% of tuition. Every sentence
there survives diligence.

---

## 7. Sources

**Research:** [AEA Registry trial 16651](https://www.socialscienceregistry.org/trials/16651) ·
[LearnLM Sierra Leone report](https://storage.googleapis.com/deepmind-media/LearnLM/learnLM_sierraleone_may26.pdf) ·
[NBER WP 27476](https://www.nber.org/papers/w27476) ·
[AERJ 2024 published version](https://journals.sagepub.com/doi/10.3102/00028312231208687) ·
[Bloom 1984](https://journals.sagepub.com/doi/10.3102/0013189X013006004) ·
[von Hippel, 2-sigma critique](https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/) ·
[Cook et al. 2015](https://www.ipr.northwestern.edu/our-work/working-papers/2015/ipr-wp-15-01.html) ·
[Bastani et al., PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2422633122) ·
[MIT "Your Brain on ChatGPT"](https://www.media.mit.edu/publications/your-brain-on-chatgpt/) ·
[YC RFS](https://www.ycombinator.com/rfs) ·
[THE, online exams](https://www.timeshighereducation.com/depth/are-universities-returning-person-exams-combat-ai-cheating) ·
[Inside Higher Ed, blue books](https://www.insidehighered.com/news/faculty-issues/curriculum/2025/06/17/amid-ai-plagiarism-more-professors-turn-handwritten-work) ·
[Construx, origins of 10x](https://www.construx.com/blog/the-origins-of-10x-how-valid-is-the-underlying-research/)

**Technical:** [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) ·
[Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4) ·
[DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing) ·
[Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing) ·
[OpenAI pricing](https://developers.openai.com/api/docs/pricing) ·
[PenEcho](https://github.com/penecho/penecho) ·
[tldraw licence](https://tldraw.dev/community/license) ·
[Tavus pricing](https://www.tavus.io/pricing) ·
[Cloudflare Realtime pricing](https://developers.cloudflare.com/realtime/sfu/pricing/) ·
[Twilio TURN pricing](https://www.twilio.com/en-us/stun-turn/pricing) ·
[LiveKit pricing](https://livekit.com/pricing)

**Market & regulatory:** [ISC Research, school groups](https://iscresearch.com/how-are-international-school-groups-developing/) ·
[ISC Research, 2025 market](https://iscresearch.com/the-international-schools-market-in-2025/) ·
[DPDP Rules 2025 (PIB)](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf) ·
[DPDP §9](https://www.dpdpa.com/dpdpa2023/chapter-2/section9.html) ·
[DPDP Fourth Schedule](https://www.dpdpa.com/schedule/schedule4.html) ·
[ADGM DPR 2021](https://assets.adgm.com/download/assets/ADGM+Data+Protection+Regulations+2021+Updated.pdf/146aa34858b011efb99a36e29b0f3a63) ·
[ADGM Tech Startup Licence](https://www.adgm.com/business-areas/tech-startup) ·
[Hub71+ AI](https://www.hub71.com/program/hub71-plus-ai) ·
[Khan Academy districts pricing](https://blog.khanacademy.org/becoming-a-khan-academy-districts-partner/) ·
[KHDA](https://web.khda.gov.ae/)

**Unverifiable at primary source** (flagged so nobody treats them as settled): Gemma 4 E2B
browser download size and time-to-first-token; tldraw commercial pricing; HeyGen
Interactive Avatar per-minute rate; Simli pricing (page 404s); Cartesia pricing; PlayHT
first-party pricing (possibly defunct post-Meta acquisition); UAE PDPL Executive
Regulations status; Telangana private-unaided school count; any ADEK/KHDA vendor-approval
process.

---

## 8. Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-07 | CTO (incoming) | Initial audit. 40 claims: 13 verified, 9 partially true, 12 misleading, 4 unverifiable, 2 false. |

---

## Related documents

- [`00-source-of-truth.md`](00-source-of-truth.md) — reconciled baseline and contradictions
- [`02-engagement-plan.md`](02-engagement-plan.md) — phases, gates, and `SPK-3`
- [`decision-log.md`](decision-log.md) — `ADR-006` (canvas protocol + licence), `ADR-008` (edge model)
