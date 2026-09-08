#!/usr/bin/env python3
"""PQ-01 - can a multimodal model read Indian student maths handwriting?

Measures step-level transcription accuracy against NFR-002 (>=92%). This is the
single point of failure for the whole product: if the model cannot read a Grade 11
student's rushed algebra, FR-002 fails and the photo-capture wedge does not work.

Stdlib only.

    python3 spikes/pq1_ocr.py --self-check               # offline, validates scoring
    GEMINI_API_KEY=... python3 spikes/pq1_ocr.py --images ~/handwriting --truth ~/handwriting/truth.json

truth.json maps each image filename to the steps a human reads in it:

    {
      "g10_01.jpg": ["3x + 7 = 22", "3x = 15", "x = 5"],
      "g11_04.jpg": ["dy/dx = 2x + 3", "at x = 1, dy/dx = 5"]
    }

PRIVACY: student handwriting is personal data. Keep images OUTSIDE this repo and
never commit them. The runner refuses in-repo paths unless you override.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent
OUT_DIR = HERE / "out"

PROMPT = """\
Transcribe every line of mathematical working in this image, in order.

Rules:
- Output one line per line of working. No commentary, no explanation, no headings.
- Transcribe exactly what is written, including mistakes. Do not correct anything.
- Do not solve the problem or add missing steps.
- Use plain text maths: ^ for powers, / for fractions, * for multiplication.
- If a line is illegible, output the single token: [ILLEGIBLE]
"""

_OPS = "=+-*/^()<>,"
_MIME = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
         "webp": "image/webp", "heic": "image/heic"}


def canon(s: str) -> str:
    """Normalise a step for comparison: case, whitespace around operators, and
    the cosmetic differences that are not transcription errors."""
    t = s.lower().strip()
    for a, b in (("×", "*"), ("÷", "/"), ("−", "-"), ("²", "^2"), ("³", "^3")):
        t = t.replace(a, b)
    t = re.sub(r"\s*([" + re.escape(_OPS) + r"])\s*", r"\1", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip().rstrip(".")


def score(expected: list[str], got: list[str]) -> dict:
    """Step-level accuracy: how many expected steps were transcribed correctly,
    allowing the model to be off by position (it may split or reorder a line).

    Deliberately strict on content and lenient on ordering - a model that reads
    every symbol right but merges two lines is far more useful than one that
    hallucinates a plausible step.
    """
    exp = [canon(e) for e in expected]
    remaining = [canon(g) for g in got]
    hits = 0
    for e in exp:
        if e in remaining:
            remaining.remove(e)
            hits += 1
    return {
        "expected_steps": len(exp),
        "correct_steps": hits,
        "spurious_steps": len(remaining),
        "accuracy": hits / len(exp) if exp else 0.0,
    }


def call_gemini(model: str, image: Path) -> str:
    key = os.environ["GEMINI_API_KEY"]
    ext = image.suffix.lower().lstrip(".")
    if ext not in _MIME:
        raise ValueError(f"unsupported image type: {image.name}")
    body = {
        "contents": [{"role": "user", "parts": [
            {"text": PROMPT},
            {"inline_data": {"mime_type": _MIME[ext],
                             "data": base64.b64encode(image.read_bytes()).decode()}},
        ]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 800},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return ""


def self_check() -> None:
    """Offline check on the scorer. Guards against the scorer flattering the model."""
    assert canon("3X + 7 = 22") == canon("3x+7=22")
    assert canon("x²  −  4") == canon("x^2-4")
    assert canon("x = 5.") == canon("x=5")

    perfect = score(["3x + 7 = 22", "3x = 15", "x = 5"], ["3x+7=22", "3x = 15", "x=5"])
    assert perfect["accuracy"] == 1.0, perfect

    partial = score(["3x + 7 = 22", "3x = 15", "x = 5"], ["3x+7=22", "3x = 14", "x=5"])
    assert abs(partial["accuracy"] - 2 / 3) < 1e-9, partial

    # A model that silently "corrects" the student is wrong, not right.
    corrected = score(["3x = 14", "x = 4.67"], ["3x = 15", "x = 5"])
    assert corrected["accuracy"] == 0.0, corrected

    # Hallucinated extra lines are counted and reported.
    noisy = score(["x = 5"], ["x = 5", "therefore the answer is 5"])
    assert noisy["accuracy"] == 1.0 and noisy["spurious_steps"] == 1, noisy
    print("self-check OK - scorer handles normalisation, partial credit, "
          "false corrections and hallucinated steps")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--images", type=Path, help="directory of handwriting photographs")
    p.add_argument("--truth", type=Path, help="ground-truth JSON")
    p.add_argument("--model", default="gemini-2.5-flash-lite")
    p.add_argument("--delay", type=float, default=4.0)
    p.add_argument("--allow-repo-path", action="store_true",
                   help="permit images inside the repo (they must never be committed)")
    p.add_argument("--self-check", action="store_true")
    args = p.parse_args()

    if args.self_check:
        self_check()
        return 0
    if not args.images or not args.truth:
        p.error("--images and --truth are required (or use --self-check)")
    if not args.allow_repo_path and REPO in args.images.resolve().parents:
        print(f"error: {args.images} is inside the repo. Student handwriting is personal "
              f"data and must not be committed.\nMove it outside, or pass --allow-repo-path "
              f"if you have confirmed it is git-ignored.", file=sys.stderr)
        return 2
    if "GEMINI_API_KEY" not in os.environ:
        print("error: GEMINI_API_KEY is not set.", file=sys.stderr)
        return 2

    truth = json.loads(args.truth.read_text())
    print(f"PQ-01  model={args.model}  images={len(truth)}\n")

    rows, tot_exp, tot_hit = [], 0, 0
    for name, expected in truth.items():
        img = args.images / name
        if not img.exists():
            print(f"  {name:<20} MISSING")
            continue
        try:
            raw = call_gemini(args.model, img)
        except Exception as e:
            print(f"  {name:<20} ERROR {type(e).__name__}: {e}")
            continue
        got = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        s = score(expected, got)
        tot_exp += s["expected_steps"]
        tot_hit += s["correct_steps"]
        rows.append({"image": name, "expected": expected, "got": got, **s})
        print(f"  {name:<20} {s['correct_steps']}/{s['expected_steps']} steps  "
              f"{s['accuracy']:>5.0%}  (+{s['spurious_steps']} spurious)")
        time.sleep(args.delay)

    if not tot_exp:
        print("\nno images scored")
        return 1

    acc = tot_hit / tot_exp
    print(f"\nstep-level accuracy: {tot_hit}/{tot_exp} = {acc:.1%}")
    print(f"NFR-002 target is >=92%.  {'PASS' if acc >= 0.92 else 'FAIL'} at {acc:.1%}")
    if acc < 0.92:
        print("\nFR-002 is the single point of failure for the photo-capture wedge.\n"
              "If this cannot be raised, the input model has to change - see PRD section 2.")

    OUT_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = OUT_DIR / f"ocr-{ts}.json"
    path.write_text(json.dumps({"model": args.model, "accuracy": acc, "results": rows}, indent=2))
    print(f"\nper-image detail written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
