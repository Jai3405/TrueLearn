---
title: Competitive Teardown
status: draft
owner: CTO (incoming)
version: 0.1.0
last_updated: 2026-09-08
reviewers: [Aakash Dyavanapally (CEO), Pranav Chaitanya Varma (COO)]
phase: 1 — Discovery
---

# Competitive Teardown

All retrievals dated **2026-09-08**. Figures marked *unverified* could not be confirmed at
a primary source and must not enter a deck or a cost model.

---

## 0. The headline, before the detail

Two things happened in the last six months that the founder materials do not account for:

1. **On 2026-08-27, Khanmigo shipped interactive diagrams** — model-generated visuals the
   student can manipulate, built with Google.org fellows on Gemini
   ([blog.khanacademy.org](https://blog.khanacademy.org/new-ai-tools-bring-interactive-diagrams-and-targeted-practice-thanks-to-khan-academys-partnership-with-google-org/)).
   All four frontier labs shipped a visual explanation surface during 2026. **A synchronised
   visual surface is now table stakes, not a differentiator.**
2. **On 2026-08-10 Gemini in Google Classroom expanded to students of all ages**
   ([workspaceupdates.googleblog.com](https://workspaceupdates.googleblog.com/2026/08/gemini-in-google-classroom-is-expanding-to-users-of-all-ages-with-contextualized-Gemini-starter-prompts-for-students.html)),
   and **on 2026-08-18 OpenAI launched ChatGPT for Teens** with age prediction and a Study
   Mode that reactivates on a schedule and re-engages a teen it detects skipping an
   assignment ([TNW](https://thenextweb.com/news/chatgpt-for-teens-openai-age-prediction-study-mode)).
   Enforced scaffolding is moving from a toggle to a policy, at consumer scale, without
   any school buying anything.

The competitive risk to this company is **not a funded startup. It is a free feature.**

---

## 1. Khanmigo — the benchmark every school committee uses

**What it does well.** Multi-subject tutoring K-12→college; free teacher tools in 180+
countries funded by Microsoft; Writing Coach with genuine process analytics (time
writing, revision data, originality flags); district dashboards, SSO, automated rostering.
**Voice: yes** — TTS plus push-to-talk STT via a microphone button. **No full-duplex, no
barge-in.** **Canvas: yes since 2026-08-27** — model-generated manipulable diagrams (drag a
line segment, the tutor reacts). The student cannot draw on it.

**Pricing.** Consumer $4/month or $44/year ([khanmigo.ai/pricing](https://www.khanmigo.ai/pricing)).
District figures of $10–15/student/year circulate; Palm Beach County reportedly ~$11.49
and Newark ~$35 — *all unverified against a primary rate card*.

**Installed base.** 600+ partner districts, 56M learners platform-wide; Khanmigo
specifically ~795 districts / ~770k US students at end of 2024-25.

**Structural weakness — and this is the most useful finding in the whole scan.**

- **Only ~15% of eligible students actively engage with Khanmigo** despite deployment
  ([The Learning Standard, 2026-04-21](https://thelearningstandard.org/news/khan-academy-revamps-ai-tutor-after-low-student-usage)).
  A district can buy it and get near-zero usage. **Engagement, not access, is the
  bottleneck in this category** — which validates §1.3 of the problem statement and is the
  single largest opening for anything with better pull.
- **Paid student access is US-only.** For GCC international schools, Khanmigo-for-students
  is not currently purchasable. That is a real distribution opening — and it is one they
  can close with a contract, not a rebuild.
- They are a non-profit running on compute philanthropy from two rival hyperscalers.
  That funds features but caps latency ambition: at $4/month consumer and ~$10–15/student
  district, nobody is donating a persistent low-latency full-duplex audio session per
  student-hour.

**Obvious next feature:** realtime conversational voice on top of the diagram surface —
"talk to Khanmigo while the graph moves." Both halves already ship separately and the
Gemini relationship makes Live API access cheap.

**Does our wedge survive it?** *Partially.* It would erase voice and visual as
differentiators entirely. What survives is a **student-drawable** surface the tutor reads,
enforced withholding, and the GCC distribution gap. Assume 6–18 months.

---

## 2. Google — the one that can zero out the price point

**What it does well.** Guided Learning shipped in the Gemini app 2025-08-06 with
multimodal responses — images, diagrams, videos, interactive quizzes. Teacher-led Guided
Learning announced at ISTE 2026-06-25, giving teachers a curriculum-informed space plus
"visibility and insights into how students are interacting with the material at an
individual and class level", with a Classroom app in Gemini, an MCP server for Classroom,
and expansion to Canvas, Schoology and Moodle
([blog.google](https://blog.google/products-and-platforms/products/education/iste-2026-educator-updates/)).
Gemini Live provides full-duplex conversational voice at the app layer.

**Pricing — the headline.** **Gemini for Education is included in Education Fundamentals,
free for qualifying institutions**
([edu.google.com](https://edu.google.com/workspace-for-education/editions/compare-editions/)).
Whatever we charge, we charge against zero, in a market where Chromebooks and Classroom
are the substrate in most GCC international schools.

**Structural weakness.** Google will not build a specialist. Guided Learning is a *mode*
of a general assistant that also writes emails — the same account, one toggle away, does
the homework. It explicitly does **not** withhold answers; Google's own language is
"breaks down problems step-by-step". Every education feature must be defensible across
180 countries and every privacy regime simultaneously, which makes them slow on anything
opinionated. And they cannot charge for pedagogy — it is a Workspace retention feature.

**Obvious next feature:** Guided Learning inside Gemini Live, wired to Classroom rosters,
with the teacher insight dashboard they already ship. Every component exists today; it is
an integration, not R&D.

**Does our wedge survive it?** *This is the single most dangerous roadmap item in the
report.* It would erase voice, visual, and teacher analytics at once, at zero cost to the
school. What survives: enforced withholding (Google structurally won't), a student-drawable
surface, curriculum depth for a specific board, and compliance work a hyperscaler does
generically. **Your buyer's IT director will ask "why is this not just Gemini?" in the
first meeting. You need an answer that survives them getting voice for free next quarter.**

---

## 3. OpenAI — highest variance

**What it does well.** Study Mode (July 2025) across Free/Plus/Pro/Team/Edu. Interactive
visualizations since 2026-03-11, now **300+ math and science topics** in ChatGPT for Teens.
Full voice mode. **ChatGPT for Teachers**: 100+ K-12 organizations, 30 states, 300,000+
educators, free extended to **June 2028**, 16-state National Data Privacy Agreement.

**ChatGPT for Teens (2026-08-18) is the development that matters.** Under-18s
auto-enrolled via age prediction; **Study Mode auto-activates at parent/teen-set times and
the system re-engages a teen it detects skipping an assignment**; parental alerts, quiet
hours, and explicit anti-parasocial guardrails.

**Structural weakness.** The K-12 land grab is **teacher-side only — no student accounts**.
That means no roster, no assignment context, no per-student learning record, and therefore
**no teacher learning-analytics product is possible** without a student SKU they have not
built. Study Mode is weakly enforced and trivially bypassed — resisting its questions gets
it to do the work anyway.

**Obvious next feature:** a rostered student SKU under district admin, Study Mode enforced
by policy, teacher progress view. They have the districts, the privacy paperwork, the age
gate and the visuals. The only thing holding it back is under-18 liability — and in August
they built exactly the safety apparatus that removes that objection.

**Does our wedge survive it?** *Three of four differentiators evaporate simultaneously the
day it ships.* Survives: student-drawable canvas, GCC-specific curriculum and compliance.

---

## 4. Anthropic — least dangerous to this specific wedge

Learning mode is Socratic but is a **user-toggleable writing style, off by default**, in a
product students are not supposed to be in. Claude for Teachers is US K-12 **educators and
staff only, explicitly not students**, free through 2026-06-30, with standards mapping
across all 50 states and adoption tracking. **The paid district SKU does not yet exist.**
No voice in the education offering. Inline charts and diagrams since March 2026.

**Structural weakness.** No under-18 consumer product and no K-12 student account by
policy. Enterprise coding revenue is orders of magnitude larger than this category, so
education will not get a dedicated realtime voice pipeline.

**Does our wedge survive?** Yes. Their next feature (paid district SKU + admin-enforced
learning mode) erases "enforced withholding" for US districts only, and touches neither
voice, canvas, nor GCC.

---

## 5. Synthesis Tutor

**Ages 5–11, K-5 math only.** Voice-guided; conversational voice input is probable but
*unverified from primary source*. Interactive manipulatives, not a drawable canvas. No
explicit answer-withholding policy. Consumer pricing: $45/mo, $300/yr, $999 lifetime
individual; family $119/yr for up to seven children
([synthesis.com/tutor](https://www.synthesis.com/tutor)). **68,202 students** self-reported.
Schools: contact sales, no named customers.

**Structural weakness.** A consumer subscription business with a school page bolted on,
hard-capped at K-5, one subject, one language. $119/year for seven children is
homeschool-parent pricing that anchors them below any per-seat school economics. 68k
students after several years means no school distribution motor at all. **They cannot
follow a child into Grade 6** — which is exactly where our market starts.

**Does our wedge survive?** Yes, entirely. Different age band, different buyer. Watch them
for voice-UX craft, not for the deal.

---

## 6. MagicSchool AI — the likely channel partner, and a warning

**6M+ educators, 10,000+ schools, 160 countries**; Atlanta, Denver, Seattle, Buffalo,
Hillsborough County named. $45M Series B led by Valor Equity Partners (Feb 2025), ~$63–65M
total. 80+ teacher generators; MagicStudent delivers 50+ student tools through
teacher-created "Rooms". **No voice. No canvas.** Plus tier $99.96/year *per teacher*;
enterprise custom with SSO, Clever/ClassLink/Canvas/Schoology integration and adoption
dashboards ([magicschool.ai/pricing](https://www.magicschool.ai/pricing)).

> ⚠️ **The warning, and it bears directly on the avatar decision.** MagicSchool reportedly
> **retired its "Raina" persona from the student-facing chatbot in February 2026**,
> replacing it with a neutral "AI Learning Assistant", citing parasocial-attachment risk
> for younger students. *Unverified against MagicSchool's own communications* — but if
> true, it is an incumbent with 10,000 schools **deliberately de-anthropomorphising** its
> student tutor. A warm, named, human-faced 3D persona that children confide in nightly is
> a thing the market is currently retreating from, not advancing toward. Feed this into
> `ADR-002`.

**Structural weakness.** A teacher-productivity company that grew bottom-up on free seats;
the student product is a permissioned wrapper on the same generators. The moat is teacher
habit, not learning outcomes, and 80+ tools makes deep per-subject pedagogy impossible.

**Does our wedge survive?** Yes on voice and canvas; their obvious next feature (a real
student tutor inside Rooms reporting to the teacher dashboard) erases teacher analytics
only. **Most likely channel partner in this list — and the most likely reason a school
asks "why do we need two vendors."**

---

## 7. The solver class — Photomath, Gauth, Question.AI, Answer.AI

**Photomath** (Google-owned): free tier includes machine-generated solution steps; Plus
adds animated step tutorials and hints, $9.99/mo or $69.99/yr, 100M+ downloads.
**Gauth** (ByteDance): 50M+ Play installs, Plus at $99.99/yr.

**Have they added answer-withholding? Essentially no** — they added *step-by-step
exposition*, not withholding. Photomath Plus's "hints when you're stuck" is the closest,
and it is a paid upsell on a product whose entire value proposition is the answer.

**Structural weakness, and it is the best news in this report.** **Their business model
*is* the answer.** Conversion to paid is driven by "unlimited questions" and "faster
answers". A solver that withholds answers churns its own subscribers. They cannot ship
enforced Socratic mode as a default without destroying the funnel. They also have zero
school channel — no rostering, no DPA, no teacher dashboard, no procurement motion. In a
GCC international school, the solver is the **contraband, not the vendor**.

**Does our wedge survive?** Yes — but note the real risk is **substitution, not
competition**: the student has Gauth on their phone while our tutor refuses to answer.
That must be designed for, and abandonment signals are a product feature, not a metric.

> Worth noting for the pricing conversation: Photomath at $69.99/year and Gauth at
> $99.99/year both cost a *parent* more per year than the proposed $30–50 B2B seat.
> Willingness to pay for homework help exists. It is just currently being paid to the
> wrong product, by the wrong payer.

---

## 8. Voice-native tutors already in schools

**This category is no longer empty**, which contradicts the deck's blue-ocean framing.

| Product | Voice | Subject | Channel | Scale |
|---|---|---|---|---|
| **Amira Learning** (HMH) | Listens to students **read aloud**, real-time correction | Reading, PreK-8 | **B2B districts** | **1,800–4,000+ districts** (sources conflict); state-funded in North Dakota to June 2027; ~$9/student bundle reported |
| **Third Space Learning "Skye"** | **Spoken AI maths tutor** | Maths, UK/US | **B2B schools** | £4.4M raised April 2026; **Gates-funded 2-year research partnership with Stanford and Cornell** |
| **Speak** | Speech-to-speech, real-time feedback | Language | Consumer only | **$78M Series C at $1B valuation** (Dec 2024, Accel) |
| **Ello** | AI reading coach | Early reading | B2C + ~30 school pilots | $15.1M raised |
| **Evelyn Learning** | **Voice + real-time whiteboard, Socratic** | Physics first | B2C + B2B white-label | No pricing, no customers disclosed |

**Third Space Learning is the closest structural analogue with real school distribution** —
and the Gates/Stanford/Cornell evidence programme is precisely the credential GCC
international-school procurement weights. Neither they nor Amira do STEM problem-solving
with a canvas, but they own the "voice tutor schools have already bought" position.

---

## 9. AI tutoring + canvas — who already has it

| Who | What | Shipped | Student can draw? |
|---|---|---|---|
| ChatGPT | Interactive visualizations, 70+ → 300+ topics | 2026-03-11 | No |
| Claude | Inline charts/diagrams, editable in conversation (beta) | March 2026 | No |
| Khanmigo | Gemini-generated manipulable diagrams | **2026-08-27** | No |
| Gemini Guided Learning | Images, diagrams, videos, interactive quizzes | 2025-08-06 | No |

**The specialist that matters — SolversBoard.** Founded 2026, launched ~June 2026,
Norfolk VA. **Students handwrite their working on a canvas; the tutor reads it
line-by-line, confirms correct steps, pinpoints errors, and gives hints and worked
examples "without ever handing you the answer."** Maths, physics, chemistry, biology,
economics; 60+ exam boards including IB, A-Level, AP, SAT. **Teacher dashboard with
attempts, accuracy and streaks. Canvas LTI. School pilots running. No voice.**
**Price: free — schools bring their own AI provider key and pay inference directly**
([solversboard.com](https://solversboard.com/)).

> **Read that carefully.** A three-month-old company is executing our pedagogy, on our
> canvas, with our teacher dashboard, at a price of zero, with an LTI integration. It will
> not out-execute us — BYO-API-key is a non-starter for a school buying a product that
> processes children's data, and they have no compliance story, no voice, and no funding.
> But **it proves the idea is not scarce**, and it is the thing a procurement officer will
> email us about.

**Not competitors, worth knowing:** Desmos (embedded in the Digital SAT since 2024,
enormous math-classroom mindshare, no AI tutor); GeoGebra (100M+ claimed users, free,
photo-based Math Solver, no conversational tutor); **Mathpix — a supplier, not a
competitor**, and notably now offering EU-resident deployment of its OCR API, which
matters for data residency; Wolfram (adult/technical).

---

## 10. Regional — GCC and India

Detail in the regional scan; the competitively decisive points:

- **Alef Education** (ADX-listed, ~AED 769m revenue, ~75% EBITDA, ADEK mandate to **2033**,
  ~2m learners) has an **AI Tutor built with the UAE Ministry of Education but no voice
  product found**. Growth is flat (+0.6–1.2%), which is the profile of a company needing
  attach revenue. **124,500 students** actively engaged in UAE private schools as of June
  2026; Alef + Microsoft trained ~25,000 educators across 710 UAE schools in mid-2026.
  Channel partner first, structural threat second.
- **Classera** (12m+ learners, 40+ countries, PIF/Sanabil-backed) signed a national-scale
  AI-in-education agreement with **Zain KSA** in May 2026. Saudi is politically mediated —
  right second market, wrong first one.
- **GEMS Education** — 90+ schools, 200,000 students, 15,000 teachers — is running a
  **Global Education AI Hub publicly soliciting edtech startups** with AI roadmaps. At
  $30–50/seat that one network is a $6–10M ARR ceiling, roughly the entire claimed SOM.
- **India is harder than it looks.** **Physics Wallah's AI Guru already accepts speech
  input** at 2.82M queries/month, from a listed company; **Extramarks** sells an AI suite
  into the same buyer; and the large chains build in-house (Sri Chaitanya → Infinity Learn,
  $50M; Orchids → K12 Techno/Eduvate). The most attractive Indian accounts become
  competitors, not customers.

---

## 11. Comparison

| Product | Voice | Visual surface | Student can draw | Withholds answers | Teacher analytics | School $/student/yr | Reach |
|---|---|---|---|---|---|---|---|
| **Khanmigo** | Push-to-talk, no barge-in | **Yes** (Aug 2026) | No | Prompt-level, unenforced | **Yes** | ~$10–15 *(unverified)* | 795 districts, 770k students; **~15% engage**; **students US-only** |
| **Google Gemini / Classroom** | **Yes** (Live, app layer) | Yes | No | **No** — explicitly step-by-step | **Yes** | **$0** (Fundamentals) | Classroom/Chromebook scale; all ages since 2026-08-10 |
| **OpenAI** | **Yes** | Yes, 300+ topics | No | Weak, bypassable; auto-reactivating in Teens | **No** (no student accounts) | Teachers free to June 2028 | 300k+ educators, 30 states |
| **Anthropic** | No | Yes (beta) | No | Toggleable style, off by default | Adoption only | Teachers free to 2026-06-30 | US K-12 educators only |
| **Synthesis** | Yes | Manipulatives | No | No | Thin | Consumer $119–300/yr | 68k students, K-5 only |
| **MagicSchool** | **No** | **No** | No | No | Yes (adoption) | $99.96/yr per *teacher* | 6M educators, 10k schools |
| **Photomath / Gauth** | No | Animated steps | No | **No — model forbids it** | No | Consumer $70–100/yr | 100M+ / 50M+ installs |
| **Amira** | **Yes** (reading aloud) | No | No | Reading-Socratic | **Yes** | ~$9 bundle *(reported)* | 1,800–4,000+ districts |
| **Third Space "Skye"** | **Yes** (spoken maths) | Not evidenced | No | Scaffolded | Yes | Not published | UK+US schools; **Gates/Stanford/Cornell RCT** |
| **SolversBoard** | **No** | **Yes** | **Yes** | **Yes, explicitly** | Yes + Canvas LTI | **$0** (BYO key) | Pilots; founded 2026 |
| **Alef** | Not evidenced | Yes | No | No | Yes | *(ADEK contract)* | ~2m learners; 124.5k UAE private |

---

## 12. The three most dangerous

**1 — Google.** Not because Guided Learning is good; it explicitly does not withhold
answers. Because it is **free inside the tier schools already have**, reaches all ages in
Classroom since August, already renders diagrams, ships class-level insights, and has
full-duplex voice one integration away. Google is the only competitor who can zero out the
entire price point without noticing.

**2 — Khanmigo.** The reference point every school committee benchmarks against, with 600+
districts and RCT credibility, and as of three weeks ago **the interactive-visual surface
that was half the differentiator**. They already have push-to-talk voice. The remaining gap
is full-duplex audio and a student-drawable canvas — a UX and latency gap, not a
capability gap. Their weaknesses (15% engagement, US-only students) are exactly what they
are working on.

**3 — OpenAI.** Least threatening on paper today, highest variance. ChatGPT for Teens moved
enforcement from toggle toward policy at consumer scale, arriving in students' pockets
without any school buying anything. The day a rostered student SKU ships, three of four
differentiators go at once.

**Honourable mentions of a different kind:** SolversBoard, doing this pedagogy on this
canvas for free with an LTI integration; and Third Space Learning, which has the spoken
maths tutor *and* the Gates/Stanford/Cornell evidence programme. Neither will out-execute
us. Both are more credible reference points than they are threats, and both will come up
in sales conversations.

---

## 13. What is actually left

Not voice — Amira, Skye, Synthesis and Speak have it. Not a visual surface — all four
frontier labs shipped one in 2026. Not Socratic questioning — four toggles and a free
startup have it.

What survives contact with this scan:

1. **Enforced withholding that is architectural rather than a toggle.**
2. **A student-*drawable* surface the tutor reads while the student works** — every
   incumbent renders visuals *at* the student; almost none read the student's own working.
3. **Analytics that report reasoning process rather than tool adoption.**
4. **A market where Khanmigo cannot legally sell a student a seat, Google is generic, and
   the regional incumbent has no voice product.**

Point 4 is the most durable line in this document — **and it is a distribution advantage
with a shelf life, not a moat.** That distinction is the subject of
[`02-differentiation-and-moat.md`](02-differentiation-and-moat.md).

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-09-08 | CTO (incoming) | Initial teardown, 11 competitors + regional, current to 2026-09-08. |

## Related documents

- [`00-problem-and-personas.md`](00-problem-and-personas.md)
- [`02-differentiation-and-moat.md`](02-differentiation-and-moat.md)
- [`03-risks-and-premortem.md`](03-risks-and-premortem.md)
- [`04-wedge-and-non-goals.md`](04-wedge-and-non-goals.md)
