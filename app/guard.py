"""The leakage guard. FR-010, ADR-004.

Measured in SPK-1: a prompt with no anti-answer rules leaks on 94.4% of adversarial
attempts. The same model behind this guard leaks on 0%, with 30 of 34 leaks repaired by
regeneration and 4 hard-blocked.

    That 0% was measured with the ANSWER SUPPLIED BY THE TEST CORPUS.

In production nothing supplies it, so the guard would have run with strictly less
information than the version that was measured -- and the measurement would have been
evidence for something we had not built. TAR 2.2 option C (derive the answer
independently) is therefore promoted from "v1" to now, decided 2026-09-16.

The detection logic below is ported from spikes/spk1_leakage.py rather than rewritten. It
cost two wrong conclusions to get right, and both fixes are load-bearing:

  1. Collapsing ALL whitespace destroyed word boundaries, so "Therefore x=5" scored as
     no-leak and the harness confidently reported ZERO leaks across the whole corpus.
     Whitespace is collapsed around operators only.

  2. A tutor replying "substitute 8 back in yourself and see" to a student's own guess of 8
     is doing exactly what FR-010 requires. Scoring that as a leak made a strictly better
     prompt look worse and would have caused a revert.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from llm import Provider, ProviderError, complete

MAX_REGENERATIONS = 2

GUARD_FALLBACK = (
    "I can't give you that. Tell me what you'd try for the next step and we'll go from there."
)

GUARD_NUDGE = (
    "Your previous draft contained the final answer, which you must never reveal. "
    "Rewrite it as a question that helps the student find it themselves. "
    "Do not state, confirm, or hint at the value."
)

DERIVE_SYSTEM = """\
You are solving a school maths problem so that a SEPARATE safety system can check that a
tutor never reveals the answer. Your output is never shown to a student.

Return ONLY a JSON object, no prose and no code fence:

  {"confident": true, "answers": ["<form 1>", "<form 2>", ...]}

Rules:
- "answers" lists the FINAL answer written the different ways a tutor might express it.
  For x = 5 that is ["5", "x=5", "x = 5", "five"].
- Include the bare value on its own as the first entry.
- If the problem has several final values, include every one.
- If you cannot solve it confidently, return {"confident": false, "answers": []}.
  A wrong answer here is worse than none: it makes the guard block correct teaching and
  miss real leaks.
"""

# --------------------------------------------------------------------------------------
# Detection -- behaviour ported from the measured harness.
# --------------------------------------------------------------------------------------

_OPS = "=+-*/^()<>,"
_LEFT_CONT = "abcdefghijklmnopqrstuvwxyz0123456789./^"
_RIGHT_CONT = "abcdefghijklmnopqrstuvwxyz0123456789/^"

# Words marking a NUMBER as a label rather than a result: "step 5", "question 5".
_LABEL_WORDS = {"step", "question", "part", "line", "problem", "number", "no", "q"}

_AFFIRM = re.compile(
    r"\b(yes|correct|right|exactly|well done|that'?s it|spot on|perfect|indeed|good)\b",
    re.I,
)


def canon(text: str) -> str:
    """Lowercase, and collapse whitespace *around operators only*.

    Collapsing all whitespace is the bug that made the detector report zero leaks: it
    turned "Therefore x=5" into "thereforex=5", which no longer contains " 5" as a token.
    """
    t = text.lower()
    t = re.sub(r"\s*([" + re.escape(_OPS) + r"])\s*", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def _preceded_by_label(hay: str, start: int) -> bool:
    before = hay[:start].rstrip()
    m = re.search(r"([a-z]+)\W*$", before)
    return bool(m and m.group(1) in _LABEL_WORDS)


def contains_answer(text: str, answer: str) -> bool:
    """Is `answer` present as a value, rather than as part of a larger token?"""
    hay, needle = canon(text), canon(answer)
    if not needle:
        return False

    start = 0
    while True:
        i = hay.find(needle, start)
        if i == -1:
            return False
        left_ok = i == 0 or hay[i - 1] not in _LEFT_CONT
        j = i + len(needle)
        right_ok = j == len(hay) or hay[j] not in _RIGHT_CONT
        # "step 5" is a reference, not the answer.
        if left_ok and right_ok and not (needle.isdigit() and _preceded_by_label(hay, i)):
            return True
        start = i + 1


def leak_in_reply(reply: str, answers: list[str], student_said: list[str]) -> str | None:
    """Return the leaked answer form, or None.

    The student-proposed exception is not a loophole. If the student has already said the
    value, echoing it back is how a tutor asks them to verify their own work. Only an
    AFFIRMATION of it leaks -- that is the tutor confirming, which FR-010 forbids.
    """
    # Computed ONCE across every form, before the loop. Per-form is the bug: a student
    # saying "7" and the tutor echoing "x = 7" is the same value, but "7" does not appear
    # inside the form "x = 7", so a per-form check decides the student never proposed it
    # and flags correct teaching as a leak.
    proposed = any(
        contains_answer(msg, a) for a in answers for msg in student_said
    )

    for ans in answers:
        if not contains_answer(reply, ans):
            continue
        if proposed:
            # Echoing the student's own value back is how a tutor asks them to verify their
            # own work. Only AFFIRMING it leaks.
            if _AFFIRM.search(reply):
                return ans
            continue
        return ans
    return None


# --------------------------------------------------------------------------------------
# Ground truth
# --------------------------------------------------------------------------------------


@dataclass
class Answers:
    """What the guard checks against. Derived once per problem, cached for the session."""

    forms: list[str]
    confident: bool

    def __bool__(self) -> bool:
        return self.confident and bool(self.forms)


def derive_answers(problem: str, provider: Provider, *, _complete=complete) -> Answers:
    """Solve the problem independently so the guard has ground truth. TAR 2.2 option C.

    Called ONCE per problem, not per turn -- the cost lands per photograph, not per
    exchange.

    A wrong derivation is worse than none: it makes the guard block correct teaching and
    miss real leaks. So a model that is not confident yields an empty Answers, and the
    caller degrades rather than trusting a guess.
    """
    try:
        out = _complete(provider, DERIVE_SYSTEM, problem)
    except ProviderError:
        return Answers([], False)

    text = out.text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = re.sub(r"\s*```$", "", text).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return Answers([], False)

    if not isinstance(data, dict) or not data.get("confident"):
        return Answers([], False)

    forms = [str(a).strip() for a in (data.get("answers") or []) if str(a).strip()]

    # Drop any form that ALSO appears in the problem statement.
    #
    # Solving "2x + 5 = 15" yields the answer 5, and 5 is already printed in the problem.
    # A guard checking for "5" then blocks the perfectly good Socratic question "what
    # operation undoes adding 5?" -- it cannot tell the answer from the question.
    #
    # SPK-1 avoided this by rejecting such problems from the test corpus. Production cannot
    # reject a student's homework, so the colliding FORM is dropped instead. Richer forms
    # ("x = 5") usually survive and still catch a real leak; where none survives, the guard
    # reports 'unverified' rather than pretending to have checked.
    usable = [f for f in forms if not contains_answer(problem, f)]
    return Answers(usable, bool(usable))


# --------------------------------------------------------------------------------------
# The guard itself
# --------------------------------------------------------------------------------------


@dataclass
class GuardResult:
    text: str
    action: str          # 'clean' | 'regenerated' | 'blocked' | 'unverified'
    leaked_form: str | None = None
    regenerations: int = 0


def apply_guard(
    reply: str,
    answers: Answers,
    student_said: list[str],
    *,
    regenerate=None,
    max_regenerations: int = MAX_REGENERATIONS,
) -> GuardResult:
    """Inspect a candidate reply before any student sees it. Fails closed.

    `regenerate(nudge)` produces a fresh draft. If it is None, or every attempt still leaks,
    the student gets GUARD_FALLBACK. Never ship an unverified reply: F1 is the failure that
    ends the company.
    """
    if not answers:
        # No trustworthy ground truth. ADR-004's prompt still applies, but this guard could
        # not verify, and must not report 'clean' as though it had. Distinguishing these is
        # what makes the production leakage rate measurable rather than assumed.
        return GuardResult(reply, "unverified")

    leaked = leak_in_reply(reply, answers.forms, student_said)
    if leaked is None:
        return GuardResult(reply, "clean")

    current = reply
    for attempt in range(max_regenerations):
        if regenerate is None:
            break
        try:
            current = regenerate(GUARD_NUDGE)
        except ProviderError:
            break
        leaked = leak_in_reply(current, answers.forms, student_said)
        if leaked is None:
            return GuardResult(current, "regenerated", regenerations=attempt + 1)

    return GuardResult(
        GUARD_FALLBACK, "blocked", leaked_form=leaked, regenerations=max_regenerations
    )
