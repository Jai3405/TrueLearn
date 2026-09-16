#!/usr/bin/env python3
"""SPK-4 -- safeguarding detector eval.

Measures the RULES FLOOR. ADR-011 runs a safeguarding screen on every student turn, and the
cost model (09-ops 1) shows a per-turn LLM call would more than double session cost to catch
under 1% of turns. So rules must run on 100% of turns, with a model escalated to only on
suspicion. This harness asks whether rules alone are good enough to be that floor.

Three errors, not two. A binary precision/recall number hides the dangerous one:

    MISS        disclosure scored tier 0      a child in danger is not seen
    FALSE ALARM benign scored tier >= 1       pager fires; this is the COST DRIVER
    MISROUTE    tier 3 scored as tier 2       a parent who may be the abuser is notified

Misroute is invisible to precision/recall because the detector *did* find the disclosure.
It is gated at zero.

Usage:
    python3 spk4_safeguard.py --self-check      # offline harness validation
    python3 spk4_safeguard.py                   # score the rules floor
    python3 spk4_safeguard.py --show-negatives  # print every false alarm, for triage
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE / "disclosures.json"

# --------------------------------------------------------------------------------------
# Rules. Ordered by legal stakes: abuse first, because POCSO s.19 is a criminal duty and
# ADR-011 forbids routing it anywhere near the home.
# --------------------------------------------------------------------------------------

_HOUSEHOLD = (r"(?:father|dad|daddy|papa|mother|mom|mum|amma|nanna|"
              r"step[- ]?(?:father|mother|dad|mom)|parents?|guardian)")

ABUSE = [
    r"\btouch(?:es|ed|ing)?\b(?:(?!notation).){0,30}\b(?:me|my)\b",
    r"\b(?:molest\w*|rape\w*)\b",
    r"\bcomes? into my room\b",
    r"\bdid something to me\b",
    r"\bmakes? me stay back alone\b",
    r"\bsending me photos\b",
    r"\basking for mine\b",
    r"\bdont feel safe with\b",
    r"\bhits? me when\b",
    r"\bbeats? me\b",
    r"\block(?:s|ed)? me in\b",
    r"\bwithout food for days\b",
    r"\bwhat my " + _HOUSEHOLD + r" does\b",
    r"\bis the one hurting me\b",
]

SELF_HARM = [
    r"\bcutting myself\b", r"\bcut myself\b", r"\bhurt myself\b",
    r"\bkill myself\b", r"\bend my life\b", r"\bending it\b",
    r"\bdont want to be here\b", r"\bdont want to live\b",
    r"\bbetter off if i (?:wasnt|was not|werent|were not)\b",
    r"\bdont see the point of any\b",
    r"\bnobody would (?:even )?notice if i\b",
    r"\bdisappeared? tomorrow\b",
    r"\btook some of .{0,24}tablets\b", r"\boverdos\w+\b",
    r"\bstand near the balcony\b",
    r"\bhavent eaten\b(?:.){0,40}\bdont really care\b",
    r"\bsomething to myself\b",
    r"\btired of being alive\b",
    r"\bthinking about (?:ending|killing)\b",
]

THREAT = [
    r"\bbring something to school\b",
    r"\bmake them all pay\b",
    r"\bknow where (?:he|she|they) lives?\b",
    r"\bgoing to hurt (?:him|her|them)\b",
    r"\bget back at (?:him|her)\b(?:.){0,30}\bserious\b",
    r"\bdo something to (?:him|her|them)\b",
]

LOW_CONCERN = [
    r"\bmak(?:e|es|ing) fun of me\b", r"\bbully\w*\b",
    r"\bnot been sleeping\b", r"\bcant sleep\b",
    r"\banxious all the time\b",
    r"\bposting about me\b", r"\bgroup without me\b",
    r"\bcry (?:almost )?every\b",
    r"\beat lunch alone\b",
    r"\bparents fight constantly\b",
    r"\bfalling behind\b(?:.){0,40}\bmiserable\b",
]

# --------------------------------------------------------------------------------------
# Suppressors -- what separates a disclosure from Telugu-English exam-stress idiom. This is
# the whole reason the harness exists. Wrong in one direction costs founder sleep; wrong in
# the other costs a child.
# --------------------------------------------------------------------------------------

MATHS_CONTEXT = re.compile(
    r"\b(?:equation|term|factor|root|asymptote|axis|decimal|recurring|integrat\w+|"
    r"differenti\w+|derivative|constant|discriminant|fraction|matrix|matrices|"
    r"trigonometry|logarithm|syllabus|chapter|substitut\w+|variable|coefficient|"
    r"graph|curve|function|notation|probability|cost price|maximum|minimum|"
    r"common factor)\b",
    re.I,
)

IDIOM = re.compile(
    r"\b(?:if i (?:fail|dont|lose|score|get)|before boards|in boards|unit test|"
    r"this (?:test|paper|chapter|question|problem|syllabus)|one more|"
    r"rather die than|death of me)\b",
    re.I,
)

HYPERBOLE_TARGET = re.compile(
    _HOUSEHOLD + r"\b(?:.){0,34}\b(?:will|is going to|said he will|gonna)\b(?:.){0,20}"
    r"\b(?:kill|murder|destroy|slaughter|break my legs|beat)\b",
    re.I,
)

SELF_DIRECTED = re.compile(r"\b(?:myself|my wrist|my arm|my life)\b", re.I)


# --------------------------------------------------------------------------------------
# ESCALATION NET.
#
# Measured 2026-09-16: the precise rules above score 76/76 on the corpus they were written
# against and MISS 18 of 18 disclosures on held-out phrasing. Precise rules do not
# generalise, so they cannot be the classifier.
#
# The fix is to invert their job. Rules become a cheap, deliberately LOW-PRECISION,
# HIGH-RECALL triage net whose only question is "could this possibly be a disclosure?"
# Anything it catches goes to a model for actual classification. Rules triage; the model
# classifies. Cost is then escalation_rate x model_cost, not model_cost on every turn.
# --------------------------------------------------------------------------------------

ESCALATE_NET = re.compile(
    r"""(?xi)
    \b(?:
        # harm, injury, death -- any form, any target
        hurt|harm|burn\w*|cut\w*|bleed\w*|blood|wound|scar|knife|blade|
        die|died|dying|dead|death|kill\w*|murder\w*|suicide|
        slap\w*|beat\w*|thrash\w*|hit|hits|hitting|rag|ragging|
        # finality, absence, escape
        disappear\w*|vanish\w*|gone|end\s+it|ending|finish\w*|stop|relieved|
        escape|run\s+away|not\s+be\s+here|wake\s+up|alive|letter|
        # contact, body, privacy
        touch\w*|lap|room|bed|photo\w*|picture\w*|secret|private|
        # household and kin (Telugu and English)
        father|dad|papa|mother|mom|amma|nanna|parents?|guardian|uncle|aunt|
        chinnanna|peddanna|chithi|mama|attha|brother|sister|cousin|step\w*|
        # authority and setting
        sir|madam|teacher|tuition|senior\w*|warden|
        # affect
        scared|afraid|alone|lonely|low|sad|cry\w*|depress\w*|anxious|
        upset|strange|weird|uncomfortable|hate|miserable|tired|
        # secrecy and disclosure markers
        dont\s+tell|do\s+not\s+tell|nobody\s+knows|please\s+dont
    )\b
    """,
)

# First-person personal content -- the student talking about themselves rather than the sum.
PERSONAL = re.compile(
    r"(?i)(?:\b(?:i|me|my|myself|mine|nobody|everyone|anyone|somebody|someone)\b"
    r"|\bi'?m\b|\bi'?ve\b|\bi'?ll\b)"
)

# A turn is "clearly maths" only when it carries real maths vocabulary AND asks or states
# something about the problem rather than the student.
MATHS_ONLY = re.compile(
    r"(?i)\b(?:equation|term|factor|root|asymptote|axis|decimal|recurring|integrat\w+|"
    r"differenti\w+|derivative|constant|discriminant|fraction|matrix|matrices|"
    r"trigonometry|logarithm|substitut\w+|variable|coefficient|graph|curve|function|"
    r"notation|probability|cost price|maximum|minimum|common factor|denominator|"
    r"numerator|solve|sum|step|answer|formula|syllabus|chapter|percent|profit|"
    r"degenerate|square|differentiate|practise|practice)\b"
)


def should_escalate(text: str) -> bool:
    """Cheap triage, running on 100% of turns. Only hits pay for a model call.

    Inverted on purpose. Rather than asking "is this a disclosure?" -- which precise rules
    answered with 0% recall on held-out phrasing -- it asks "is this anything other than a
    maths turn?" Separating personal content from maths content is a far easier and far
    more robust discrimination, and it degrades safely: an unfamiliar way of describing
    harm still escalates, because it still isn't maths.

    Deliberately over-fires. A false escalation costs a fraction of a cent; a missed one
    is a child.
    """
    if not PERSONAL.search(text):
        return False  # no first-person content at all -- a bare problem statement
    if ESCALATE_NET.search(text):
        return True  # any harm/kin/affect/secrecy token, regardless of maths context
    return not MATHS_ONLY.search(text)


def _any(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, re.I) for p in patterns)


def parent_is_implicated(text: str) -> bool:
    """True when the transcript points at the household. Forces Tier 3 (ADR-011)."""
    if HYPERBOLE_TARGET.search(text):
        return False  # "my dad will kill me if i fail" -- idiom, not a disclosure
    checks = [
        r"\bdont tell my parents\b(?:.){0,40}\b(?:hurting|hurts|abus)\w*",
        r"\bmy " + _HOUSEHOLD + r"\b(?:.){0,40}\bis the one hurting me\b",
        r"my " + _HOUSEHOLD + r"\b(?:.){0,30}\b(?:touch\w+|hits?|beats?|locks? me)\b",
        r"\bwhat my " + _HOUSEHOLD + r" does\b",
        r"\bmy " + _HOUSEHOLD + r"\b(?:.){0,40}\bwithout food for days\b",
    ]
    return any(re.search(c, text, re.I) for c in checks)


def classify(text: str) -> tuple[int, bool]:
    """Rules-only classifier. Returns (tier, parent_implicated).

    Abuse is tested first and is NOT suppressible by idiom heuristics: suppressing a real
    abuse disclosure is not comparable in cost to a false alarm, and POCSO s.19(7) gives
    good-faith immunity for over-reporting.
    """
    implicated = parent_is_implicated(text)
    if implicated:
        return 3, True

    if _any(ABUSE, text):
        return 3, False

    if _any(SELF_HARM, text):
        # Idiom suppression applies ONLY when the utterance is not self-directed.
        # "if i fail i am going to do something to myself" must stay Tier 2.
        if not SELF_DIRECTED.search(text) and (IDIOM.search(text) or MATHS_CONTEXT.search(text)):
            return 0, False
        return 2, False

    if _any(THREAT, text):
        return 4, False

    if _any(LOW_CONCERN, text):
        return 1, False

    return 0, False


# --------------------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------------------


def load_corpus(path: Path = CORPUS) -> list[dict]:
    data = json.loads(path.read_text())
    cases = data["cases"]
    seen: set[str] = set()
    for c in cases:
        for field in ("id", "tier", "category", "utterance", "parent_implicated"):
            if field not in c:
                raise SystemExit(f"corpus case missing {field!r}: {c.get('id', '?')}")
        if c["id"] in seen:
            raise SystemExit(f"duplicate corpus id: {c['id']}")
        seen.add(c["id"])
        if c["parent_implicated"] and c["tier"] != 3:
            raise SystemExit(
                f"{c['id']}: parent_implicated must imply tier 3 (ADR-011), got {c['tier']}"
            )
    return cases


def score(cases: list[dict]) -> dict:
    misses, false_alarms, misroutes, correct = [], [], [], []
    tier_conf: dict[tuple[int, int], int] = {}

    for c in cases:
        got_tier, got_impl = classify(c["utterance"])
        want_tier, want_impl = c["tier"], c["parent_implicated"]
        tier_conf[(want_tier, got_tier)] = tier_conf.get((want_tier, got_tier), 0) + 1
        rec = {**c, "got_tier": got_tier, "got_parent_implicated": got_impl}

        if want_tier >= 1 and got_tier == 0:
            misses.append(rec)
        elif want_tier == 0 and got_tier >= 1:
            false_alarms.append(rec)
        elif want_tier == 3 and got_tier != 3:
            misroutes.append(rec)
        elif want_impl and not got_impl:
            misroutes.append(rec)  # found, but the household was not flagged
        else:
            correct.append(rec)

    n_benign = sum(1 for c in cases if c["tier"] == 0)
    return {
        "n": len(cases),
        "misses": misses,
        "false_alarms": false_alarms,
        "misroutes": misroutes,
        "correct": correct,
        "n_benign": n_benign,
        "flag_rate_benign": len(false_alarms) / n_benign if n_benign else 0.0,
        "tier_conf": tier_conf,
    }


def report(res: dict, show_negatives: bool) -> None:
    n = res["n"]
    print(f"\n{'=' * 74}")
    print(f"SPK-4 safeguarding detector -- RULES FLOOR, {n} synthetic cases")
    print("=" * 74)
    print(f"\n  correct        {len(res['correct']):3d} / {n}")
    print(f"  MISSES         {len(res['misses']):3d}   (disclosure scored tier 0)")
    print(f"  false alarms   {len(res['false_alarms']):3d}   (benign scored tier >= 1)")
    print(f"  MISROUTES      {len(res['misroutes']):3d}   (tier 3 not routed as tier 3)")
    print(f"\n  flag rate on benign corpus:  {res['flag_rate_benign'] * 100:.1f}%"
          f"   ({len(res['false_alarms'])}/{res['n_benign']})")

    print("\n  tier confusion (want -> got):")
    for want in range(5):
        row = {got: c for (w, got), c in res["tier_conf"].items() if w == want}
        if row:
            cells = "  ".join(f"{g}:{c}" for g, c in sorted(row.items()))
            print(f"    tier {want} ->  {cells}")

    if res["misses"]:
        print("\n  MISSES -- each one is a child not seen:")
        for m in res["misses"]:
            print(f"    [{m['id']}] tier {m['tier']}  {m['utterance'][:64]}")

    if res["misroutes"]:
        print("\n  MISROUTES -- gated at zero:")
        for m in res["misroutes"]:
            print(f"    [{m['id']}] want tier {m['tier']} impl={m['parent_implicated']} "
                  f"-> got tier {m['got_tier']} impl={m['got_parent_implicated']}")
            print(f"         {m['utterance'][:64]}")

    if show_negatives and res["false_alarms"]:
        print("\n  FALSE ALARMS -- each is one pager wake. Triage by hand:")
        for f in res["false_alarms"]:
            print(f"    [{f['id']}] -> tier {f['got_tier']}  {f['utterance'][:60]}")
            if f.get("note"):
                print(f"         note: {f['note']}")

    print(f"\n{'-' * 74}")
    if res["misroutes"]:
        print("  VERDICT: FAIL -- misroute is gated at zero (ADR-011).")
    elif res["misses"]:
        print(f"  VERDICT: FAIL -- {len(res['misses'])} missed disclosure(s). "
              "Recall is the non-negotiable axis.")
    else:
        print("  VERDICT: rules floor holds. 0 misses, 0 misroutes.")
        print(f"  Pager load is set by the {res['flag_rate_benign'] * 100:.1f}% "
              "benign flag rate.")
    print("-" * 74)
    print("\n  NOTE: synthetic corpus (A-025). This sizes the rota; it does NOT validate")
    print("  the detector against real children. Re-measure in the first pilot term.\n")


# --------------------------------------------------------------------------------------
# Offline self-check -- invariant 3 from docs/07-quality/02-test-and-eval-strategy.md.
# A detector that silently reports nothing looks exactly like one that is working.
# --------------------------------------------------------------------------------------

SELF_CHECK_CASES = [
    ("i have been cutting myself when it gets bad", 2, False, "explicit self-harm"),
    ("my dad will literally kill me if i fail this test", 0, False, "exam idiom, not a threat"),
    ("my father touches me and says its normal", 3, True, "abuse, household implicated"),
    ("do i eliminate x first or y first", 0, False, "maths vocabulary collision"),
    ("i killed the middle term but it looks wrong", 0, False, "maths vocabulary collision"),
    ("my teacher said this is an abuse of notation", 0, False, "'abuse' in the maths sense"),
    ("if i fail this exam i am going to do something to myself, i mean it",
     2, False, "self-directed: idiom must NOT suppress"),
    ("i am going to bring something to school and make them all pay", 4, False, "threat"),
    ("some boys in my class keep making fun of me", 1, False, "low concern"),
    ("can you check if my step 3 is correct", 0, False, "ordinary maths turn"),
    ("please dont tell my parents, my mother is the one hurting me", 3, True, "household"),
    ("where does this line cut the x axis", 0, False, "maths: cut"),
]


def self_check() -> int:
    print("SPK-4 self-check (offline, no corpus dependency, no network)\n")
    failures = 0
    for text, want_tier, want_impl, why in SELF_CHECK_CASES:
        got_tier, got_impl = classify(text)
        ok = (got_tier == want_tier) and (got_impl == want_impl)
        failures += 0 if ok else 1
        print(f"  [{'ok  ' if ok else 'FAIL'}] tier {got_tier} impl={str(got_impl):5s} "
              f"(want {want_tier}/{want_impl})  {why}")
        if not ok:
            print(f"         {text!r}")

    try:
        cases = load_corpus()
        n_neg = sum(1 for c in cases if c["tier"] == 0)
        pct = n_neg / len(cases) * 100
        print(f"\n  corpus: {len(cases)} cases, {n_neg} hard negatives ({pct:.0f}%)")
        if pct < 50:
            print("  [FAIL] under half the corpus is hard negatives -- the "
                  "false-positive measurement is not trustworthy")
            failures += 1
    except SystemExit as e:
        print(f"\n  [FAIL] corpus integrity: {e}")
        failures += 1

    print(f"\n{'SELF-CHECK PASSED' if not failures else f'SELF-CHECK FAILED ({failures})'}\n")
    return 1 if failures else 0


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--self-check", action="store_true",
                   help="validate the harness offline and exit")
    p.add_argument("--show-negatives", action="store_true",
                   help="print every false alarm for hand triage")
    p.add_argument("--escalation", action="store_true",
                   help="measure the triage net instead of the classifier")
    p.add_argument("--corpus", type=Path, default=CORPUS)
    args = p.parse_args()

    if args.self_check:
        return self_check()

    cases = load_corpus(args.corpus)

    if args.escalation:
        return report_escalation(cases, args.corpus.name)

    res = score(cases)
    report(res, args.show_negatives)
    return 1 if (res["misses"] or res["misroutes"]) else 0


def report_escalation(cases: list[dict], name: str) -> int:
    """Measure the triage net: recall on disclosures, escalation rate on benign."""
    disclosures = [c for c in cases if c["tier"] >= 1]
    benign = [c for c in cases if c["tier"] == 0]

    caught = [c for c in disclosures if should_escalate(c["utterance"])]
    leaked = [c for c in disclosures if not should_escalate(c["utterance"])]
    escalated_benign = [c for c in benign if should_escalate(c["utterance"])]

    recall = len(caught) / len(disclosures) if disclosures else 0.0
    esc_rate = len(escalated_benign) / len(benign) if benign else 0.0
    overall = (len(caught) + len(escalated_benign)) / len(cases)

    print(f"\n{'=' * 74}")
    print(f"SPK-4 ESCALATION NET -- {name}, {len(cases)} cases")
    print("=" * 74)
    print(f"\n  recall on disclosures       {recall * 100:5.1f}%   "
          f"({len(caught)}/{len(disclosures)})   <- must approach 100%")
    print(f"  escalation rate on benign   {esc_rate * 100:5.1f}%   "
          f"({len(escalated_benign)}/{len(benign)})   <- drives model cost")
    print(f"  overall turns escalated     {overall * 100:5.1f}%")

    model_cost = overall * 0.002 * 8
    print(f"\n  modelled cost: {overall * 100:.0f}% x $0.002/turn x 8 turns "
          f"= ${model_cost:.4f}/session")
    print(f"  against a $0.015 session budget: +{model_cost / 0.015 * 100:.0f}%")
    print("  (a model on EVERY turn would be $0.016/session, +107%)")

    if leaked:
        print(f"\n  NOT ESCALATED -- {len(leaked)} disclosure(s) the net would never see:")
        for c in leaked:
            print(f"    [{c['id']}] tier {c['tier']}  {c['utterance'][:60]}")

    print(f"\n{'-' * 74}")
    if recall < 1.0:
        print(f"  VERDICT: FAIL -- {len(leaked)} disclosure(s) never reach the model.")
    else:
        print("  VERDICT: net holds. 100% of disclosures reach the model classifier.")
    print("-" * 74 + "\n")
    return 0 if recall == 1.0 else 1


if __name__ == "__main__":
    sys.exit(main())
