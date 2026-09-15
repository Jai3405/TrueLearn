---
title: "ADR-015: Empty or truncated model output is a first-class error"
status: Accepted
date: 2026-09-16
deciders: [CTO]
---

# ADR-015: Empty or truncated model output is a first-class error

## Context

Across two independent harnesses and three separate model families, models returned
**empty or truncated responses** under budget pressure, and in every case the harness
scored the result as a *capability* failure:

| Observed | Read as | Actually was |
|---|---|---|
| `0/4 steps, +0 spurious` on every image | "models cannot read handwriting" | Empty content — budget spent on internal reasoning |
| `gemini-3.5-flash` 58.3% vs 85.4% | "the newer model reads worse" | Truncated mid-expression at `maxOutputTokens: 800` |
| Step-down turns scored "held" | "the tutor refused correctly" | The model returned nothing at all |

Reasoning models spend the same output budget on internal reasoning before emitting any
text. When it runs out, `content` is empty and `finish_reason` is `length`. An ambiguous
prompt makes this worse: measured, the v1 prompt spent >300 tokens deliberating whether it
was permitted to confirm an answer and returned nothing, where the v2 prompt answered in
124 tokens.

## Decision

**An empty or truncated model response is an error, never a value.**

1. Empty `content` raises rather than returning `""`.
2. `finish_reason == length` (or `MAX_TOKENS`) raises — truncation is not a short answer.
3. Both are retried with backoff, then fall back to a **designed message**.
4. **No code path may render an empty tutor turn.** `tutor_text` is non-nullable in the API
   contract (LLD §2).
5. Candidate models must be validated for non-empty completion under long context before
   selection, and reasoning budget controlled explicitly where the provider allows it.

## Consequences

**Good.** A silent turn is now visible instead of scoring as good behaviour. Model
comparisons measure models rather than token budgets.

**Bad.** Every provider adapter carries this handling; a wrapper that forgets it
re-introduces the bug. Larger budgets cost marginally more per call.

**The product reason this matters more than the measurement reason:** a student who says
"I don't know" three times and receives silence has been abandoned mid-question — on the
step-down path, which is the retention mechanism. No leakage or accuracy metric would ever
show it.

## Alternatives rejected

- **Treat empty as a refusal.** This is what the harness did by accident, and it made a
  broken step-down look like correct behaviour.
- **Just raise `max_tokens`.** Tried: 800 → 2000 → 6000 changed nothing, because the
  provider capped completions at 300. The budget was never the lever; the prompt was.
