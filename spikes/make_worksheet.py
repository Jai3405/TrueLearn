#!/usr/bin/env python3
"""Generate handwriting test material for PQ-01, so no data collection is needed.

The question PQ-01 actually asks is not "can a model read *student* handwriting" -
it is "can a model read MULTI-STEP handwritten working that contains mistakes,
photographed casually". You can produce that yourself in an hour.

This writes two files:

  worksheet.txt  - numbered items to copy onto paper BY HAND, exactly as printed
  truth.json     - the ground truth, already filled in, keyed by "<NN>.jpg"

So the workflow is: run this, copy each item onto paper in your own handwriting,
photograph it as <NN>.jpg, then run pq1_ocr.py. No transcription needed - the
ground truth is generated alongside the worksheet.

    python3 spikes/make_worksheet.py --out ~/handwriting --count 20
    python3 spikes/make_worksheet.py --self-check

About half the items contain a DELIBERATE, realistic mistake (sign slip, dropped
term, arithmetic error) which then propagates through the later steps. That is the
point: a model that silently "corrects" the mistake has failed, because seeing the
student's actual error is the entire product.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

# Each generator returns (problem, correct_steps, wrong_steps).
# `wrong_steps` embeds a realistic slip and propagates it, the way a student's
# working actually looks - not a single isolated typo.


def num(v: float) -> str:
    """Render a value the way a student would write it: integers bare, otherwise
    two decimal places. Long repeating decimals are tedious to copy accurately and
    would measure the copier's patience rather than the model's reading."""
    return str(int(v)) if float(v).is_integer() else f"{v:.2f}"


def linear(r: random.Random):
    a, x, b = r.randint(2, 9), r.randint(2, 12), r.randint(3, 19)
    c = a * x + b
    correct = [f"{a}x + {b} = {c}", f"{a}x = {c - b}", f"x = {x}"]
    # sign slip: adds b instead of subtracting it
    bad = c + b
    wrong = [f"{a}x + {b} = {c}", f"{a}x = {bad}", f"x = {num(bad / a)}"]
    return f"Solve for x:  {a}x + {b} = {c}", correct, wrong


def bracket(r: random.Random):
    a, x, b = r.randint(2, 7), r.randint(3, 11), r.randint(2, 8)
    c = a * (x - b)
    correct = [f"{a}(x - {b}) = {c}", f"x - {b} = {c // a}", f"x = {x}"]
    # forgets to distribute onto the constant
    wrong = [f"{a}(x - {b}) = {c}", f"{a}x - {b} = {c}", f"x = {num((c + b) / a)}"]
    return f"Solve for x:  {a}(x - {b}) = {c}", correct, wrong


def quadratic(r: random.Random):
    p, q = r.randint(1, 7), r.randint(1, 7)
    b, c = p + q, p * q
    correct = [f"x^2 + {b}x + {c} = 0", f"(x + {p})(x + {q}) = 0", f"x = -{p} or x = -{q}"]
    # loses the sign on the roots
    wrong = [f"x^2 + {b}x + {c} = 0", f"(x + {p})(x + {q}) = 0", f"x = {p} or x = {q}"]
    return f"Factorise and solve:  x^2 + {b}x + {c} = 0", correct, wrong


def derivative(r: random.Random):
    a, b = r.randint(2, 9), r.randint(2, 9)
    correct = [f"y = {a}x^2 + {b}x", f"dy/dx = {2 * a}x + {b}"]
    # drops the power rule multiplier
    wrong = [f"y = {a}x^2 + {b}x", f"dy/dx = {a}x + {b}"]
    return f"Differentiate:  y = {a}x^2 + {b}x", correct, wrong


def progression(r: random.Random):
    first, d, n = r.randint(2, 9), r.randint(2, 7), r.randint(8, 15)
    nth = first + (n - 1) * d
    correct = [f"a = {first}, d = {d}, n = {n}", "a_n = a + (n - 1)d",
               f"a_n = {first} + {n - 1} x {d}", f"a_n = {nth}"]
    # off-by-one: uses n instead of n-1
    bad = first + n * d
    wrong = [f"a = {first}, d = {d}, n = {n}", "a_n = a + nd",
             f"a_n = {first} + {n} x {d}", f"a_n = {bad}"]
    return (f"Find the {n}th term of the AP starting {first} with common difference {d}",
            correct, wrong)


def fraction(r: random.Random):
    d1, d2 = r.choice([(3, 6), (4, 8), (2, 6), (5, 10), (3, 9)])
    n1, n2 = r.randint(1, d1 - 1), r.randint(1, d2 - 1)
    lcm = d2  # d2 is a multiple of d1 in every pair above
    num = n1 * (lcm // d1) + n2
    correct = [f"{n1}/{d1} + {n2}/{d2}", f"= {n1 * (lcm // d1)}/{lcm} + {n2}/{lcm}",
               f"= {num}/{lcm}"]
    # adds numerators and denominators straight across
    wrong = [f"{n1}/{d1} + {n2}/{d2}", f"= {n1 + n2}/{d1 + d2}"]
    return f"Evaluate:  {n1}/{d1} + {n2}/{d2}", correct, wrong


GENERATORS = [linear, bracket, quadratic, derivative, progression, fraction]

HEADER = """\
PQ-01 HANDWRITING TEST SHEET
============================

HOW TO USE THIS - about one hour.

1. Copy each item below onto paper BY HAND, exactly as printed, including any
   mistakes. Do not correct anything. Do not print it - handwrite it.
2. Write naturally and fairly fast. Neat handwriting is not the test.
3. Photograph each item with a phone and save it as the filename shown.
4. Deliberately make the photos imperfect: hold the phone at an angle, use dim
   indoor light for at least five of them, and use ruled paper and pencil for
   some. Cheap photos in bad light are what the product will actually receive.
5. If you can, get one or two other people to write some of them - handwriting
   variation is a large part of what is being measured.

Then:
    OPENROUTER_API_KEY=... python3 spikes/pq1_ocr.py \\
        --provider openrouter --images {out} --truth {out}/truth.json

Items marked (contains a mistake) have a deliberate error that propagates through
the later lines. Copy them wrong, exactly as shown. A model that silently corrects
the mistake has FAILED - seeing the student's actual error is the whole product.

------------------------------------------------------------------------
"""


def build(count: int, seed: int) -> tuple[str, dict]:
    r = random.Random(seed)
    lines, truth = [], {}
    for i in range(1, count + 1):
        problem, correct, wrong = GENERATORS[(i - 1) % len(GENERATORS)](r)
        use_wrong = i % 2 == 0  # alternate, so roughly half contain a mistake
        steps = wrong if use_wrong else correct
        name = f"{i:02d}.jpg"
        truth[name] = steps
        tag = "  (contains a mistake - copy it exactly as shown)" if use_wrong else ""
        lines.append(f"\nITEM {i:02d}   ->  save photo as {name}{tag}")
        lines.append(f"Problem: {problem}")
        lines.append("Write these lines:")
        lines.extend(f"    {s}" for s in steps)
        lines.append("-" * 72)
    return "\n".join(lines), truth


def self_check() -> None:
    body, truth = build(12, seed=7)
    assert len(truth) == 12, truth.keys()
    assert all(k.endswith(".jpg") for k in truth)
    assert all(isinstance(v, list) and v for v in truth.values())
    assert "ITEM 01" in body and "ITEM 12" in body
    # Every generator must be exercised and produce differing correct/wrong paths.
    r = random.Random(1)
    for g in GENERATORS:
        problem, correct, wrong = g(r)
        assert problem and correct and wrong, g.__name__
        assert correct != wrong, f"{g.__name__}: error variant is identical to correct"
    # Determinism - the ground truth must match what was printed on the sheet.
    assert build(12, seed=7)[1] == truth, "generator is not deterministic for a fixed seed"
    # Values must be copyable by hand: no long repeating decimals.
    assert num(4.0) == "4" and num(1.3333333) == "1.33", (num(4.0), num(1.3333333))
    for steps in truth.values():
        for s in steps:
            frac = [p for p in s.split() if "." in p]
            assert all(len(p.split(".")[-1].rstrip(",")) <= 2 for p in frac), s
    print(f"self-check OK - {len(GENERATORS)} generators, deterministic, "
          f"correct/error variants differ, {len(truth)} items built")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", type=Path, help="output directory (keep it OUTSIDE this repo)")
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--seed", type=int, default=20260908)
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args()

    if args.self_check:
        self_check()
        return 0
    if not args.out:
        p.error("--out is required (or use --self-check)")

    args.out.mkdir(parents=True, exist_ok=True)
    body, truth = build(args.count, args.seed)
    (args.out / "worksheet.txt").write_text(HEADER.format(out=args.out) + body + "\n")
    (args.out / "truth.json").write_text(json.dumps(truth, indent=2) + "\n")

    mistakes = sum(1 for i in range(1, args.count + 1) if i % 2 == 0)
    print(f"wrote {args.out}/worksheet.txt   ({args.count} items, {mistakes} with a deliberate mistake)")
    print(f"wrote {args.out}/truth.json      (ground truth, already filled in)")
    print("\nNext: handwrite each item, photograph as NN.jpg in that directory, then run pq1_ocr.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
